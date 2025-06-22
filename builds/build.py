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

classrooms = "./Classrooms-Grid view.csv"
educations = "./Educations-Grid view.csv"
guides = "./Guides-Grid view.csv"
availability = "./Guides Availability-Grid view.csv"

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
    init_MainDB()

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
                Event_Guide_Relation.add_relation(Events.get_id(event), guide_id)

def super_admin():
    admin_id = Users.new_user(os.getenv("ADMIN_NAME"), os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD"))
    Admins.assign(admin_id)

if __name__ == "__main__":
    init()
    super_admin()
    load_events()
    load_rooms()
    load_guides()
    load_relations()
