import mysql.connector
import config


class Database:
    def __init__(self):
        self._database_connection = mysql.connector.connect(
            host=config.botConfig["host"],
            user=config.botConfig["user"],
            password=config.botConfig["password"],
            port=config.botConfig["port"],
            database=config.botConfig["database"],
            charset='utf8mb4'
        )
        self._cursor = self._database_connection.cursor(buffered=True)
