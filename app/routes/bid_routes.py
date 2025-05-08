
from flask import Blueprint, request, jsonify
from models.Bid import Bid  
from models.Listing import Listing
from datetime import datetime
from send_noti import send_sms
from routes.db import get_db_connection


bid_bp = Blueprint('bids', __name__)

def get_user_phone(user_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT phonenumber FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
    conn.close()
    return row['phonenumber'] if row else None

@bid_bp.route('/bids', methods=['POST'])
def place_bid():
    data = request.get_json()

    # Validate listing existence
    listing = Listing.get_by_id(data['listing_id'])
    if not listing:
        return jsonify({"error": "Listing not found"}), 404

    # Validate listing is still active
    if datetime.now() > listing.end_time:
        return jsonify({"error": "Listing has ended"}), 400

    # Validate bid amount
    highest_bid = Bid.get_highest_bid(data['listing_id'])
    if highest_bid and data['amount'] <= highest_bid.amount:
        return jsonify({"error": "Bid amount must be higher than the current highest bid"}), 400
    
     # Notify the previous highest bidder (if any)
    if highest_bid:
        previous_bidder_phone = get_user_phone(highest_bid.bidder_id)  # Replace with actual logic to get phone number
        if previous_bidder_phone:
            send_sms(previous_bidder_phone, f"You have been outbid on listing '{listing.title}'.")

    # Save the bid
    bid = Bid(**data)
    bid.save()
    

    # To notify the lister
    lister_phone = get_user_phone(listing.lister_id)  # Replace with actual logic to get phone number
    if lister_phone:
        send_sms(lister_phone, f"A new bid of ${data['amount']} has been placed on your listing '{listing.title}'.")
    return jsonify(bid.to_dict()), 201

@bid_bp.route('/bids/<int:listing_id>', methods=['GET'])
def get_bids(listing_id):
    bids = Bid.get_for_listing(listing_id)
    return jsonify([b.to_dict() for b in bids]), 200