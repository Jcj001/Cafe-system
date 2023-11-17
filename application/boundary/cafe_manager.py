from flask import Blueprint, render_template, request, redirect, url_for
from application.control.WorkSlotController import GetUnAssignedWorkSlotsController

from application.control.WorkSlotController import GetUpComingWorkSlotController, WorkSlotShifts, AssignWorkSlotController, \
    UnAssignWorkSlotController, GetAssignedWorkSlotsController, GetWorkSlotByIdController
from application.control.UserAccountController import GetStaffAccountController
from application.control.UserProfileController import GetUserProfileController
from application.control.BidController import GetBidsForSlotController

manager = Blueprint("manager", __name__,  url_prefix="/manager")


@manager.route("/view-work-slots")
def view_work_slots():

    shifts_filter = request.args.get('q', None, type=str)

    getWorkSlots = GetUpComingWorkSlotController()

    slots = getWorkSlots.getUpComingWorkSlot(filter=shifts_filter)
    shifts = WorkSlotShifts.getWorkSlotShifts()

    return render_template("./cafe_manager/view_work_slots.html"
                           , slots=slots
                           , title="View Work Slots"
                           , shifts=shifts)


@manager.route("/view-unassigned-slots")
def view_unassigned_work_slots():
    shifts_filter = request.args.get('q', None, type=str)
    getWorkSlots = GetUnAssignedWorkSlotsController()

    slots = getWorkSlots.getAssignedWorkSlots(filter=shifts_filter)
    shifts = WorkSlotShifts.getWorkSlotShifts()

    return render_template("./cafe_manager/view_work_slots.html"
                           , title="View Unassigned Work Slots"
                           , shifts=shifts
                           , slots=slots)


@manager.route("/view-assigned-slots")
def view_assigned_work_slots():
    shifts_filter = request.args.get('q', None, type=str)
    getWorkSlots = GetAssignedWorkSlotsController()

    slots = getWorkSlots.getAssignedWorkSlots(filter=shifts_filter)
    shifts = WorkSlotShifts.getWorkSlotShifts()

    return render_template("./cafe_manager/view_work_slots.html"
                           , title="View Assigned Work Slots"
                           , shifts=shifts
                           , slots=slots)


@manager.route("/view-bids/<int:slot_id>")
def view_bids(slot_id):

    getBids = GetBidsForSlotController()
    getWorkSlot = GetWorkSlotByIdController()

    work_slot = getWorkSlot.getWorkSlotById(slot_id)
    bids = getBids.getBidsForSlot(slot_id)

    return render_template("./cafe_manager/view_bids.html"
                           , title=f"View Bids for {work_slot[1]} ({work_slot[2]})"
                           , bids=bids)


@manager.route("/assign_work_slots")
def assign_work_slot():

    slot_id = request.args.get("slot_id", None, type=int)
    user_id = request.args.get("user_id", None, type=int)

    if not slot_id or not user_id:
        return redirect(url_for("boundary.manager.view_work_slots"))

    workSlot = AssignWorkSlotController()

    workSlot.assignWorkSlot(slot_id, user_id)

    return redirect(url_for("boundary.manager.view_bids", slot_id=slot_id))


@manager.route("/unassign_work_slot")
def unassign_work_slot():

    slot_id = request.args.get("slot_id", None, type=int)
    user_id = request.args.get("user_id", None, type=int)

    if not slot_id or not user_id:
        return redirect(url_for("boundary.manager.view_work_slots"))

    workSlot = UnAssignWorkSlotController()

    workSlot.unAssignWorkSlot(slot_id, user_id)

    return redirect(url_for("boundary.manager.view_bids", slot_id=slot_id))


@manager.route("/view_all_staff")
def view_all_staff():

    userProfile = GetStaffAccountController()
    users = userProfile.getStaffAccounts()

    return render_template("./cafe_manager/view_staff.html"
                           , users=users
                           , title="View Staff")


@manager.route("/view_user_profile/<int:user_id>")
def view_user_profile(user_id):

    userProfile = GetUserProfileController()
    user = userProfile.getUserProfile(user_id)

    return render_template("./cafe_manager/view_user_profile.html"
                           , user=user
                           , title=f"{user[1]} {user[2]}'s Profile")


@manager.route("/assign_work_slot/<int:user_id>", methods=['GET', 'POST'])
def assign_work_slots_to_user(user_id):

    if request.method == 'POST':
        slot_id = request.form.get("slot_id")
        user_id = request.form.get("user_id")
        return redirect(f"{url_for('boundary.manager.assign_work_slot')}?slot_id={slot_id}&user_id={user_id}")

    userController = GetStaffAccountController()
    workSlots = GetUpComingWorkSlotController()

    work_slots = workSlots.getUpComingWorkSlot()
    users = userController.getStaffAccounts()

    return render_template("./cafe_manager/assign_work_slot.html"
                           , title="Assign Work Slot"
                           , users=users
                           , work_slots=work_slots
                           , user_id=user_id)