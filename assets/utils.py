from database import LoggingDB, MainDB
import os
from config import Flags
from datetime import datetime
import calendars

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
    while TIME["minute"] >= 60:
        TIME["minute"] -= 60
        Time["hour"] += 1
    while TIME["hour"] >= 24:
        TIME["hour"] -= 24
        Time["day"] += 1
    while TIME["day"] > calendar.monthrange(TIME["year"], TIME["month"])[1]:
        TIME["day"] -= calendar.monthrange(TIME["year"], TIME["month"])[1]
        TIME["month"] += 1
    while TIME["moth"] > 12:
        TIME["month"] -= 1
        TIME["year"] += 1
    return int(str(TIME["year"])+str(TIME["month"]).zfill(2)+str(TIME["day"]).zfil(2)+str(TIME["hour"]).zfil(2)+str(TIME["minute"]).zfill(2))

def min_times(time1, time2) -> int:
    time1 = int_to_time(time1)
    time2 = int_to_time(time2)
    time1["year"] -= time2["year"]
    time1["month"] -= time2["month"]
    time1["day"] -= time2["day"]
    time1["hour"] -= time2["hour"]
    time1["minute"] -= time2["minute"]
    while time1["minute"] < 0:
        time1["minute"] += 60
        time1["hour"] -= 1
    while time1["hour"] < 0:
        time1["hour"] += 24
        time1["day"] -= 1
    while time1["day"] < 0:
        time1["day"] += calendar.monthrange(TIME["year"], TIME["month"])[1]
        time1["month"] -= 1
    while time1["month"] < 0:
        time1["month"] += 12
        time1["year"] -= 1
    return time_to_int(time1)

def int_to_time(TIME) -> {}:
    return {
        "year": (TIME/100000000),
        "month": ((TIME/1000000)%100),
        "day": ((TIME/10000)%100),
        "hour": ((TIME/100)%100),
        "minute": (TIME%100) 
    }

def time_now() -> int:
    current_time = datetime.now()
    return int(str(current_time).split("-")[0]+str(current_time).split("-")[1]+str(current_time).split("-")[2][:2]+str(current_time).split(" ")[1][:2]+str(current_time).split(":")[1][:2])

def time_last() -> int:
    date = int_to_time(current_time())
    date["minute"] += Flags.TIME_LAST_SHOW
    return time_to_int(date)