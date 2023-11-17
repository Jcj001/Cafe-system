from application.entity import db


SlotAssignments = db.Table('slot_assignments',
                    db.Column('slot_id', db.Integer, db.ForeignKey('work_slot.id')),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                    )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    desc = db.Column(db.Text)
    phone = db.Column(db.String(20))
    user_id = db.Column(db.String(30))
    password = db.Column(db.String(50))
    user_type = db.Column(db.String(10))
    role = db.Column(db.String(20))
    account_status = db.Column(db.String(10))

    bids = db.relationship("Bids", backref="bidder")

    def __repr__(self):
        return f"<User>: {self.email} - {self.user_type}"


class WorkSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    shift_time = db.Column(db.String(10))

    bids = db.relationship("Bids", backref="workslot")
    assigned_to = db.relationship("User", secondary=SlotAssignments, backref="assigned_workslots")

    def __repr__(self):
        return f"<WORK SLOT>: {self.date}"


class Bids(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_slot_id = db.Column(db.Integer, db.ForeignKey(WorkSlot.id))
    bidder_id = db.Column(db.Integer, db.ForeignKey(User.id))
    status = db.Column(db.String(20))

    def __repr__(self):
        return f"<Bids> {self.bidder.first_name} {self.workslot.date}"
