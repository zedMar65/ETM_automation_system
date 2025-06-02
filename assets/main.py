from dotenv import load_dotenv
import os
from config import Flags, Errors
from users import Users, Guides
from utils import *
from interface import *
import time

def init():
    # print_bee_movie_script()
    load_dotenv()
    if os.getenv("LOG") != None:
        Flags.LOG_FLAG = True
    if os.getenv("DEBUG") != None:
        Flags.DEBUG_FLAG = True
    init_log()
    init_MainDB()

# wrapper, TODO: extrude later

def fetch_by_event(event_id):
    try:
        free_events = []
        from_time = time_to_int(from_time)
        to_time = time_to_int(to_time)
        if to_time < from_time:
            raise ValueError(Errors.wrong_time)
        events = Available_Events.find(event_id=event_id)
        for event in events:
            availability = Available_Events.get_availability(event[0], from_time, to_time)
            free_events += availability
        return free_events
    except Exception as e:
        log(f"Error while fetching spots by time: {e}")


def fetch_by_time(from_time, to_time):
    try:
        free_events = []
        from_time = time_to_int(from_time)
        to_time = time_to_int(to_time)
        if to_time < from_time:
            raise ValueError(Errors.wrong_time)
        events = Available_Events.find()
        for event in events:
            availability = Available_Events.get_availability(event[0], from_time, to_time)
            free_events += availability
        return free_events
    except Exception as e:
        log(f"Error while fetching spots by time: {e}")

def main():
    log("starting main script")
    user_id = Users.new_user("bronius", "bronius@gmail.com", "password")
    guide_id = Guides.assign(user_id)
    event_id = Events.new_event("some event", 90)
    room_id = Rooms.new_room("some room", 4)
    Event_Guide_Relation.add_relation(event_id, guide_id)
    Event_Room_Relation.add_relation(event_id, room_id)
    available_event_id = Available_Events.find(event_id=event_id, room_id=room_id)[0][0]
    Occupied_Events.new(
        time_to_int({"year": "2024", "month": "05", "day": "15", "hour": "09", "minute": "45"}), 
        time_to_int({"year": "2024", "month": "05", "day": "15", "hour": "10", "minute": "45"}), 
        available_event_id
        )

    # print(Available_Events.find())

    Events.delete_event(event_id)
    Rooms.delete_room(room_id)
    Users.delete_user(user_id)
    pass

if __name__ == "__main__":
    start_time = time.time()    
    init()
    log("main init complete")
    main()
    print(f"Finished test in {round(time.time()-start_time, 2)}")