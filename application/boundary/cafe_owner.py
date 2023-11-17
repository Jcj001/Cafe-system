from flask import Blueprint, render_template, redirect, url_for, session, abort, request, flash
from application.control.const import CAFE_OWNER
from application.control.WorkSlotController import *

owner = Blueprint("owner", __name__, url_prefix="/owner")


@owner.before_request
def check_user_validity():
    if 'user_id' not in session:
        return redirect(url_for("boundary.auth.login"))

    if session['user_type'] != CAFE_OWNER:
        return abort(403)


@owner.route("/")
def view_work_slots():

    shift = request.args.get('q', None, type=str)

    upcoming = GetUpComingWorkSlotController()
    slots = upcoming.getUpComingWorkSlot(filter=shift)

    shifts = WorkSlotShifts.getWorkSlotShifts()

    return render_template("./cafe_owner/view_work_slots.html"
                           , title="Upcoming Work Slots"
                           , page_for="Upcoming"
                           , slots=slots
                           , shifts=shifts)


@owner.route("/create-work-slot", methods=['GET', 'POST'])
def create_work_slot():

    work_slots_dates = DateRangeCalculator.get_dates_range()
    shifts = WorkSlotShifts.getWorkSlotShifts()

    if request.method == 'POST':
        shift = request.form.get('shift')
        date = request.form.get('date')

        workSlot = AddWorkSlotController()
        workSlot.addWordSlot(shift, date)

        return redirect(url_for("boundary.owner.create_work_slot"))

    return render_template("./cafe_owner/create_work_slots.html"
                           , work_slots_dates=work_slots_dates
                           , shifts=shifts
                           , title="Create Work Slot")


@owner.route("/view-all-work-slot")
def view_all_work_slot():

    shift = request.args.get('q', None, type=str)

    slotController = GetAllWorkSlotsController()
    slots = slotController.getAllWorkSlots(filter=shift)

    shifts = WorkSlotShifts.getWorkSlotShifts()

    return render_template("./cafe_owner/view_work_slots.html"
                           , title="View All Work Slots"
                           , slots=slots
                           , shifts=shifts)


@owner.route("/update-work-slot/<int:slot_id>", methods=['GET', 'POST'])
def update_work_slot(slot_id):

    if request.method == 'POST':
        shift = request.form.get('shift')
        date = request.form.get('date')

        workSlot = UpdateWorkSlotController()
        stat = workSlot.updateWorkSlot(slot_id, shift, date)

        return redirect(url_for("boundary.owner.view_work_slots"))

    work_slots_dates = DateRangeCalculator.get_dates_range()
    shifts = WorkSlotShifts.getWorkSlotShifts()

    slotController = GetWorkSlotByIdController()
    slot = slotController.getWorkSlotById(slot_id=slot_id)

    return render_template("./cafe_owner/create_work_slots.html"
                           , work_slots_dates=work_slots_dates
                           , shifts=shifts
                           , title="Update Work Slot"
                           , slot=slot)


@owner.route("/delete-work-slot/<int:work_slot_id>")
def delete_work_slot(work_slot_id):

    workSlot = DeleteWorkSlotController()
    workSlot.deleteWorkSlot(work_slot_id)

    flash("Deleted Successfully")
    return redirect(url_for("boundary.owner.view_work_slots"))