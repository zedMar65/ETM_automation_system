from dotenv import load_dotenv
import os
from config import Flags, Errors
from users import Users, Guides
from utils import *
from interface import *
from api import *
import time
from server import start_server
import threading
from api import check_and_run_monthly_task
from callender_api import GoogleCalendarBot

def init():
    # load env vars
    load_dotenv()
    if os.getenv("LOG") != None:
        Flags.LOG_FLAG = True
    if os.getenv("DEBUG") != None:
        Flags.DEBUG_FLAG = True
    if os.getenv("TIME_LAST_SHOW") != None:
        Flags.TIME_LAST_SHOW = int(os.getenv("TIME_LAST_SHOW"))
    if os.getenv("TIME_FIRST_SHOW") != None:
        Flags.TIME_FIRST_SHOW = int(os.getenv("TIME_FIRST_SHOW"))
    if os.getenv("SERVE_PORT") != None:
        Flags.SERVE_PORT = int(os.getenv("SERVE_PORT"))
    if os.getenv("SERVE_IP") != None:
        Flags.SERVE_IP = str(os.getenv("SERVE_IP"))
    if os.getenv("GOOGLE_CLIENT_ID") != None:
        Flags.GOOGLE_CLIENT_ID = str(os.getenv("GOOGLE_CLIENT_ID"))
    if os.getenv("GOOGLE_REDIRECT_URI") != None:
        Flags.GOOGLE_REDIRECT_URI = str(os.getenv("GOOGLE_REDIRECT_URI"))
    if os.getenv("GOOGLE_CLIENT_SECRET") != None:
        Flags.GOOGLE_CLIENT_SECRET = str(os.getenv("GOOGLE_CLIENT_SECRET"))
    init_log()
    init_MainDB()

def main():
    # After user callback:
    GoogleCalendarBot.initialize()
    GoogleCalendarBot.create_event(
        summary="Bot-Scheduled Sync",
        start_time="2025-07-01T10:00:00",
        end_time="2025-07-01T10:30:00",
    )

    # log("starting main script")
    # monthly_thread = threading.Thread(target=check_and_run_monthly_task, daemon=True)
    # monthly_thread.start()
    # start_server()
    return

if __name__ == "__main__":
    init()
    log("main init complete")
    main()