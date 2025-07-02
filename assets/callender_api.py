from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from config import *
from utils import *

class GoogleCalendarBot:
    _service = None

    @staticmethod
    def initialize():
        try:
            creds = service_account.Credentials.from_service_account_file(
                os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"),
                scopes=['https://www.googleapis.com/auth/calendar']
            )
            GoogleCalendarBot._service = build('calendar', 'v3', credentials=creds)
        except Exception as e:
            log(f"Failed to initialize calendar service: {e}")
            GoogleCalendarBot._service = None

    @staticmethod
    def create_event(summary, start_time, end_time, timezone='UTC+3',
                     description=None, location=None, attendees=None, color_id=None,
                     extended_properties=None):
        if not GoogleCalendarBot._service:
            log("Service not initialized")
            return None
        try:
            event = {
                'summary': summary,
                'description': description,
                'visibility': "public",
                'start': {'dateTime': start_time, 'timeZone': timezone},
                'end': {'dateTime': end_time, 'timeZone': timezone},
            }

            if location:
                event['location'] = location
            if color_id:
                event['colorId'] = color_id
            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]
            if extended_properties:
                event['extendedProperties'] = {'public': extended_properties}

            calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
            return GoogleCalendarBot._service.events().insert(calendarId=calendar_id, body=event).execute()
        except Exception as e:
            log(f"Failed to create event: {e}")
            return None


def watch_calendar():
    if not GoogleCalendarBot._service:
        GoogleCalendarBot.initialize()

    calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
    body = {
        "id": os.getenv("GOOGLE_CALENDAR_ID"),  # a UUID
        "type": "web_hook",
        "address": "https://"+os.getenv("SERVE_IP")+"/google-calendar/webhook"
    }

    try:
        response = GoogleCalendarBot._service.events().watch(calendarId=calendar_id, body=body).execute()
        log(f"Watch response: {response}")
        return response
    except Exception as e:
        log(f"Failed to create watch: {e}")
        return None
