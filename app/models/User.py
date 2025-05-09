from routes.db import get_db_connection

class User:
    def __init__(self, username, phone_number,password, id=None):
        self.id = id
        self.username = username
        self.phone_number = phone_number
        self.password = password

    def save(self):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO users (username, password)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (self.username, self.password))
            conn.commit()
            self.id = cursor.lastrowid
        conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
        conn.close()
        return User(**row) if row else None
    
    @staticmethod
    def get_phone_by_id(user_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT phone_number FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
        conn.close()
        return row['phone_number'] if row else None
    
    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * from users WHERE username = %s", (username,))
            row = cursor.fetchone()

        conn.close()
        return User(**row) if row else None # get matching user else none 

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "phone_number": self.phone_number # not including password in return
            
        }
