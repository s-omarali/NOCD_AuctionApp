from routes.db import get_db_connection
class Bid:
    def __init__(self, listing_id, amount, bidder_id=None, id=None, created_at=None):
        self.listing_id = listing_id
        self.amount = amount
        self.bidder_id = bidder_id
        self.id = id
        self.created_at = created_at

    def save(self):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO bids (listing_id, amount, bidder_id)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (self.listing_id, self.amount, self.bidder_id))
            conn.commit()
            self.id = cursor.lastrowid
        conn.close()

    def to_dict(self):
        return {
            "id": self.id,
            "listing_id": self.listing_id,
            "amount": self.amount,
            "bidder_id": self.bidder_id,
            "created_at": self.created_at,
        }

    @staticmethod
    def get_highest_bid(listing_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM bids WHERE listing_id = %s ORDER BY amount DESC LIMIT 1",
                (listing_id,),
            )
            row = cursor.fetchone()
        conn.close()
        return Bid(**row) if row else None

    @staticmethod
    def get_for_listing(listing_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM bids WHERE listing_id = %s", (listing_id,))
            rows = cursor.fetchall()
        conn.close()
        return [Bid(**row) for row in rows]