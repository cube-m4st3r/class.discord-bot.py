from classes.person import Person

class School_Teacher(Person):
    def __init__(self, id=None):
        super().__init__()
        self._cursor = self._database_connection.cursor()
        
        if id is not None:
            self._id = id
            person = self.fill_school_teacher(id)
            self._givenname = person._get_givenname()
            self._surname = person._get_surname()
        else: 
            pass
    
    def fill_school_teacher(self, id):
        sql = f"SELECT idperson FROM teacher WHERE idteacher={id}"
        self._cursor.execute(sql)
        teacher_id = self._cursor.fetchone()[0]
        return Person(id=teacher_id)
    
    def add_teacher_to_database(self, idperson):
        sql = f"INSERT INTO teacher VALUES(null, {idperson})"
        self._cursor.execute(sql)
        self._database_connection.commit()

        sql = "SELECT LAST_INSERT_ID()"
        self._cursor.execute(sql)
        return self._cursor.fetchone()[0]

    def retrieve_idteacher_list(self):
        sql = f"SELECT idteacher FROM teacher"
        self._cursor.execute(sql)
        
        idteacher_list = list()
        for idteacher in self._cursor.fetchall():
            idteacher_list.append(idteacher[0])
        
        return idteacher_list
    
    def _get_id(self):
        return self._id
