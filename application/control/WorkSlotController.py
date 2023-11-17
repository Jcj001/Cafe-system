import datetime
from datetime import date, timedelta
from application.entity.WorkSlotEntity import WorkSlotEntity


class WorkSlotResponses:
    RECORD_ADDED_SUCCESSFULLY = "RECORD_ADDED_SUCCESSFULLY"
    ALREADY_EXIST = "ALREADY_EXIST"


class AddWorkSlotController:
    def __init__(self):
        self.entity = WorkSlotEntity()

    def addWordSlot(self, shift, date):
        # TODO: GET WORKSLOT BY DATE AND SHIFT TIME AND CHECK IF ALREADY EXIST
        date_obj = datetime.datetime.strptime(date, "%d/%b/%y")
        return self.entity.addWorkSlot(date_obj, shift)


class UpdateWorkSlotController(WorkSlotResponses):
    def __init__(self):
        self.entity = WorkSlotEntity()

    def updateWorkSlot(self, id, shift, date):
        date_obj = datetime.datetime.strptime(date, "%d/%b/%y")
        stat = self.entity.updateWorkSlot(id, date_obj, shift)

        return self.RECORD_ADDED_SUCCESSFULLY


class DeleteWorkSlotController:
    def __init__(self):
        self.entity = WorkSlotEntity()

    def deleteWorkSlot(self, id):
        self.entity.deleteWorkSlot(slot_id=id)


class GetWorkSlotByIdController:
    def __init__(self):
        self.entity = WorkSlotEntity()

    def getWorkSlotById(self, slot_id):
        slot = self.entity.getWorkSlotById(slot_id=slot_id)
        list_slot = [slot[0], datetime.datetime.strptime(slot[1], '%Y-%m-%d %H:%M:%S'), slot[2]]
        return list_slot


class DateRangeCalculator:

    @staticmethod
    def get_dates_range(start=date.today(), end=date.today() + timedelta(days=6)):
        date_list = []
        curr_date = start
        while curr_date <= end:
            date_list.append(curr_date)
            curr_date += timedelta(days=1)

        return date_list


class WorkSlotShifts:

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

    @staticmethod
    def getWorkSlotShifts():
        return WorkSlotShifts.SHIFTS


class GetUpComingWorkSlotController:
    def __init__(self):
        self.entity = WorkSlotEntity()

    def getUpComingWorkSlot(self, filter=None):
        return self.entity.getUpcomingWorkSlots(filter)


class GetAllWorkSlotsController:
    def __init__(self):
        self.entity = WorkSlotEntity()

    def getAllWorkSlots(self, filter=None):
        return self.entity.getAllWorkSlots(filter)


class AssignWorkSlotController:
    def __init__(self):
        self.entity = WorkSlotEntity()

    def assignWorkSlot(self, slot_id, user_id):
        return self.entity.assignWorkSlot(slot_id, user_id)


class UnAssignWorkSlotController:
    def __init__(self):
        self.entity = WorkSlotEntity()

    def unAssignWorkSlot(self, slot_id, user_id):
        return self.entity.unAssignWorkSlot(slot_id, user_id)


class GetAssignedWorkSlotsController:
    def __init__(self):
        self.entity = WorkSlotEntity()

    def getAssignedWorkSlots(self, filter=None):
        return self.entity.getAssignedWorkSlots(filter)


class GetUnAssignedWorkSlotsController:
    def __init__(self):
        self.entity = WorkSlotEntity()

    def getAssignedWorkSlots(self, filter=None):
        return self.entity.getUnAssignedWorkSlots(filter)
