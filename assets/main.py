from dotenv import load_dotenv
import os
from config import Flags, Errors
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

def main():
    log("starting main script")
    id = Rooms.new_room("some_room",5)
    id_event = Events.new_event("some_event")
    id_guide = Guides.assign(Users.new_user("some_iser", "some_mail", "some_pass"))
    Event_Guide_Relation.add_relation(id_event, id_guide)
    Event_Room_Relation.add_relation(id_event, id)
    EV_id = Available_Events.new(id_event, id, id_guide)
    Occupied_Events.new()


    Available_Events.remove(EV_id)
    Event_Guide_Relation.remove_relation(id_event, id_guide)
    Event_Room_Relation.remove_relation(id_event, id)
    user_id = Guides.get_user_id(id_guide)
    Guides.remove(id_guide)
    Users.delete_user(user_id)
    Rooms.delete_room(id)
    Events.delete_event(id_event)

    
    
    
    pass

if __name__ == "__main__":
    start_time = time.time()    
    init()
    log("main init complete")
    main()
    print(f"Finished test in {round(time.time()-start_time, 2)}")