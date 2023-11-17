from flask import session
from application.entity.user import UserEntity
from .const import ACCESS_LEVELS, CHEF, WAITER, CASHIER


class UserResponses:
    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    USER_NOT_LOGGED_IN = "USER_NOT_LOGGED_IN"
    INVALID_ACCESS_LEVEL = "INVALID_ACCESS_LEVEL"
    RECORD_ADDED_SUCCESSFULLY = "RECORD_ADDED_SUCCESSFULLY"
    CANNOT_REMOVE_SELF = "CANNOT_REMOVE_SELF"
    SUSPENDED_ACCOUNT = "SUSPENDED_ACCOUNT"


class UserProfile(UserResponses):
    def __init__(self):
        self.entity = UserEntity()

    def add_user_profile(self, first_name, last_name, desc):
        self.entity.add_user_profile(first_name, last_name, desc)
        return self.RECORD_ADDED_SUCCESSFULLY

    def update_user_profile(self, id, first_name, last_name, desc):
        self.entity.update_user_profile(id, first_name, last_name, desc)

    def get_all_profiles(self):
        return self.entity.get_all_complete_profile_user()

    def get_new_profiles(self):
        return self.entity.get_all_new_user()


class UserRole(UserResponses):
    def __init__(self):
        self.entity = UserEntity()

    @staticmethod
    def get_roles():
        return [CHEF, WAITER, CASHIER]

    def add_role(self,user_id, role):
        self.entity.add_role(user_id, role)


class SearchUser(UserResponses):
    def __init__(self):
        self.entity = UserEntity()

    def search_by_name(self, name):
        return self.entity.search_user_by_name(name)


class UserAccount(UserResponses):
    def __init__(self):
        self.entity = UserEntity()

    def add_user(self, id, password, phone, profile, user_type):
        if user_type not in ACCESS_LEVELS:
            return self.INVALID_ACCESS_LEVEL

        self.entity.add_user_account(id, password, phone, profile, user_type)
        return self.RECORD_ADDED_SUCCESSFULLY

    def update_user_account(self, user_id, password, phone, profile_id, user_type):
        status = self.entity.update_user_account(user_id, password, phone, profile_id, user_type)

        if status == self.entity.USER_NOT_FOUND:
            return self.USER_NOT_FOUND

        return self.RECORD_ADDED_SUCCESSFULLY

    def delete_user_account(self, account_id):
        if session['user_id'] == account_id:
            return self.CANNOT_REMOVE_SELF

        status = self.entity.delete_user_account_by_id(account_id)
        if status == self.entity.USER_NOT_FOUND:
            return self.USER_NOT_FOUND
        return self.RECORD_ADDED_SUCCESSFULLY

    def get_user(self, account_id=None, user_id=None):
        if account_id:
            user = self.entity.get_user_by_id(account_id)
            return user
        elif user_id:
            user = self.entity.get_user_by_user_id(user_id)
            return user

    def get_all_users(self):
        return self.entity.get_all_users()


class SuspendUserAccount(UserResponses):

    SUSPENDED = "SUSPENDED"
    UNSUSPENDED = None

    def __init__(self):
        self.entity = UserEntity()

    def suspend_user_account(self, account_id):
        if session['user_id'] == account_id:
            return self.CANNOT_REMOVE_SELF

        status = self.entity.set_account_status(account_id=account_id, status=self.SUSPENDED)

        if status == self.entity.USER_NOT_FOUND:
            return self.USER_NOT_FOUND

        return self.RECORD_ADDED_SUCCESSFULLY

    def unsuspend_user_account(self, account_id):
        if session['user_id'] == account_id:
            return self.CANNOT_REMOVE_SELF

        status = self.entity.set_account_status(account_id, self.UNSUSPENDED)
        if status == self.entity.USER_NOT_FOUND:
            return self.USER_NOT_FOUND

        return self.RECORD_ADDED_SUCCESSFULLY


class UserController:
    _userEntity = UserEntity()

    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    USER_NOT_LOGGED_IN = "USER_NOT_LOGGED_IN"
    INVALID_ACCESS_LEVEL = "INVALID_ACCESS_LEVEL"
    RECORD_ADDED_SUCCESSFULLY = "RECORD_ADDED_SUCCESSFULLY"
    CANNOT_REMOVE_SELF = "CANNOT_REMOVE_SELF"
    SUSPENDED_ACCOUNT = "SUSPENDED_ACCOUNT"

    def get_user(self, account_id=None, user_id=None, user_type=None):
        if account_id:
            user = self._userEntity.get_user_by_id(account_id)
        elif user_id:
            user = self._userEntity.get_user_by_user_id(user_id)
        elif user_type:
            user = self._userEntity.get_user_by_user_type(user_type)

        return user

    def get_user_type(self):
        if 'user_id' in session:
            return session['user_type']
        
        return self.USER_NOT_LOGGED_IN

    def get_all_new_users(self):
        return self._userEntity.get_all_new_user()

    def get_suspended_accounts(self):
        return self._userEntity.get_user_by_account_status("SUSPENDED")

    def count_users(self):
        return self._userEntity.count_users()