# messaging_service.py

from twilio.rest import Client

# ----------------------------
# Twilio credentials here
# ----------------------------
ACCOUNT_SID = "AC6e1da314c8eb8e25e3a5dd1eb26b48a9"
AUTH_TOKEN = "d01185bf772bc567823b0d61233e0e1d"

FROM_NUMBER = "+19529528546"   


TO_NUMBER = "+919098218859"    

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_study_reminder(subject, topic):
    message_body = f"📘 Study Reminder\nSubject: {subject}\nTopic: {topic}"

    message = client.messages.create(
        body=message_body,
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )

    print("SMS sent:", message.sid)