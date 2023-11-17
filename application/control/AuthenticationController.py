from datetime import datetime

from application.entity.AuthenticationEntity import LoginUserEntity
from flask import session


logged_in_users = dict()


class LoginUserController:

    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    SUSPENDED_ACCOUNT = "SUSPENDED_ACCOUNT"

    def __init__(self):
        self.entity = LoginUserEntity()

    def loginUser(self, user_id, password):
        user = self.entity.getUserByUserID(user_id)
        if not user:
            return self.USER_NOT_FOUND

        if user[6] != password:
            return self.INVALID_PASSWORD

        if user[9] == "SUSPENDED":
            return self.SUSPENDED_ACCOUNT

        session['user_id'] = user[0]
        session['user_type'] = user[7]
        session['complete_profile'] = True if user[8] else False

        full_name = user[1] + f" {user[2]}" if user[2] else ""

        logged_in_users[user[0]] = {
            "id": user[0],
            "full_name": full_name,
            "user_id": user_id,
            "last_login": "Active",
            "user_type": session['user_type']
        }

        return session['user_type']


class LogoutUserController:
    def __init__(self):
        self.entity = LoginUserEntity()

    def logoutUser(self,):
        if 'user_id' in session:
            user = logged_in_users.get(session['user_id'])
            if user:
                user['last_login'] = datetime.now().strftime("%d/%b - %H:%M")
            session.pop('user_id')
            session.pop('user_type')
            session.pop('complete_profile')


class GetAllLoginActivityController:
    def getLoginActivity(self):
        return logged_in_users