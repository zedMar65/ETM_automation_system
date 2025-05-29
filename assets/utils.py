from database import LoggingDB
import os

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
    print(e)
    try:
        LoggingDB.execute("INSERT INTO logs (user_id, user_ip, message) VALUES(?, ?, ?)", (user, ip, msg))
    except Exception as e:
        print(f"Error while Logging: {e}")