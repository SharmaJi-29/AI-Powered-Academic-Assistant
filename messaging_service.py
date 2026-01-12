# messaging_service.py

from twilio.rest import Client

# ----------------------------
# Twilio credentials here
# ----------------------------
ACCOUNT_SID = 'Your Account SID'
AUTH_TOKEN = 'Your Account Authentication Token'

FROM_NUMBER = 'Your Twillo Number'  


TO_NUMBER = 'Personal Mobile Number'    

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_study_reminder(subject, topic):
    message_body = f"📘 Study Reminder\nSubject: {subject}\nTopic: {topic}"

    message = client.messages.create(
        body=message_body,
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )

    print("SMS sent:", message.sid)
