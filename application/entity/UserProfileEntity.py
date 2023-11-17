import sqlite3


class UserProfileEntity:
    def __init__(self):
        self.connection = sqlite3.connect("./application/entity/database.db")
        self.cursor = self.connection.cursor()

    def addUserProfile(self, job_title, desc):
        query = "INSERT INTO user ('job_title', 'desc') VALUES (?, ?)"
        self.cursor.execute(query, (job_title, desc))
        self.connection.commit()
        self.cursor.close()

    def updateUserProfile(self, id, job_title, desc):
        query = "UPDATE USER SET job_title=?, desc=? where id=?"
        self.cursor.execute(query, (job_title, desc, id))
        self.connection.commit()
        self.cursor.close()

    def getNewUserProfiles(self):
        query = "SELECT id, job_title from user where job_title is not NULL and user_id is NULL"
        rows = self.cursor.execute(query)
        return rows

    def getAllUserProfiles(self):
        query = "SELECT id, job_title, desc, user_id from user"
        rows = self.cursor.execute(query)
        return rows

    def getUserById(self, row_id):
        query = f"SELECT id, job_title, desc, user_type from user where id={row_id}"
        rows = self.cursor.execute(query).fetchone()
        return rows

    def searchUserProfileByJobTitle(self, job_title):
        query = f"SELECT id, job_title, desc, user_id from user where job_title like '%{job_title}%'"
        rows = self.cursor.execute(query)
        return rows

    def getUserProfile(self, row_id):
        query = f"SELECT * FROM user WHERE id={row_id}"
        rows = self.cursor.execute(query).fetchone()
        return rows