import random
import time
from employee import Employee

def mode_1_create_table(db):
    cursor = db.get_cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            last_name VARCHAR(100),
            first_name VARCHAR(100),
            middle_name VARCHAR(100),
            birth_date DATE,
            gender VARCHAR(10)
        );
    """)

    db.commit()
    print('Таблица "employees" создана, если не была ещё создана')

def mode_2_add_employee(db, fio, birth_date, gender):
    parts = fio.split(" ")

    if len(parts) != 3:
        print('ФИО должно содержать 3 части: Фамилия, Имя, Отчество')
        return

    last, first, middle = parts

    emp = Employee(
        last_name=last,
        first_name=first,
        middle_name=middle,
        birth_date=birth_date,
        gender=gender
    )

    emp.save(db)
    print('Сотрудник сохранен')

def mode_3_list_employees(db):
    cursor = db.get_cursor()

    cursor.execute("""
        SELECT DISTINCT last_name, first_name, middle_name, birth_date, gender
        FROM employees
        ORDER BY last_name, first_name, middle_name;
    """)

    rows = cursor.fetchall()

    if not rows:
        print('Сотрудников не найдено')
        return

    print('Сотрудники:')
    for row in rows:
        last_name, first_name, middle_name, birth_date, gender = row

        emp = Employee(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birth_date=str(birth_date),
            gender=gender
        )

        age = emp.get_age()

        print(f'{last_name} {first_name} {middle_name} | {age} лет | {birth_date} | {gender}')

def mode_4_fill_employees(db):
    TOTAL_MAIN = 1_000_000
    BATCH_SIZE = 10_000
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    first_name_male = ['Ivan', 'Petr', 'Michail', 'Denis', 'Grigoriy', 'Dmitry', 'Anton', 'Afanasiy', 'Bogdan', 'Ilya', 'Vadim']
    first_name_female = ['Anna', 'Anastasiya', 'Diana', 'Arina', 'Elizaveta', 'Kristina', 'Daria', 'Alena', 'Mariya', 'Alexandra', 'Nadezhda']
    middle_name_female = ['Ivanovna', 'Petrovna', 'Denisovna', 'Grigoryevna', 'Dmitrievna', 'Antonovna', 'Afanasyevna', 'Bogdanovna', 'Vadimovna']
    middle_name_male = ['Ivanovich', 'Petrovich', 'Denisovich', 'Grigoriyevich', 'Dmitrievich', 'Antonovich', 'Afanasiyevich', 'Bogdanovich', 'Vadimovich']
    last_name_male = ['Kuzmin', 'Lakomkin', 'Sidorov', 'Petrov', 'Ivanov', 'Smirnov']
    last_name_female = ['Kuzmina', 'Lakomkina', 'Sidorova', 'Petrova', 'Ivanova', 'Smirnova']
    last_name_f = ['Fedotov', 'Fedorov', 'Fomin', 'Frolov']

    def random_birth_date():
        year = random.randint(1980, 2007)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f'{year:04d}-{month:02d}-{day:02d}'

    def random_employee():
        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            last_name = random.choice(last_name_male)
            first_name = random.choice(first_name_male)
            middle_name = random.choice(middle_name_male)
        if gender == 'Female':
            last_name = random.choice(last_name_female)
            first_name = random.choice(first_name_female)
            middle_name = random.choice(middle_name_female)

        birth_date = random_birth_date()
        return Employee(last_name, first_name, middle_name, birth_date, gender)

    remaining = TOTAL_MAIN
    inserted = 0

    while remaining > 0:
        current_batch_size = min(BATCH_SIZE, remaining)
        batch = [random_employee() for _ in range(current_batch_size)]
        Employee.bulk_save(db, batch)

        remaining -= current_batch_size
        inserted += current_batch_size
        print(f'Добавлено {inserted}/{TOTAL_MAIN} сотрудников')

    special_employees = []
    for _ in range(100):
        birth_date = random_birth_date()
        last_name = 'A'
        last_name = random.choice(last_name_f)
        first_name = random.choice(first_name_male)
        middle_name = random.choice(middle_name_male)

        emp = Employee(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birth_date=birth_date,
            gender='Male'
        )
        special_employees.append(emp)

    Employee.bulk_save(db, special_employees)
    print("Добавлены 100 сотрудников мужского пола с фамилией на 'F' ")
    input("Режим 4 завершил свою работу")


def mode_5_male_f(db):
    cursor = db.get_cursor()

    start = time.perf_counter()

    cursor.execute("""
        SELECT last_name, first_name, middle_name, birth_date, gender
        FROM employees
        WHERE gender = %s AND last_name LIKE %s;
    """, ('Male', 'F%'))

    rows = cursor.fetchall()

    end = time.perf_counter()
    elapsed_ms = (end - start) * 1000

    print(f'Найдено записей: {len(rows)}')
    print(f'Время выполнения запроса: {elapsed_ms:.2f} ms')

    print("\nПервые пять сотрудников:")
    for row in rows[:5]:
        last_name, first_name, middle_name, birth_date, gender = row
        emp = Employee(last_name, first_name, middle_name, birth_date, gender)
        age = emp.get_age()
        print(f'{last_name} {first_name} {middle_name} | {age} лет | {birth_date} | {gender}')

def mode_6_optimize(db):
    cursor = db.get_cursor()

    print("Создаю индекс по gender и last_name")
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_employees_male_f
        ON employees (last_name);
    """)
    db.commit()
    print("Индекс создан\n")

    cursor.execute("ANALYZE employees;")
    db.commit()
    print("Статистика по таблице обновлена\n")

    start = time.perf_counter()

    cursor.execute("""
        SELECT last_name, first_name, middle_name, birth_date, gender 
        FROM employees
        WHERE gender = %s AND last_name LIKE %s
    """, ("Male", "F%"))


    rows = cursor.fetchall()

    end = time.perf_counter()
    elapsed_ms = (end - start) * 1000

    print(f'Найдено записей: {len(rows)}')
    print(f'Время выполнения запроса: {elapsed_ms:.2f} ms')

    print("\nПервые пять сотрудников:")
    for row in rows[:5]:
        last_name, first_name, middle_name, birth_date, gender = row
        emp = Employee(last_name, first_name, middle_name, birth_date, gender)
        age = emp.get_age()
        print(f'{last_name} {first_name} {middle_name} | {age} лет | {birth_date} | {gender}')