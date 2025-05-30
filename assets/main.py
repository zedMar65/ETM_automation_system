from dotenv import load_dotenv
import os
import config
from utils import *
from interface import *
import time

def init():
    load_dotenv()
    if os.getenv("LOG") != None:
        config.LOG_FLAG = True
    if os.getenv("DEBUG") != None:
        config.DEBUG_FLAG = True
    init_log()
    init_MainDB()

def main():
    log("starting main script")
    user = Users.find(user_name="bronius")
    
    if len(user) > 0:
        Users.delete_user(user[0][0])

    id = Users.new_user("bronius", "mail@gmail.com", "seacret_pass")
    guide_id = Guides.assign(id)
    log(f"id: {id}")
    log(f"id by guide_id: {Guides.get_user_id(guide_id)}")
    log(f"{guide_id} - {Guides.get_group_id(id)}")

    pass

if __name__ == "__main__":
    start_time = time.time()    
    init()
    log("main init complete")
    main()
    print(f"Finished test in {round(time.time()-start_time, 2)}")