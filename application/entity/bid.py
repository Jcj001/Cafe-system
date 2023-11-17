from .models import Bids
from application.entity import db
from application.control.const import PENDING


class BidEntity:
    def add_bid(self, user_id, work_slot_id):
        check = Bids.query.filter(Bids.work_slot_id==work_slot_id).filter(Bids.bidder_id==user_id).first()

        if check:
            return "ALREADY BIDDED"

        bid = Bids(bidder_id=user_id, work_slot_id=work_slot_id, status=PENDING)
        db.session.add(bid)
        db.session.commit()

    def get_user_bids(self, user_id):
        return Bids.query.filter(Bids.bidder_id==user_id).all()

    def delete_bid_by_id(self, bid_id):
        bid = Bids.query.get_or_404(bid_id)
        db.session.delete(bid)
        db.session.commit()

    def search_user_bids(self, user_id, status):
        return Bids.query.filter(Bids.bidder_id==user_id).filter(Bids.status==status).all()

    def get_slot_bids(self, slot_id):
        return Bids.query.filter(Bids.work_slot_id==slot_id).all()

    def update_bid_status(self, slot_id, user_id, status):
        bid = Bids.query.filter(Bids.work_slot_id==slot_id).filter(Bids.bidder_id==user_id).first()
        if bid:
            bid.status = status
