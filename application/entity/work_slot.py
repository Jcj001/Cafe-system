import datetime

from .models import WorkSlot, Bids
from application.entity import db
from application.control.user import UserController


class WorkSlotsEntity:

    def get_work_slots(self, date=None, shift=None):
        workSlot = WorkSlot.query
        if date:
            workSlot = workSlot.filter(WorkSlot.date >= datetime.date.today())

        if shift:
            workSlot = workSlot.filter(WorkSlot.shift_time==shift)

        if date:
            workSlot = workSlot.order_by(WorkSlot.date.desc())

        workSlot = workSlot.all()

        return workSlot

    def get_work_slot(self, slot_id=None):
        return WorkSlot.query.get_or_404(slot_id)

    def get_unassigned_work_slots(self):
        return WorkSlot.query.filter(WorkSlot.date >= datetime.date.today()).filter(WorkSlot.assigned_to==None).all()

    def get_assigned_work_slots(self):
        return WorkSlot.query.filter(WorkSlot.date >= datetime.date.today()).filter(WorkSlot.assigned_to!=None).all()

    def assign_work_slot(self, user_id, slot_id):
        workSlot = WorkSlot.query.get_or_404(slot_id)
        user = UserController().get_user(account_id=user_id)

        if user in workSlot.assigned_to:
            return False

        bid = Bids.query.filter(Bids.workslot==workSlot).filter(Bids.bidder==user).first()
        bid.status = "APPROVED"

        workSlot.assigned_to.append(user)
        db.session.commit()

        return True

    def unassign_work_slot(self, user_id, slot_id):
        workSlot = WorkSlot.query.get_or_404(slot_id)
        user = UserController().get_user(account_id=user_id)

        if user in workSlot.assigned_to:
            workSlot.assigned_to.remove(user)
            bid = Bids.query.filter(Bids.workslot == workSlot).filter(Bids.bidder == user).first()
            bid.status = "PENDING"
            db.session.commit()
            return True

        return False
