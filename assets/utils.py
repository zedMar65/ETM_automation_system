from database import LoggingDB
import os

def init_log():
    LoggingDB.connect()
    with open(os.environ.get("BUILD_SCRIPT_INTERNAL"), "r") as build_file:
        build_script = build_file.read()
    LoggingDB.execute_script(build_script)
    log("logging Init complete")

def log(msg, user=-1, ip="internal"):
    LoggingDB.execute("INSERT INTO logs (user_id, user_ip, message) VALUES(?, ?, ?)", (user, ip, msg))