import boto3
import os
from dotenv import load_dotenv

load_dotenv()

sns_client = boto3.client("sns",
                          aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
                          region_name=os.getenv("AWS_REGION")
)

def send_sms(phone_num, message):
    try:
        response = sns_client.publish(
            PhoneNumber=phone_num,
            Message=message
        )
        print(f"Message sent successfully. MessageId: {response['MessageId']}")
        return response
    except Exception as e:
        print(f"Failed to send message: {e}")
        return None
