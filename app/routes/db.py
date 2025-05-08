import pymysql
import os
from dotenv import load_dotenv
import pymysql.cursors
load_dotenv()  # Load environment variables from a .env file
def get_db_connection():
    

    return pymysql.connect(
        host="bidding-db-aws.cpoegk8yqyce.us-east-2.rds.amazonaws.com",
        user="admin",
        password=os.getenv("DB_PASSWORD"), 
        database="bidding_db_aws",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )