from database import LoggingDB, MainDB
import os
from config import Flags

def init_log() -> bool:
    try:
        LoggingDB.connect()
        with open(os.environ.get("BUILD_SCRIPT_INTERNAL"), "r") as build_file:
            build_script = build_file.read()
        LoggingDB.execute_script(build_script)
        log("logging Init complete")
    except Exception as e:
        log(f"Error while initing log: {e}")

def log(msg, user=-1, ip="internal"):
    try:
        if Flags.LOG_FLAG:
            LoggingDB.execute("INSERT INTO logs (user_id, user_ip, message) VALUES(?, ?, ?)", (user, ip, msg))
        if Flags.DEBUG_FLAG:
            print(f"[{user}], [{ip}], [{msg}]")
    except Exception as e:
        print(f"Error while Logging: {e}, last_msg: [{msg}]")

def init_MainDB() -> int:
    try:
        MainDB.connect()
        with open(os.environ.get("BUILD_SCRIPT_TIMELINES"), "r") as build_file:
            build_script = build_file.read()
        MainDB.execute_script(build_script)
        log("MainDB init complete")
        return 1
    except Exception as e:
        log(f"Error while Initing MainDB: {e}")
        return -1

def time_to_int(TIME) -> int:
    return int(str(TIME["year"])+str(TIME["month"])+str(TIME["day"])+str(TIME["hour"])+str(TIME["minute"]))

def int_to_time(TIME) -> {}:
    return {
        "year": (TIME/100000000),
        "month": ((TIME/1000000)%100),
        "day": ((TIME/10000)%100),
        "hour": ((TIME/100)%100),
        "minute": (TIME%100) 
    }

