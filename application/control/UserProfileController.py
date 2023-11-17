from application.entity.UserProfileEntity import UserProfileEntity

from application.control.const import CHEF, WAITER, CASHIER


class CreateUserProfileController:
    def __init__(self):
        self.entity = UserProfileEntity()

    def createUserProfile(self, job_title, desc):
        self.entity.addUserProfile(job_title, desc)


class UpdateUserProfileController:
    def __init__(self):
        self.entity = UserProfileEntity()

    def updateUserProfile(self, row_id, job_title, desc):
        self.entity.updateUserProfile(row_id, job_title, desc)


class SearchUserProfileController:
    def __init__(self):
        self.entity = UserProfileEntity()

    def searchUserProfileByJobTitle(self, job_title):
        return self.entity.searchUserProfileByJobTitle(job_title)


class GetUserProfileByIdController:
    def __init__(self):
        self.entity = UserProfileEntity()

    def getUserByID(self, id):
        return self.entity.getUserById(id)


class GetNewUserProfileController:
    def __init__(self):
        self.entity = UserProfileEntity()

    def getNewProfiles(self):
        return self.entity.getNewUserProfiles()


class GetAllUserProfileController:
    def __init__(self):
        self.entity = UserProfileEntity()

    def getAllProfiles(self):
        return self.entity.getAllUserProfiles()


class GetUserProfileController:
    def __init__(self):
        self.entity = UserProfileEntity()

    def getUserProfile(self, row_id):
        return self.entity.getUserProfile(row_id)


class GetUserRolesController:

    @staticmethod
    def getUserRoles():
        return [CHEF, WAITER, CASHIER]