from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from application.control.AuthenticationController import LoginUserController, LogoutUserController
from application.control.const import SYSTEM_ADMIN, CAFE_OWNER, CAFE_STAFF, CAFE_MANAGER

authentication = Blueprint("auth", __name__)


@authentication.route("/", methods=['GET', 'POST'])
@authentication.route("/login", methods=['GET', 'POST'])
def login():

    if 'user_id' in session:
        if session['user_type'] == SYSTEM_ADMIN:
            return redirect(url_for('boundary.admin.dashboard'))
        elif session['user_type'] == CAFE_OWNER:
            return redirect(url_for('boundary.owner.view_work_slots'))
        elif session['user_type']  == CAFE_STAFF:
            return redirect(url_for("boundary.staff.view_all_work_slots"))
        elif session['user_type']  == CAFE_MANAGER:
            return redirect(url_for("boundary.manager.view_work_slots"))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        auth = LoginUserController()
        authStatus = auth.loginUser(user_id, password)
        if authStatus == auth.USER_NOT_FOUND:
            flash("User doesn't exist")
            return redirect(url_for("boundary.auth.login"))
        elif authStatus == auth.INVALID_PASSWORD:
            flash("Invalid Password")
            return redirect(url_for("boundary.auth.login"))
        elif authStatus == auth.SUSPENDED_ACCOUNT:
            flash("Your Account is Suspended")
            return redirect(url_for("boundary.auth.login"))

        if authStatus == SYSTEM_ADMIN:
            return redirect(url_for('boundary.admin.dashboard'))
        elif authStatus == CAFE_OWNER:
            return redirect(url_for('boundary.owner.view_work_slots'))
        elif authStatus == CAFE_STAFF:
            return redirect(url_for("boundary.staff.view_all_work_slots"))
        elif authStatus == CAFE_MANAGER:
            return redirect(url_for("boundary.manager.view_work_slots"))

    return render_template("login.html")


@authentication.route("/logout")
def logout():
    auth = LogoutUserController()
    auth.logoutUser()
    return redirect(url_for("boundary.auth.login"))