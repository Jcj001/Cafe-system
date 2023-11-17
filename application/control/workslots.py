import datetime
from datetime import date, timedelta
from application.entity.work_slot import WorkSlotsEntity


class WorkSlotResponses:
    RECORD_ADDED_SUCCESSFULLY = "RECORD_ADDED_SUCCESSFULLY"
    ALREADY_EXIST = "ALREADY_EXIST"


class AddWorkSlot(WorkSlotResponses):
    def __init__(self):
        self.entity = WorkSlotsEntity()

    def addWordSlot(self, shift, date):
        date_obj = datetime.datetime.strptime(date, "%d/%b/%y")
        stat = self.entity.add_work_slot(date_obj, shift)

        if stat == "ALREADY_EXIST":
            return self.ALREADY_EXIST
        return self.RECORD_ADDED_SUCCESSFULLY


class UpdateWorkSlot(WorkSlotResponses):
    def __init__(self):
        self.entity = WorkSlotsEntity()

    def updateWorkSlot(self, id, shift, date):
        date_obj = datetime.datetime.strptime(date, "%d/%b/%y")
        stat = self.entity.update_work_slot(id, shift, date_obj)

        if stat == "ALREADY_EXIST":
            return self.ALREADY_EXIST

        return self.RECORD_ADDED_SUCCESSFULLY


class DeleteWorkSlot(WorkSlotResponses):
    def __init__(self):
        self.entity = WorkSlotsEntity()

    def deleteWorkSlot(self, id):
        self.entity.delete_work_slot(id)


class GetWorkSlots:

    _workSlotEntity = WorkSlotsEntity()

    MORNING = {
        "shift": "Morning",
        "time-start": datetime.time(hour=9),
        "time-end": datetime.time(hour=15)
    }

    EVENING = {
        "shift": "Evening",
        "time-start": datetime.time(hour=15),
        "time-end": datetime.time(hour=21)
    }

    FULL_DAY = {
        "shift": "Full Day",
        "time-start": datetime.time(hour=9),
        "time-end": datetime.time(hour=21)
    }
    SHIFTS = [MORNING, EVENING, FULL_DAY]

    RECORD_ADDED_SUCCESSFULLY = "RECORD_ADDED_SUCCESSFULLY"

    def get_work_slot_by_id(self, slot_id):
        return self._workSlotEntity.get_work_slot(slot_id=slot_id)

    def get_dates_range(self, start=date.today(), end=date.today() + timedelta(days=6)):
        date_list = []
        curr_date = start
        while curr_date <= end:
            date_list.append(curr_date)
            curr_date += timedelta(days=1)

        return date_list

    def get_shifts(self):
        return self.SHIFTS

    def get_all_work_slots(self):
        return self._workSlotEntity.get_work_slots()

    def get_upcoming_workslots(self, shift_filter=None):
        date = datetime.date.today()
        return self._workSlotEntity.get_work_slots(date=date, shift=shift_filter)

    def search_work_slot(self, shift=None):
        return self._workSlotEntity.get_work_slots(shift=shift)

    def get_assigned_work_slots(self):
        return self._workSlotEntity.get_assigned_work_slots()

    def get_unassigned_work_slots(self):
        return self._workSlotEntity.get_unassigned_work_slots()

    def assign_work_slot(self, slot_id, bidder_id):
        return self._workSlotEntity.assign_work_slot(bidder_id, slot_id)

    def unassign_work_slot(self, slot_id, bidder_id):
        return self._workSlotEntity.unassign_work_slot(bidder_id, slot_id)