from utils import log
from database import MainDB
import os
import uuid, M2Crypto

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
            log(f"Error while adding guide: {e}")
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
            log(f"Modified guide: {guide_id}")
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

class User:
    @classmethod
    def new_user(user_name, user_mail, user_pass) -> bool:
        try:
            cookie = user_mail + str(uuid.UUID(bytes = M2Crypto.m2.rand_bytes(num_bytes)))
            MainDB.execute("INSERT INTO users (user_name, user_mail, user_auth, user_pass, cookie) VALUES(?, ?, ?, ?, ?)", (user_name, user_mail, "user", user_pass, cookie))
            log(f"Created user: {user_name}")
            return True
        except Exception as e:
            log(f"Errorh while creating user[{user_name}]: {e}")
            return False
    
    @classmethod
    def update_user(user_id, new_name = None, new_mail = None, new_pass = None, new_cookie = None, new_auth = None):
        try:
            if new_name != None:
                MainDB.execute("UPDATE users SET user_name = ? WHERE user_id = ?", (new_name, user_id))
            if new_mail != None:
                MainDB.execute("UPDATE users SET user_mail = ? WHERE user_id = ?", (new_mail, user_id))
            if new_pass != None:
                MainDB.execute("UPDATE users SET user_pass = ? WHERE user_id = ?", (new_pass, user_id))
            if new_cookie != None:
                MainDB.execute("UPDATE users SET cookie = ? WHERE user_id = ?", (new_cookie, user_id))
            if new_auth != None:
                MainDB.execute("UPDATE users SET user_auth = ? WHERE user_id = ?", (new_auth, user_id))
            return True
        except Exception as e:
            log(f"Error while updating user[{user_id}]: {e}")
            return False

    @classmethod
    def remove_guide(guide_id) -> bool:
        try:
            MainDB.execute("DELETE ")
            log(f"Removed guide: {guide_id}")
            return True
        except Exception as e:
            log("Error while removing guide: {e}")
            return False
