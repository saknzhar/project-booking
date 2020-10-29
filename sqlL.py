import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    def get_zakazchikov(self, status = True):
        with self.connection:
            return self.cursor.execute("select *from  'Zakazy' where 'status' = ?", (status,)).fetchall()
    def add_user(self, user_id, id_zakaz, mail):
        with self.connection:
            return self.cursor.execute("INSERT INTO `Zakazy` (`user_id`, `id_zakaz`, `mail`) VALUES(?,?,?)", (user_id, id_zakaz, mail))
    