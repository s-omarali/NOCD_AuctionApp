import sys
import os
from flask import Blueprint, request, jsonify
from models.Bid import Bid  


from models.Listing import Listing

listing_bp = Blueprint('listings', __name__)

# POST AND GET from same route

@listing_bp.route('/', methods=['POST'])
def create_listing():
    data = request.get_json()
    listing = Listing(**data)
    listing.save()
    return jsonify(listing.to_dict()), 201

@listing_bp.route('/', methods=['GET'])
def get_listings():
    listings = Listing.get_all()
    return jsonify([l.to_dict() for l in listings])
