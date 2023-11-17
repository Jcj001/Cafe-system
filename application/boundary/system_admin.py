from flask import Blueprint, render_template, request, session, redirect, url_for, abort
from application.control.const import ACCESS_LEVELS, SYSTEM_ADMIN, CAFE_OWNER, CAFE_STAFF, CAFE_MANAGER
from application.control.UserAccountController import CreateUserAccountController, GetUserAccountController,\
    DeleteUserAccountController, SuspendUserAccountController, UnSuspendUserAccountController, \
    UpdateUserAccountController, CountUserAccountController, SearchSuspendedUserAccountByIdController, SearchSuspendedUserAccountController ,\
    SearchUserAccountByIdController, SearchUserAccountByRowIdController
from application.control.UserProfileController import CreateUserProfileController, GetUserProfileByIdController, \
    SearchUserProfileController, UpdateUserProfileController, GetAllUserProfileController, GetNewUserProfileController
from application.control.AuthenticationController import GetAllLoginActivityController


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.before_request
def check_user_validity():
    if 'user_id' not in session:
        return redirect(url_for("boundary.auth.login"))

    if session['user_type'] != SYSTEM_ADMIN:
        return abort(403)


@admin.route("/")
def dashboard():

    auth = GetAllLoginActivityController()
    userCounter = CountUserAccountController()

    login_info = auth.getLoginActivity()

    user_counts = {
        SYSTEM_ADMIN: 0,
        CAFE_STAFF: 0,
        CAFE_MANAGER: 0,
        CAFE_OWNER: 0,
        "TOTAL": 0
    }

    for user in userCounter.countUserAccount():
        user_counts[user[0]] = user[1]
        user_counts['TOTAL'] = user_counts['TOTAL'] + user[1]

    return render_template("system_admin/dashboard.html"
                           , login_info=login_info
                           , user_counts=user_counts)


@admin.route("/create-user-account", methods=['GET', 'POST'])
def create_user_account():

    if request.method == 'POST':
        row_id = request.form.get('row_id')
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        phone = request.form.get('phone')
        access_level = request.form.get('access_level')

        accountController = CreateUserAccountController()
        accountController.createUserAccount(row_id, user_id, password, first_name, last_name, phone, access_level)

        return redirect(url_for("boundary.admin.create_user_account"))

    getProfiles = GetNewUserProfileController()
    profiles = getProfiles.getNewProfiles()


    return render_template("system_admin/create_user_account.html"
                           , title="Create User Account"
                           , profiles=profiles
                           , ACCESS_LEVELS=ACCESS_LEVELS)


@admin.route("/create-user-profile", methods=['GET', 'POST'])
def create_user_profile():

    if request.method == 'POST':
        job_title = request.form.get('job_title')
        desc = request.form.get('description')

        profileController = CreateUserProfileController()
        profileController.createUserProfile(job_title, desc)
        return redirect(url_for('boundary.admin.create_user_profile'))

    return render_template("system_admin/create_user_profile.html"
                           , title="Create User Profile"
                            , ACCESS_LEVELS=ACCESS_LEVELS)


@admin.route("/view-user-accounts")
def view_user_accounts():

    name = request.args.get("q", None, type=str)

    userAccount = GetUserAccountController()
    searchAccount = SearchUserAccountByIdController()

    if name:
        users = searchAccount.searchUserByName(name)
    else:
        users = userAccount.getAllUserAccount()

    return render_template("system_admin/view-user-accounts.html"
                           , users=users
                           , title="View User Accounts")


@admin.route("/view-suspended-user-accounts")
def view_suspended_user_accounts():

    user_id = request.args.get("q", None, type=str)

    if user_id:
        searchAccount = SearchSuspendedUserAccountByIdController()
        users = searchAccount.searchSupendedAccountByUserId(user_id)
    else:
        searchAccount = SearchSuspendedUserAccountController()
        users = searchAccount.searchSupendedAccount()

    return render_template("system_admin/view-user-accounts.html"
                           , users=users
                           , title="View Suspended User Accounts")


@admin.route("/view-user-profiles")
def view_user_profiles():

    title = request.args.get("q", None, type=str)
    userSearch = SearchUserProfileController()
    userProfile = GetAllUserProfileController()

    if title:
        users = userSearch.searchUserProfileByJobTitle(title)
    else:
        users = userProfile.getAllProfiles()

    return render_template("system_admin/view-user-profiles.html"
                           , users=users)


@admin.route("/delete-user-account/<int:account_id>")
def delete_user_account(account_id):

    deleteAccount = DeleteUserAccountController()
    deleteAccount.deleteUserAccountByRowId(account_id)

    return redirect(url_for("boundary.admin.view_user_accounts"))


@admin.route("/suspend-user-account/<int:account_id>")
def suspend_user_account(account_id):
    suspendUser = SuspendUserAccountController()
    suspendUser.suspendUserAccount(account_id)
    return redirect(url_for("boundary.admin.view_user_accounts"))


@admin.route("/unsuspend-user-account/<int:account_id>")
def unsuspend_user_account(account_id):
    unsuspend = UnSuspendUserAccountController()
    unsuspend.suspendUserAccount(account_id)
    return redirect(url_for("boundary.admin.view_user_accounts"))


@admin.route("/update-user-account/<int:account_id>", methods=['GET', 'POST'])
def update_user_account(account_id):
    userAccount = SearchUserAccountByRowIdController()
    user = userAccount.searchUserAccount(account_id)

    if request.method == "POST":
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        phone = request.form.get('phone')
        access_level = request.form.get('access_level')

        updateAccount = UpdateUserAccountController()
        updateAccount.updateUserAccount(user_id, password, first_name, last_name, phone, access_level, account_id)

        return redirect(url_for("boundary.admin.view_user_accounts"))

    return render_template("system_admin/create_user_account.html"
                           , user=user
                           , page_type="UPDATE"
                           , title="Update User Account"
                           , ACCESS_LEVELS=ACCESS_LEVELS)


@admin.route("/update-user-profile/<int:account_id>", methods=['GET', 'POST'])
def update_user_profile(account_id):
    getProfile = GetUserProfileByIdController()
    user = getProfile.getUserByID(account_id)

    if request.method == "POST":
        title = request.form.get('job_title')
        desc = request.form.get('description')

        updateProfile = UpdateUserProfileController()
        updateProfile.updateUserProfile(account_id, title, desc)

        return redirect(url_for('boundary.admin.view_user_profiles'))

    return render_template("system_admin/create_user_profile.html"
                           , user=user
                           , title="Update User Profile"
                           , ACCESS_LEVELS=ACCESS_LEVELS
                           , page_type='UPDATE')