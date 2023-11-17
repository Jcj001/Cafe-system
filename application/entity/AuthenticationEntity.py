import sqlite3


class LoginUserEntity:
    def __init__(self):
        self.connection = sqlite3.connect("./application/entity/database.db")
        self.cursor = self.connection.cursor()

    def getUserByUserID(self, user_id):
        query = f"SELECT * from user where user_id='{user_id}'"
        row = self.cursor.execute(query).fetchone()
        return row