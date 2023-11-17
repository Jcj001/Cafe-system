from application.entity.BidEntity import BidEntity
from application.control.const import PENDING, APPROVED, REJECTED


class AddBidController:
    def __init__(self):
        self.entity = BidEntity()

    def addBid(self, bidder_id, work_slot_id):
        # TODO: CHECK IF ALREADY BIDDED
        return self.entity.addBid(bidder_id, work_slot_id)


class DeleteBidController:
    def __init__(self):
        self.entity = BidEntity()

    def deleteBid(self, bid_id):
        return self.entity.deleteBid(bid_id)


class ViewMyBidsController:
    def __init__(self):
        self.entity = BidEntity()

    def viewMyBids(self, user_id, filter_status):
        return self.entity.viewMyBids(user_id, filter_status)


class GetBidStatus:

    @staticmethod
    def getBids():
        return [PENDING, APPROVED, REJECTED]


class GetBidsForSlotController:
    def __init__(self):
        self.entity = BidEntity()

    def getBidsForSlot(self, slot_id):
        return self.entity.getBidsForSlot(slot_id)