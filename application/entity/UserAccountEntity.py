import sqlite3


class UserAccountEntity:
    def __init__(self):
        self.connection = sqlite3.connect("./application/entity/database.db")
        self.cursor = self.connection.cursor()

    def addUserAccount(self, row_id, user_id, password, first_name, last_name, phone, access_level):
        query = "UPDATE user SET first_name=?, last_name=?, user_id=?, password=?, phone=?, user_type=? where id=?"
        self.cursor.execute(query, (first_name, last_name, user_id, password, phone, access_level, row_id))
        self.connection.commit()
        self.cursor.close()

    def searchUserAccountByName(self, name):
        query = f"SELECT id, first_name, last_name, phone, user_type, account_status FROM USER where first_name LIKE '%{name}%' or last_name LIKE '%{name}%'"
        rows = self.cursor.execute(query)
        return rows

    def searchSuspendedAccount(self):
        query = f"SELECT id, user_id, password, phone, user_type, account_status from USER where account_status='SUSPENDED'"
        rows = self.cursor.execute(query)
        return rows

    def searchSuspendedAccountById(self, user_id):
        query = f"SELECT id, user_id, password, phone, user_type, account_status from USER where user_id='{user_id}' and account_status='SUSPENDED'"
        rows = self.cursor.execute(query)
        return rows

    def searchUserByRowId(self, row_id):
        query = f"SELECT id, user_id, password, first_name, last_name, phone, user_type FROM USER where id={row_id}"
        rows = self.cursor.execute(query).fetchone()
        return rows

    def deleteUserAccountByRowId(self, row_id):
        query = f"DELETE FROM user WHERE id={row_id}"
        self.cursor.execute(query)
        self.connection.commit()

    def updateUserAccount(self, user_id, password, first_name, last_name, phone, access_level, id):
        query = f"UPDATE USER SET user_id=?, password=?, first_name=?, last_name=?, phone=?, user_type=? where id=?"
        self.cursor.execute(query, (user_id, password, first_name, last_name, phone, access_level, id))
        self.connection.commit()

    def suspendUserAccount(self, row_id):
        query = f"UPDATE user SET account_status='SUSPENDED' where id='{row_id}'"
        self.cursor.execute(query)
        self.connection.commit()

    def unSuspendUserAccount(self, row_id):
        query = f"UPDATE user SET account_status=NULL where id='{row_id}'"
        self.cursor.execute(query)
        self.connection.commit()

    def getAllAccounts(self):
        query = "SELECT id, first_name, last_name, phone, user_type, account_status FROM USER"
        rows = self.cursor.execute(query)
        return rows

    def countUsers(self):
        query = "SELECT user_type, count(id) from user group by user_type"
        return self.cursor.execute(query)

    def addUserRole(self, id, role):
        query = "UPDATE user SET role=? where id = ?"
        print(id, role)
        self.cursor.execute(query, (role, id))
        self.connection.commit()

    def getStaffAccounts(self):
        query = "SELECT id, first_name, last_name, phone, role from USER where user_type='STAFF'"
        return self.cursor.execute(query).fetchall()