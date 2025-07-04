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
import datetime
import shutil

def init():
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
    if os.path.isfile("../backup/database/internal_data.db"):
        shutil.copyfile("../backup/database/internal_data.db", "./database/internal_data.db")
    else:
        init_log()
    if os.path.isfile("../backup/database/timelines_data.db"):
        shutil.copyfile("../backup/database/timelines_data.db", "./database/timelines_data.db")
    else:
        init_MainDB()

    super_admin()
    # load_events()
    # load_rooms()
    # load_guides()
    # load_relations()
    # load_hours()

def load_events():
    with open(educations, "r") as e:
        for line in e:
            e_type = line.split(" ")[0]
            e_name = " ".join(line.split(",")[0].split(" ")[1:])
            e_time = "".join(line.split(",")[1].split(":"))
            Events.new_event(e_name, e_time, e_type)

def load_rooms():
    with open(classrooms, "r") as e:
        for line in e:
            e_name = line.split(",")[0]
            e_capacity = line.split(",")[1]
            Rooms.new_room(e_name, e_capacity)

def load_guides():
    with open(guides, "r") as e:
        for line in e:
            e_name = line.split(",")[0]
            Guides.assign(Users.new_user(e_name, e_name, "password"))

def load_relations():
    with open(guides, "r") as e:
        for line in e:
            e_name = line.split(",")[0]
            guide_id = Guides.get_group_id(Users.get_id(e_name))
            e_events = line.split("\"")[1].split(",")
            for event in e_events:
                ev = " ".join(event.split(" ")[1:])
                event_id = Events.get_id(ev)
                Event_Guide_Relation.add_relation(event_id, guide_id)
    with open(classrooms, "r") as e:
        for line in e:
            e_name = line.split(",")[0]
            room_id = Rooms.get_id(e_name)
            e_events = line.split(",")[2:]
            for event in e_events:
                ev = " ".join(event.split(" ")[1:])
                event_id = Events.get_id(ev)
                Event_Room_Relation.add_relation(event_id, room_id)

def load_hours():
    with open(availability) as e:
        for line in e:
            e_name = line.split(",")[0]
            day = line.split(",")[1]
            start_time = "".join(line.split(",")[2].split(":")[:2])
            end_time = "".join(line.split(",")[-1].split(":")[:2])[:-1]
            WorkHours.add(Guides.get_group_id(Users.get_id(e_name)), name_to_int(day)+1, start_time, end_time)

def super_admin():
    admin_id = Users.new_user(os.getenv("ADMIN_NAME"), os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD"))
    Admins.assign(admin_id)

if __name__ == "__main__":
    log(f"Starting build")
    init()
    log(f"Build finished")