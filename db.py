import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS employees(
            id Integer Primary Key,
            name text,
            age int,
            doj text,
            email text,
            gender text,
            contact int,
            address text
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, name, age, doj, email, gender, contact, address):
        self.cur.execute("insert into employees values (NULL,?,?,?,?,?,?,?)",
                         (name, age, doj, email, gender, contact, address))
        self.con.commit()

    def fetch(self):
        self.cur.execute("SELECT * from employees")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute("delete from employees where id=?", (id,))
        self.con.commit()

    def update(self, id, name, age, doj, email, gender, contact, address):
        self.cur.execute(
            "update employees set name=?, age=?, doj=?, email=?, gender=?, contact=?, address=? where id=?",
            (name, age, doj, email, gender, contact, address, id))
        self.con.commit()
    def shownames(self):
        self.cur.execute('select name from employees')
        rows = self.cur.fetchall()
        return rows
    def showdata(self, name):
        name_pattern = name + '%'
        self.cur.execute('SELECT * FROM employees WHERE name LIKE ?', (name_pattern,))
        rows = self.cur.fetchall()
        return rows
    def sortingID(self):
        self.cur.execute("SELECT * from employees order by id desc")
        rows = self.cur.fetchall()
        return rows
    def sortingIDa(self):
        self.cur.execute("SELECT * from employees order by id")
        rows = self.cur.fetchall()
        return rows
    def sortingNAME(self):
        self.cur.execute("SELECT * from employees order by name desc")
        rows = self.cur.fetchall()
        return rows
    def sortingNAMEa(self):
        self.cur.execute("SELECT * from employees order by name")
        rows = self.cur.fetchall()
        return rows
