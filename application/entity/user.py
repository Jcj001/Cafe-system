from sqlalchemy import or_, func

from .models import User
from application.entity import db


class UserEntity:

    USER_NOT_FOUND = "USER_NOT_FOUND"

    def get_user_by_user_id(self, user_id):
        user = User.query.filter(User.user_id==user_id).first()
        return user

    def get_user_by_id(self, id):
        user = User.query.get(id)
        return user

    def get_all_users(self):
        return User.query.all()

    def get_all_complete_profile_user(self):
        return User.query.filter(User.first_name != None).all()

    def get_all_new_user(self):
        return User.query.filter(User.user_id==None).all()

    def add_user_account(self, id, password, phone, profile, user_type):
        user = User.query.get_or_404(profile)
        user.user_id = id
        user.password = password
        user.phone = phone
        user.user_type = user_type

        db.session.commit()

    def add_user_profile(self, first_name, last_name, desc):
        user = User(first_name=first_name, last_name=last_name, desc=desc)
        db.session.add(user)
        db.session.commit()

    def add_role(self, user_id, role):
        user = User.query.get_or_404(user_id)
        user.role = role
        db.session.commit()

    def count_users(self):
        count = User.query.with_entities(User.user_type, func.count(User.id)).group_by(User.user_type).all()
        print(count)
        return count

    def update_user_profile(self, account_id, first_name, last_name, desc):
        user = User.query.get(account_id)
        if not user:
            return False

        user.first_name = first_name
        user.last_name = last_name
        user.desc = desc

        db.session.commit()

        return True

    def delete_user_account_by_id(self, account_id):
        try:
            user = User.query.get_or_404(account_id)
        except:
            return self.USER_NOT_FOUND

        db.session.delete(user)
        db.session.commit()

        return True

    def set_account_status(self, account_id, status):
        try:
            user = User.query.get_or_404(account_id)
        except:
            return self.USER_NOT_FOUND

        user.account_status = status
        db.session.commit()
        return True

    def get_user_by_account_status(self, status):
        return User.query.filter(User.account_status == status).all()

    def update_user_account(self, user_id, password, phone, profile_id, user_type):
        try:
            user = User.query.get_or_404(profile_id)
        except:
           return self.USER_NOT_FOUND

        user.user_id = user_id
        user.password = password
        user.phone = phone
        user.user_type = user_type

        db.session.commit()

        return True

    def get_user_by_user_type(self, user_type):
        return User.query.filter(User.user_type==user_type).all()

    def search_user_by_name(self, name):
        return User.query.filter(or_(User.first_name.like(f"%{name}%")
                                     , User.last_name.like(f"%{name}%") )).all()
