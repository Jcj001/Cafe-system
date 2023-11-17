from application.entity.bid import BidEntity
from application.control.const import PENDING, APPROVED, REJECTED


class AddBid:
    def __init__(self):
        self.entity = BidEntity()

    def add_bid(self, bidder_id, work_slot_id):
        return self.entity.add_bid(bidder_id, work_slot_id)


class DeleteBid:
    def __init__(self):
        self.entity = BidEntity()

    def delete_bid_by_id(self, bid_id):
        return self.entity.delete_bid_by_id(bid_id)


class GetBid:
    def __init__(self):
        self.entity = BidEntity()

    def get_user_bids(self, user_id, filter_status=None):
        if filter_status:
            return self.entity.search_user_bids(user_id=user_id, status=filter_status)
        return self.entity.get_user_bids(user_id)

    def get_slot_bids(self, slot_id):
        return self.entity.get_slot_bids(slot_id)

    @staticmethod
    def get_bid_status():
        return [PENDING, APPROVED, REJECTED]


class UpdateBid:
    def __init__(self):
        self.entity = BidEntity()

    def set_bid_status(self, slot_id, user_id, status):
        self.entity.update_bid_status(slot_id, user_id, status)