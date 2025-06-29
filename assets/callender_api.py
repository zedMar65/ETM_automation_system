from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

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
            print(f"Failed to initialize calendar service: {e}")
            GoogleCalendarBot._service = None

    @staticmethod
    def create_event(summary, start_time, end_time, timezone='UTC+3', description=None):
        if not GoogleCalendarBot._service:
            print("Service not initialized")
            return None
        try:
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': timezone,
                }
            }
            calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
            return GoogleCalendarBot._service.events().insert(calendarId=calendar_id, body=event).execute()
        except Exception as e:
            print(f"Failed to create event: {e}")
            return None
