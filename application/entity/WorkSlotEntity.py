import datetime
import sqlite3


class WorkSlotEntity:
    def __init__(self):
        self.connection = sqlite3.connect("./application/entity/database.db")
        self.cursor = self.connection.cursor()

    def addWorkSlot(self, date, shift_time):
        query = "INSERT INTO work_slot (date, shift_time) VALUES (?, ?)"
        self.cursor.execute(query, (date, shift_time))
        self.connection.commit()

    def updateWorkSlot(self, slot_id, date, shift_time):
        query = "UPDATE work_slot SET date=?, shift_time=? WHERE id=?"
        self.cursor.execute(query, (date, shift_time, slot_id))
        self.connection.commit()

    def deleteWorkSlot(self, slot_id):
        query = f"DELETE FROM work_slot WHERE id={slot_id}"
        self.cursor.execute(query)
        self.connection.commit()

    def getWorkSlotById(self, slot_id):
        query = f"SELECT * FROM work_slot WHERE id={slot_id}"
        rows = self.cursor.execute(query).fetchone()
        return rows

    def getAllWorkSlots(self, filter):
        query = f"SELECT * FROM work_slot"

        if filter:
            query += f" WHERE shift_time='{filter}'"

        rows = self.cursor.execute(query).fetchall()
        return rows

    def getUpcomingWorkSlots(self, filter):
        date_today = datetime.date.today()
        query = f"SELECT * FROM work_slot where date>='{date_today}'"

        if filter:
            query += f" AND shift_time='{filter}'"

        rows = self.cursor.execute(query).fetchall()

        return rows

    def assignWorkSlot(self, slot_id, user_id):
        query = "INSERT INTO slot_assignments (slot_id, user_id) VALUES (?, ?)"
        self.cursor.execute(query, (slot_id, user_id))

        query = "UPDATE bids SET status='APPROVED' WHERE work_slot_id=? and bidder_id=?"
        self.cursor.execute(query, (slot_id, user_id))

        self.connection.commit()

    def unAssignWorkSlot(self, slot_id, user_id):
        query = "DELETE FROM slot_assignments WHERE slot_id=? and user_id=?"
        self.cursor.execute(query, (slot_id, user_id))

        query = "UPDATE bids SET status='PENDING' WHERE work_slot_id=? and bidder_id=?"
        self.cursor.execute(query, (slot_id, user_id))

        self.connection.commit()

    def getAssignedWorkSlots(self, filter):
        query = "select * from work_slot w inner join slot_assignments sa on w.id = sa.slot_id"

        if filter:
            query += f" WHERE shift_time = '{filter}'"

        rows = self.cursor.execute(query).fetchall()
        return rows

    def getUnAssignedWorkSlots(self, filter):
        query = "select * from work_slot w left join slot_assignments sa on w.id = sa.slot_id where slot_id is NULL"

        if filter:
            query += f" AND shift_time='{filter}'"

        rows = self.cursor.execute(query).fetchall()
        return rows