import sqlite3


class BidEntity:
    def __init__(self):
        self.connection = sqlite3.connect("./application/entity/database.db")
        self.cursor = self.connection.cursor()

    def addBid(self, bidder_id, work_slot_id):
        query = "INSERT INTO bids ('bidder_id', 'work_slot_id', 'status') VALUES (?, ?, ?)"
        self.cursor.execute(query, (bidder_id, work_slot_id, "PENDING"))
        self.connection.commit()

    def deleteBid(self, bid_id):
        query = f"DELETE FROM bids WHERE id={bid_id}"
        self.cursor.execute(query)
        self.connection.commit()

    def viewMyBids(self, bidder_id, filter_status):
        query = f"SELECT b.id, w.date, w.shift_time, status FROM bids b INNER JOIN work_slot w on w.id=b.work_slot_id WHERE bidder_id={bidder_id}"

        if filter_status:
            query += f" AND status='{filter_status}'"

        rows = self.cursor.execute(query).fetchall()
        return rows

    def getBidsForSlot(self, slot_id):
        query = f"select first_name, last_name, role, phone, status, work_slot_id, bidder_id, sa.user_id from bids b inner join user u on u.id = b.bidder_id inner join work_slot ws on ws.id = b.work_slot_id left join slot_assignments sa on u.id = sa.user_id where b.work_slot_id = {slot_id}"
        rows = self.cursor.execute(query).fetchall()
        return rows