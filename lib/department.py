import sqlite3

CONN = sqlite3.connect(":memory:")
CURSOR = CONN.cursor()

class Department:
    all_departments = []

    def __init__(self, name, location):
        self.id = None
        self.name = name
        self.location = location
        Department.all_departments.append(self)

    @staticmethod
    def create_table():
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """)
        CONN.commit()

    @staticmethod
    def drop_table():
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO departments (name, location) VALUES (?, ?)",
                (self.name, self.location)
            )
            CONN.commit()
            self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, location):
        dept = cls(name, location)
        dept.save()
        return dept

    @staticmethod
    def instance_from_db(row):
        dept = Department(row[1], row[2])
        dept.id = row[0]
        return dept

    @staticmethod
    def find_by_name(name):
        CURSOR.execute("SELECT * FROM departments WHERE name=?", (name,))
        row = CURSOR.fetchone()
        if row:
            return Department.instance_from_db(row)
        return None

    @staticmethod
    def get_all():
        CURSOR.execute("SELECT * FROM departments")
        rows = CURSOR.fetchall()
        return [Department.instance_from_db(row) for row in rows]

    def employees(self):
        from employee import Employee
        return [e for e in Employee.get_all() if e.department_id == self.id]
