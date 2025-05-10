
from flask import Blueprint, request, jsonify
from models.Bid import Bid  
from models.Listing import Listing
from datetime import datetime
from send_noti import send_sms
from routes.db import get_db_connection
from decimal import Decimal, InvalidOperation


bid_bp = Blueprint('bids', __name__)

def get_user_phone(user_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT phone_number FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
    conn.close()
    return row['phone_number'] if row else None

@bid_bp.route('/', methods=['POST'])
def place_bid():
    data = request.get_json()

    
    listing = Listing.get_by_id(data['listing_id'])
    if not listing:
        return jsonify({"error": "Listing not found"}), 404

    
    if datetime.now() > listing.end_time:
        return jsonify({"error": "Listing has ended"}), 400

    
    try:
        bid_amount = Decimal(data['amount'])
    except (InvalidOperation, KeyError):
        return jsonify({"error": "Invalid bid amount"}), 400

    
    highest_bid = Bid.get_highest_bid(data['listing_id'])
    if highest_bid and bid_amount <= highest_bid.amount:
        return jsonify({"error": "Bid amount must be higher than the current highest bid"}), 400

    # Phone number alert logic: NOT IMPLEMENTED CORRECTLY YET NEED TO CHANGE EC2 SETTINGS
    if highest_bid:
        previous_bidder_phone = get_user_phone(highest_bid.bidder_id)
        if previous_bidder_phone:
            send_sms(previous_bidder_phone, f"You have been outbid on listing '{listing.title}'.")

    # Save bid
    bid = Bid(
        listing_id=data['listing_id'],
        bidder_id=data['bidder_id'],
        amount=bid_amount
    )
    bid.save()

    
    lister_phone = get_user_phone(listing.lister_id)
    if lister_phone:
        send_sms(lister_phone, f"A new bid of ${bid_amount} has been placed on your listing '{listing.title}'.")
    
    
    return jsonify({
    "message": "Bid placed successfully",
    "bid": bid.to_dict()
    }), 201

# get each bid's data based on specific listing id
@bid_bp.route('/<int:listing_id>', methods=['GET'])
def get_bids(listing_id):
    bids = Bid.get_for_listing(listing_id)
    return jsonify([b.to_dict() for b in bids]), 200