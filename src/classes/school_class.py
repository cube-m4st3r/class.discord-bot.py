from database import Database
class School_Class(Database):
    def __init__(self, id):
        self._id = id
        self._name = ""
        self._class_teacher = ""

    
    def update_name(self):
        sql = ""
        self._cursor.execute(sql)
        self._database_connection.commit()