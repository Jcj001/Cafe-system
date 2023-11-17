from flask import Blueprint, render_template, session, request, url_for, abort, redirect
from application.control.const import *

from application.control.UserAccountController import AddUserRoleController
from application.control.UserProfileController import GetUserProfileController, GetUserRolesController
from application.control.WorkSlotController import GetUpComingWorkSlotController, WorkSlotShifts
from application.control.BidController import AddBidController, DeleteBidController, ViewMyBidsController, GetBidStatus

staff = Blueprint("staff", __name__, url_prefix="/staff")


@staff.before_request
def check_user_validity():
    if 'user_id' not in session:
        return redirect(url_for("boundary.auth.login"))

    if session['user_type'] != CAFE_STAFF:
        return abort(403)


@staff.route("/add_role/<int:user_id>", methods=['POST'])
def add_role(user_id):
    role = request.form.get("role")
    userRole = AddUserRoleController()
    userRole.addUserRole(user_id, role)
    session['complete_profile'] = True
    return redirect(url_for("boundary.staff.view_all_work_slots"))


@staff.route("/")
@staff.route("/view_all_work_slots")
def view_all_work_slots():

    shift = request.args.get('q', None, type=str)

    if not session['complete_profile']:
        userRoles = GetUserRolesController.getUserRoles()
        return render_template("./cafe_staff/complete_profile.html"
                               , roles=userRoles)

    work_slots = GetUpComingWorkSlotController()
    work_slots = work_slots.getUpComingWorkSlot(filter=shift)

    shifts = WorkSlotShifts.getWorkSlotShifts()

    return render_template("cafe_staff/view_work_slots.html"
                           , title="View Work Slots"
                           , work_slots=work_slots
                           , shifts=shifts)


@staff.route("/view_my_bids")
def view_my_bids():

    filter_status = request.args.get("q", None, type=str)

    getbids = ViewMyBidsController()
    bids = getbids.viewMyBids(session['user_id'], filter_status=filter_status)

    bid_staus = GetBidStatus.getBids()
    return render_template("./cafe_staff/view_my_bids.html"
                           , title="View My Bids"
                           , bids=bids
                           , status=bid_staus)


@staff.route("/add_bid/<int:work_slot_id>")
def add_bid(work_slot_id):
    addBid = AddBidController()
    res = addBid.addBid(session['user_id'], work_slot_id)

    return redirect(url_for("boundary.staff.view_all_work_slots"))


@staff.route("/remove/<int:bid_id>")
def remove_bid(bid_id):
    deleteBid = DeleteBidController()
    res = deleteBid.deleteBid(bid_id)
    return redirect(url_for("boundary.staff.view_all_work_slots"))


@staff.route("/view-profile")
def view_profile():
    userAccount = GetUserProfileController()
    me = userAccount.getUserProfile(session['user_id'])
    return render_template("./cafe_staff/view_profile.html"
                           , title="View User Account"
                           , user=me)