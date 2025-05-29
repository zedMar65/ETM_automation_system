from utils import log
from database import MainDB
import os

def init_MainDB():
    try:
        MainDB.connect()
        with open(os.environ.get("BUILD_SCRIPT_TIMELINES"), "r") as build_file:
            build_script = build_file.read()
        MainDB.execute_script(build_script)
        log("MainDB init complete")
    except Exception as e:
        log(f"Error while Initing MainDB: {e}")

class Guide:
    @classmethod
    def make_guide(user_id, event_ids) -> bool:
        try:
            MainDB.execute("INSERT INTO guides (user_id) VALUES(?)", (user_id))
            MainDB.execute("UPDATE users SET user_auth = ? WHERE user_id = ?", ("guide", user_id))
            guide_id = MainDB._cursor.lastrowid
            for event_id in event_ids:
                MainDB.execute(
                    "INSERT INTO event_guides (guide_id, event_id) VALUES(?, ?)", 
                    (guide_id, event_id))
            log(f"Added guide: {guide_id}")
            return True
        except Exception as e:
            log(f"Errorh while adding guide: {e}")
            return False
    
    @classmethod
    def mod_guide(guide_id, new_event_ids = None, new_user_id = None):
        try:
            if new_event_ids != None:
                placeholders = ",".join("?" for _ in new_event_ids)
                MainDB.execute(f"DELETE FROM event_guides WHERE guide_id = ? AND id NOT IN ({placeholders})", (guide_id, *new_event_ids))
                for event_id in new_event_ids:
                    MainDB.execute("INSER INTO event_guides (guide_id, event_id) VALUES(?, ?) ON CONFLICT((event_id, guide_id)) DO NOTHING", (guide_id, event_id))
                log(f"Modded guide: {guide_id}")
            if new_user_id != None:
                MainDB.execute("UPDATE guides SET user_id = ? WHERE guide_id = ?", (new_user_id, guide_id))
            return True
        except Exception as e:
            log(f"Error while modding guide: {e}")
            return False

    @classmethod
    def remove_guide(guide_id) -> bool:
        try:
            user_id = MainDB.execute("SELECT user_id FROM guides WHERE guide_id = ?", (guide_id))
            MainDB.execute("DELETE FROM guides WHERE guide_id = ?", (guide_id))
            MainDB.execute("DELETE FROM event_guides WHERE guide_id = ?", (guide_id))
            MainDB.execute("UPDATE users SET user_auth = ? WHERE user_id = ?", ("user", user_id))
            log(f"Removed guide: {guide_id}")
            return True
        except Exception as e:
            log("Error while removing guide: {e}")
            return False