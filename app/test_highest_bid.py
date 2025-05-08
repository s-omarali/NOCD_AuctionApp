from models.Bid import Bid

def test_get_highest_bid():
    listing_id = 1  # Replace with the listing_id you want to test
    highest_bid = Bid.get_highest_bid(listing_id)
    
    if highest_bid:
        print("Highest Bid:")
        print(highest_bid.to_dict())
    else:
        print("No bids found for listing_id:", listing_id)

if __name__ == "__main__":
    test_get_highest_bid()