from classes.database import Database

class Person(Database):
    def __init__(self, id=None):
        super().__init__()  # Initialize the Database class
        self._cursor = self._database_connection.cursor()

        if id is not None:
            self._id = id
            self._givenname, self._surname = self.__fill_person(id)
        else:
            self._id = None
            self._givenname = None
            self._surname = None

    def __fill_person(self, id):
        sql = f"SELECT givenname, surname FROM person WHERE idperson={id}"
        self._cursor.execute(sql)
        return self._cursor.fetchone()

    def _add_person_to_database(self, givenname, surname):
        sql = f"INSERT INTO person VALUES(null, '{givenname}', '{surname}')"
        self._cursor.execute(sql)
        self._database_connection.commit()

        sql = "SELECT LAST_INSERT_ID()"
        self._cursor.execute(sql)
        return self._cursor.fetchone()[0]

    def _get_givenname(self):
        return self._givenname

    def _get_surname(self):
        return self._surname
    
    def _get_full_name(self):
        return f"{self._get_givenname()} {self._get_surname()}"
