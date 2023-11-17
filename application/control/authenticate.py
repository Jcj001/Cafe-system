import datetime

from flask import session
from application.entity.user import UserEntity

logged_in_users = dict()


class Authentication:

    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    USER_NOT_LOGGED_IN = "USER_NOT_LOGGED_IN"
    INVALID_ACCESS_LEVEL = "INVALID_ACCESS_LEVEL"
    RECORD_ADDED_SUCCESSFULLY = "RECORD_ADDED_SUCCESSFULLY"
    CANNOT_REMOVE_SELF = "CANNOT_REMOVE_SELF"
    SUSPENDED_ACCOUNT = "SUSPENDED_ACCOUNT"

    def __init__(self):
        self.entity = UserEntity()

    def login(self, user_id, password):
        user = self.entity.get_user_by_user_id(user_id)
        if not user:
            return self.USER_NOT_FOUND

        if user.password != password:
            return self.INVALID_PASSWORD

        if user.account_status == "SUSPENDED":
            return self.SUSPENDED_ACCOUNT

        session['user_id'] = user.id
        session['user_type'] = user.user_type
        session['complete_profile'] = True if user.role else False

        full_name = user.first_name + f" {user.last_name}" if user.last_name else ""

        logged_in_users[user.id] = {
            "id": user.id,
            "full_name": full_name,
            "user_id": user_id,
            "last_login": "Active",
            "user_type": user.user_type
        }

        return user

    def logout_user(self):
        if 'user_id' in session:
            user = logged_in_users.get(session['user_id'])
            if user:
                user['last_login'] = datetime.datetime.now().strftime("%d/%b - %H:%M")
            session.pop('user_id')
            session.pop('user_type')
            session.pop('complete_profile')

    def get_logged_in_users(self):
        return logged_in_users