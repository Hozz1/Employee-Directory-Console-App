from datetime import date

class Employee:
    def __init__(self, last_name, first_name, middle_name, birth_date, gender):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_date = birth_date
        self.gender = gender

    def save(self, db):
        cursor = db.get_cursor()
        cursor.execute("""
            INSERT INTO employees (last_name, first_name, middle_name, birth_date, gender)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.last_name, self.first_name, self.middle_name, self.birth_date, self.gender))

        db.commit()

    def get_age(self):
        today = date.today()

        year, month, day = map(int, str(self.birth_date).split("-"))
        born = date(year, month, day)

        age = today.year - born.year

        if (today.month, today.day) < (born.month, born.day):
            age -= 1
        return age

    @staticmethod
    def bulk_save(db, employees):
        if not employees:
            return

        cursor = db.get_cursor()
        data = [
            (e.last_name, e.first_name, e.middle_name, e.birth_date, e.gender)
            for e in employees
        ]

        cursor.executemany("""
            INSERT INTO employees (last_name, first_name, middle_name, birth_date, gender)
            VALUES (%s, %s, %s, %s, %s)
        """, data)

        db.commit()