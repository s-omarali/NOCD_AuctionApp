from send_noti import send_sms

response = send_sms("+16053702115", "This is a test message from AWS SNS.")
print(response)