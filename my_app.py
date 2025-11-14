import sys
from db import Database
from models import mode_1_create_table, mode_2_add_employee, mode_3_list_employees, mode_4_fill_employees, mode_5_male_f, mode_6_optimize


def main():
    if len(sys.argv) < 2:
        print("Выберите режим работы")
        return

    mode = sys.argv[1]

    db = Database( # ДАННЫЕ НУЖНО ЗАПОЛНИТЬ!
        host="",
        port="",
        user="",
        password="",
        dbname=""
    )
    db.connect()

    if mode == "1":
        mode_1_create_table(db)
    if mode == "2":
        if len(sys.argv) < 5:
            print('Некорректный ввод')

        fio = sys.argv[2]
        birth_date = sys.argv[3]
        gender = sys.argv[4]

        mode_2_add_employee(db, fio, birth_date, gender)
    if mode == '3':
        mode_3_list_employees(db)
    if mode == '4':
        mode_4_fill_employees(db)
    if mode == '5':
        mode_5_male_f(db)
    if mode == '6':
        mode_6_optimize(db)


if __name__ == "__main__":
    main()