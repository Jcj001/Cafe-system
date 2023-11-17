from application.entity.UserAccountEntity import UserAccountEntity


class CreateUserAccountController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def createUserAccount(self, row_id, user_id, password, first_name, last_name, phone, access_level):
        self.entity.addUserAccount(row_id, user_id, password, first_name, last_name, phone, access_level)


class SearchUserAccountByIdController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def searchUserByName(self, name):
        return self.entity.searchUserAccountByName(name)


class SearchUserAccountByRowIdController:
    def __init__(self):
        self.entity = UserAccountEntity()


    def searchUserAccount(self, row_id):
        return self.entity.searchUserByRowId(row_id)


class SearchSuspendedUserAccountController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def searchSupendedAccount(self):
        return self.entity.searchSuspendedAccount()


class SearchSuspendedUserAccountByIdController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def searchSupendedAccountByUserId(self, user_id):
        return self.entity.searchSuspendedAccountById(user_id)


class DeleteUserAccountController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def deleteUserAccountByRowId(self, row_id):
        return self.entity.deleteUserAccountByRowId(row_id)


class SuspendUserAccountController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def suspendUserAccount(self, row_id):
        return self.entity.suspendUserAccount(row_id)


class UnSuspendUserAccountController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def suspendUserAccount(self, row_id):
        return self.entity.unSuspendUserAccount(row_id)


class UpdateUserAccountController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def updateUserAccount(self, user_id, password, first_name, last_name, phone, access_level ,id):
        self.entity.updateUserAccount(user_id, password, first_name, last_name, phone, access_level, id)


class GetUserAccountController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def getAllUserAccount(self):
        return self.entity.getAllAccounts()


class CountUserAccountController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def countUserAccount(self):
        return self.entity.countUsers()


class AddUserRoleController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def addUserRole(self, id, role):
        self.entity.addUserRole(id, role)


class GetStaffAccountController:
    def __init__(self):
        self.entity = UserAccountEntity()

    def getStaffAccounts(self):
        return self.entity.getStaffAccounts()
