from dotenv import load_dotenv
import os
from config import Flags, Errors
from users import Users, Guides
from utils import *
from interface import *
from api import *
import time

def init():
    load_dotenv()
    if os.getenv("LOG") != None:
        Flags.LOG_FLAG = True
    if os.getenv("DEBUG") != None:
        Flags.DEBUG_FLAG = True
    if os.getenv("TIME_LAST_SHOW") != None:
        Flags.TIME_LAST_SHOW = int(os.getenv("TIME_LAST_SHOW"))
    init_log()
    init_MainDB()

def main():
    log("starting main script")
    
    pass

if __name__ == "__main__":
    start_time = time.time()    
    init()
    log("main init complete")
    main()
    print(f"Finished test in {round(time.time()-start_time, 2)}")