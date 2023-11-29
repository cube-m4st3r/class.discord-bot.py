from classes.database import Database

class User(Database):
    def __init__(self, id=None):
        super().__init__()
        self._cursor = self._database_connection.cursor()

        if id is not None: 
            self._id = id
            self._username = self.__fill_user(id=id)

    def __fill_user(self, id):
        sql = f"SELECT username FROM discorduser WHERE iddiscorduser={id}"
        self._cursor.execute(sql)
        return self._cursor.fetchone()[0]
    
    def _add_user_to_database(self, id, username):
        sql = f"INSERT INTO discorduser VALUES({id}, '{username}')"
        self._cursor.execute(sql)
        self._database_connection.commit()
        return id
    
    def _get_id(self):
        return self._id
    
    def _get_username(self):
        return self._username