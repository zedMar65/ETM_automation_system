from database import LoggingDB, MainDB
import os
from config import Flags
from datetime import datetime
import calendar


def to_dt(s):
    return datetime.strptime(s, "%Y%m%d%H%M")


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
    # print(TIME["day"], "------------------------------------", calendar.monthrange(TIME["year"], TIME["month"])[1])
    while TIME["minute"] >= 60:
        while TIME["hour"] >= 24:
            while TIME["day"] > calendar.monthrange(TIME["year"], TIME["month"])[1]:
                while TIME["month"] > 12:
                    TIME["month"] -= 12
                    TIME["year"] += 1
                TIME["day"] -= calendar.monthrange(TIME["year"], TIME["month"])[1]
                TIME["month"] += 1
            TIME["hour"] -= 24
            TIME["day"] += 1
        TIME["minute"] -= 60
        TIME["hour"] += 1
    while TIME["hour"] >= 24:
        while TIME["day"] > calendar.monthrange(TIME["year"], TIME["month"])[1]:
            while TIME["month"] > 12:
                TIME["month"] -= 12
                TIME["year"] += 1
            TIME["day"] -= calendar.monthrange(TIME["year"], TIME["month"])[1]
            TIME["month"] += 1
        TIME["hour"] -= 24
        TIME["day"] += 1
    while TIME["day"] > calendar.monthrange(TIME["year"], TIME["month"])[1]:
        while TIME["month"] > 12:
            TIME["month"] -= 12
            TIME["year"] += 1
        TIME["day"] -= calendar.monthrange(TIME["year"], TIME["month"])[1]
        TIME["month"] += 1
    while TIME["month"] > 12:
        TIME["month"] -= 12
        TIME["year"] += 1
    
    return int(str(TIME["year"])+str(TIME["month"]).zfill(2)+str(TIME["day"]).zfill(2)+str(TIME["hour"]).zfill(2)+str(TIME["minute"]).zfill(2))
def min_times2(time1, time2) -> int:
    time1 = int_to_time(time1)
    time2 = int_to_time(time2)
    time1["year"] -= time2["year"]
    time1["month"] -= time2["month"]
    time1["day"] -= time2["day"]
    time1["hour"] -= time2["hour"]
    time1["minute"] -= time2["minute"]
    
    while time1["minute"] < 0:
        while time1["hour"] < 0:
            time1["hour"] += 24
            time1["day"] -= 1
        time1["minute"] += 60
        time1["hour"] -= 1
    while time1["hour"] < 0:
        time1["hour"] += 24
        time1["day"] -= 1
    return int(str(time1["year"])+str(time1["month"]).zfill(2)+str(time1["day"]).zfill(2)+str(time1["hour"]).zfill(2)+str(time1["minute"]).zfill(2))
def min_times(time1, time2) -> int:
    time1 = int_to_time(time1)
    time2 = int_to_time(time2)
    time1["year"] -= time2["year"]
    time1["month"] -= time2["month"]
    time1["day"] -= time2["day"]
    time1["hour"] -= time2["hour"]
    time1["minute"] -= time2["minute"]
    
    while time1["minute"] < 0:
        while time1["hour"] < 0:
            while time1["day"] <= 0:
                while time1["month"] <= 0:
                    time1["month"] += 12
                    time1["year"] -= 1
                time1["day"] += calendar.monthrange(time1["year"], time1["month"])[1]
                time1["month"] -= 1
            time1["hour"] += 24
            time1["day"] -= 1
        time1["minute"] += 60
        time1["hour"] -= 1
    while time1["hour"] < 0:
        while time1["day"] <= 0:
            while time1["month"] <= 0:
                time1["month"] += 12
                time1["year"] -= 1
            time1["day"] += calendar.monthrange(time1["year"], time1["month"])[1]
            time1["month"] -= 1
        time1["hour"] += 24
        time1["day"] -= 1
    while time1["day"] <= 0:
        while time1["month"] <= 0:
            time1["month"] += 12
            time1["year"] -= 1
        time1["day"] += calendar.monthrange(time1["year"], time1["month"])[1]
        time1["month"] -= 1     
    while time1["month"] <= 0:
        time1["month"] += 12
        time1["year"] -= 1
    return time_to_int(time1)

def add_times(time1, time2) -> int:
    time1 = int_to_time(time1)
    time2 = int_to_time(time2)
    time1["year"] += time2["year"]
    time1["month"] += time2["month"]
    time1["day"] += time2["day"]
    time1["hour"] += time2["hour"]
    time1["minute"] += time2["minute"]
    return time_to_int(time1)

def int_to_time(TIME) -> {}:
    TIME = int(TIME)
    return {
        "year": int(TIME/100000000),
        "month": int((TIME/1000000)%100),
        "day": int((TIME/10000)%100),
        "hour": int((TIME/100)%100),
        "minute": int(TIME%100) 
    }

def time_now() -> int:
    current_time = datetime.now()
    return int(str(current_time).split("-")[0]+str(current_time).split("-")[1]+str(current_time).split("-")[2][:2]+str(current_time).split(" ")[1][:2]+str(current_time).split(":")[1][:2])

def time_last() -> int:
    time = int_to_time(time)
    time["hours"] = int(Flags.TIME_LAST_SHOW[:2])
    time["minutes"] = int(Flags.TIME_LAST_SHOW[2:])
    return time_to_int(time)
def time_first(time) -> int:
    time = int_to_time(time)
    time["hours"] = int(Flags.TIME_FIRST_SHOW[:2])
    time["minutes"] = int(Flags.TIME_FIRST_SHOW[2:])
    return time_to_int(time)

def name_to_int(day):
    weekday_to_number = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
    }
    return weekday_to_number[day]