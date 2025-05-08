from routes.db import get_db_connection
from datetime import datetime, timedelta

class Listing:
    

    def __init__(self, title, description, starting_price, end_time, image_url=None,lister_id=None,id=None):
        self.title = title
        self.description = description
        self.starting_price = starting_price
        self.end_time = end_time if end_time else datetime.now() + timedelta(days=7)  # 7 day listing period for now
        self.image_url = image_url
        self.lister_id = lister_id
        self.id = id

    def save(self):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO listings (title,description,starting_price,end_time,image_url)
                VALUES(%s,%s,%s,%s,%s)
        """
            cursor.execute(sql,(
                self.title,
                self.description,
                self.starting_price,
                self.end_time,
                self.image_url

            ))
            conn.commit()
            self.id = cursor.lastrowid
        conn.close()
    @staticmethod
    def get_all():
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM listings")
            results = cursor.fetchall()

        conn.close()
        return [Listing(**row) for row in results]
    
    @staticmethod
    def get_by_id(listing_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM listings WHERE id = %s", (listing_id,))
            row = cursor.fetchone()
        conn.close()
        return Listing(**row) if row else None
    
    def to_dict(self):
        return self.__dict__
    

    