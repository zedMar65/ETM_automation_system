from utils import log
from database import MainDB
import os, uuid, secrets
from abc import ABC, abstractmethod

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
class Users:
    @classmethod
    def new_user(self, user_name, user_mail, user_pass) -> int:
        try:
            if(len(self.find(user_name = user_name)) > 0 or len(self.find(user_mail = user_mail)) > 0):
                log(f"Failed to create user, mail or name already exists")
                return 0
            user_salt = str(uuid.UUID(bytes=secrets.token_bytes(16)))
            pass_hash = hash(user_pass+user_salt)
            cookie = user_mail + str(uuid.UUID(bytes=secrets.token_bytes(16)))
            user_id = MainDB.execute("INSERT INTO users (user_name, user_mail, user_auth, user_pass_hash, user_salt, cookie) VALUES(?, ?, ?, ?, ?, ?)", (user_name, user_mail, "user", pass_hash, user_salt, cookie))
            log(f"Created user: {user_id}")
            return user_id
        except Exception as e:
            log(f"Error while creating user[{user_name}]: {e}")
            return -1
    
    @classmethod
    def find(self, user_id = None, user_name = None, user_mail = None, user_cookie = None, user_auth = None) -> [()]:
        args_all = [user_id, user_name, user_mail, user_cookie, user_auth]
        # I know this implementation is trash, but is there a better one really?
        # also if the database table users collumn names change, these have to also be reasigned
        arg_names = {
            0: "user_id = ?",
            1: "user_name = ?",
            2: "user_mail = ?",
            3: "cookie = ?",
            4: "user_auth = ?"
        }
        try:
            placeholder = ""
            values = ()
            num = 0
            for arg in args_all:
                if arg != None:
                    if placeholder != "":
                        placeholder += ", "
                    placeholder += arg_names[num]
                    values = values + (arg,)
                num += 1

            return MainDB.query(f"SELECT * FROM users WHERE {placeholder}", values)
        except Exception as e:
            log(f"Error while querrying for user {args_all}")
            return [()]
        
    @classmethod
    def authenticate_user(self, user_mail, user_pass) -> int:
        try:
            data = MainDB.query("SELECT user_id, user_pass_hash, user_salt FROM users WHERE user_mail = ?", (user_mail,))
            if len(data) > 1:
                log(f"User authenticate find returned to many users, user_mail: {user_mail}")
                return -1
            elif len(data) < 1:
                log(f"No user with mail {user_mail} found, while authenticating")
                return 0
            (user_id, user_hash, user_salt) = data[0]
            if str(hash(user_pass+user_salt)) == user_hash:
                log(f"Authentication of user {user_id} sucessfull")
                return user_id
            log(f"Failed to authenticate user [{user_mail}]")
            return 0
        except Exception as e:
            log(f"Error while authenticating user: {e}")
            return -1
    
    @classmethod
    def get_auth(self, user_id) -> str:
        try:
            data = self.find(user_id = user_id)
            if len(data) > 1:
                log(f"User auth find returned to many users for user [{user_id}]")
                return ""
            elif len(data) < 1:
                log(f"No user {user_id} found, while querrying for auth")
                return ""
            return data[0][3]
        except Exception as e:
            log(f"Error while finding auth of {user_id}")
            return ""

    @classmethod
    def update_user(self, user_id, new_name = None, new_mail = None, new_pass = None, new_cookie = None, new_auth = None)->int:
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
            log(f"Updated user: {user_id}")
            return 1
        except Exception as e:
            log(f"Error while updating user[{user_id}]: {e}")
            return -1

    @classmethod
    def delete_user(self, user_id) -> int:
        try:
            if len(self.find(user_id = user_id)) <= 0:
                log(f"No user [{user_id}] found to delete")
                return 0
            auth = self.get_auth(user_id)
            if auth == "guide":
                Guides.remove(Guides.get_group_id(user_id))
            elif auth == "admin":
                Admins.remove(Admins.get_group_id(user_id))
            elif auth == "mod":
                Mods.remove(Mods.get_group_id(user_id))
            MainDB.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            log(f"Deleted user: {user_id}")
            return 1
        except Exception as e:
            log(f"Error while deleting user: {e}")
            return -1
    
    @classmethod
    def authenticate_cookie(self, cookie) -> int:
        try:
            data = MainDB.query("SELECT user_id FROM users WHERE cookie = ?", (cookie,))
            if len(data) > 1:
                log(f"Multiple users detected with cookie [{cookie}] while authenticating")
                return -1
            if len(data) < 1:
                log(f"User cookie auth not found [{cookie}]")
                return 0
            return data[0][0]
        except Exception as e:
            log(f"Error while trying to authenticate cookie [{cookie}]: {e}")
            return -1

    @classmethod
    def get_cookie(self, user_id) -> str:
        try:
            user = self.find(user_id=user_id)
            if len(user) > 1:
                log(f"Multiple users detected with user_id [{user_id}] while querrying for cookie")
                return ""
            if len(user) < 1:
                log(f"No user [{uset_id}] found while querrying for cookie")
                return ""
            log(f"Found cookie [{user[0][6]}] for user [{user_id}]")
            return user[0][6]
        except Exception as e:
            log(f"Error while finding a cookie for user [{user_id}]")
            return ""

class Group(ABC):
    @classmethod
    def assign(self, user_id) -> int:
        try:
            user_auth = Users.get_auth(user_id)
            if user_auth == "admin":
                Admins.remove(Admins.get_group_id(user_id))
            elif user_auth == "mod":
                Mods.remove(Mods.get_group_id(user_id))
            elif user_auth == "guide":
                Guides.remove(Guides.get_group_id(user_id))
            Users.update_user(user_id, new_auth = self.get_auth())
            guide_id = MainDB.execute(f"INSERT INTO {self.get_table()} (user_id) VALUES(?)", (user_id,))
            log(f"Assigned user {user_id}, to {self.get_auth()}")
            return guide_id
        except Exception as e:
            log(f"Error while creating guide[{user_id}]: {e}")
            return -1
    
    @classmethod
    def update(self, group_id, new_user_id=None) -> int:
        try:
            if new_user_id != None:
                MainDB.execute(f"UPDATE {self.get_table()} SET user_id = ? WHERE {self.get_auth()}_id = ?", (new_user_id, group_id))
            log(f"Updated group user {group_id}")
            return 1
        except Exception as e:
            log(f"Error while updating {self.get_auth()}, [{group_id}]: {e}")
            return -1

    @classmethod
    def remove(self, group_id) -> int:
        try:
            MainDB.execute(f"DELETE FROM {self.get_table()} WHERE {self.get_auth()}_id = ?", (group_id,))
            log(f"Deleted {self.get_auth}: {group_id}")
            return 1
        except Exception as e:
            log(f"Error while deleting {self.get_group()} [{group_id}]: {e}")
            return -1
    
    @classmethod
    def get_group_id(self, user_id) -> int:
        try:
            data =  MainDB.query(f"SELECT {self.get_auth()}_id FROM {self.get_table()} WHERE user_id = ?", (user_id,))
            if len(data) == 1:
                log(f"Retrieved user's [{user_id}] {self.get_auth()}_id")
                return data[0][0]
            log(f"Failed querry for user's [{user_id}] {self.get_auth()}_id")
            return 0
        except Exception as e:
            return -1
            log(f"Error while retrieving {user_id} {self.get_auth()}_id: {e}")

    @classmethod
    def get_user_id(self, group_id) -> int:
        try:
            data = MainDB.query(f"SELECT user_id FROM {self.get_table()} WHERE {self.get_auth()}_id = ?", (group_id,))
            if len(data) == 1:
                log(f"Retrieved {self.get_auth()} user's [{group_id}] user_id")                
                return data[0][0]
            log(f"Failed querry for {self.get_auth()} user's [{group_id}] user_id")
            return 0
        except Exception as e:
            log(f"Error while retrieving {self.get_auth()} [{group_id}] user_id: {e}")
            return -1

    @classmethod
    @abstractmethod
    def get_auth(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_table(self) -> str:
        pass

class Admins(Group):
    @classmethod
    def get_auth(self) -> str:
        return "admin"
    @classmethod
    def get_table(self) -> str:
        return "admins"

class Mods(Group):
    @classmethod
    def get_auth(self) -> str:
        return "mod"
    @classmethod
    def get_table(self) -> str:
        return "mods"

class Guides(Group):
    @classmethod
    def get_auth(self) -> str:
        return "guide"
    @classmethod
    def get_table(self) -> str:
        return "guides"
    
    @classmethod
    def occupie(self, guide_id, start_time, end_time, reason="Užimtas") -> int:
        try:
            id = MainDB.execute("INSERT INTO guide_occupation (guide_id, busy_from, busy_to, reason) VALUES(?, ?, ?, ?)", (guide_id, start_time, end_time, reason))
            log(f"Added busy details for id [{id}]")
            return id 
        except Exception as e:
            log(f"Error while trying to occupie guide [{guide_id}]: {e}")
            return -1

    @classmethod
    def change_occ_time(id, new_start_time = None, new_end_time = None) -> int:
        try:
            data = MainDB.query("SELECT * FROM guide_occupation WHERE id = ?", (id,))
            if len(data) < 1:
                log(f"No guide occupation with id [{id}] found")
                return -2
            if new_start_time == None:
                new_start_time = data[0][2]
            if new_end_time == None:
                new_start_time = data[0][3]
            MainDB.execute("UPDATE guide_occupation SET busy_from = ?, busy_to = ? WHERE id = ?", (new_start_time, new_end_time, id))
            return 1
        except Exception as e:
            log(f"Error while changing time for guide occ [{id}]: {e}")
            return -1
    
    @classmethod 
    def get_occupation_by_id(id) -> [()]:
        try:
            data = MainDB.query("SELECT * FROM guide_occupation WHERE id = ?", (id,))
            if len(data) < 1:
                log(f"No guide occupation with id [{id}] found")
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting occupation guide [{id}]: {e}")
            return [()]

    @classmethod
    def get_occupation_by_guide(guide_id) -> [()]:
        try:
            data = MainDB.query("SELECT * FROM guide_occupation WHERE guide_id = ?", (guide_id,))
            if len(data) < 1:
                log(f"No guide occupation with for [{guide_id}] found")
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting occupation for guide [{guide_id}]: {e}")
            return [()]
    
    @classmethod
    def free(self, id) -> int:
        try:
            data = MainDB.query("SELECT * FROM guide_occupation WHERE id = ?", (id,))
            if len(data) < 1:
                log(f"No guide occupation with id [{id}] found")
                return -2
            MainDB.execute("DELETE FROM guide_occupation WHERE id = ?", (id,))
            return 1
        except Exception as e:
            log(f"Error while freeing guide [{id}]: {e}")
            return -1

class Events:
    @classmethod
    def get_id(self, event_name) -> int:
        try:
            data = MainDB.query("SELECT event_id FROM events WHERE event_name = ?", (event_name))
            if len(data) > 1:
                log(f"Too many events associated with name [{event_name}]")
                return -2
            if len(data) < 1:
                log(f"No events found for event [{event_name}]")
                return 0
            log(f"Event id [{data[0][0]}] found for [{event_name}]")
            return data[0][0]
        except Exception as e:
            log(f"Error while finding id of event [{event_name}]")
            return -1
    
    @classmethod
    def new_event(self, event_name) -> int:
        try:
            if self.get_id(event_name) < 1:
                log(f"Event with name [{event_name}] already exists")
                return 0
            event_id = MainDB.execute("INSERT INTO events (event_name) VALUES(?)", (event_name,))
            log(f"Created event [{event_id}]")
            return event_id
        except Exception as e:
            log(f"Error while creating new event [{event_name}]: {e}")
    
    @classmethod
    def get_name(self, event_id) -> str:
        try:
            data = MainDB.query("SELECT event_name FROM events WHERE event_id = ?", (event_id))
            if len(data) > 1:
                log(f"Too many events associated with id [{event_id}]")
                return ""
            if len(data) < 1:
                log(f"No events found for event [{event_id}]")
                return ""
            log(f"Event name [{data[0][1]}] found for [{event_id}]")
            return data[0][1]
        except Exception as e:
            log(f"Error while finding name of event [{event_id}]")
            return ""
    
    @classmethod
    def delete_event(self, event_id) -> int:
        try:
            if self.get_name(event_id) == "":
                log(f"No event with id [{event_id}] found to delete")
                return 0
            MainDB.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
            log(f"Removed event [{event_id}]")
            return 1
        except Exception as e:
            log(f"Error while deleting event [{event_id}]: {e}")
            return -1

    @classmethod
    def rename(self, event_id, new_name) -> int:
        try:
            if self.get_name(event_id) == "":
                log(f"No event with id [{event_id}] found to rename")
                return 0
            MainDB.execute("UPDATE events SET event_name = ? WHERE event_id = ?", (new_name, event_id))
            log(f"Renamed event [{event_id}]")
            return 1
        except Exception as e:
            log(f"Error while renaming event [{event_id}]: {e}")
            return -1

class Rooms:
    @classmethod
    def get_id(self, room_name) -> int:
        try:
            data = MainDB.query("SELECT room_id FROM rooms WHERE room_name = ?", (room_name))
            if len(data) > 1:
                log(f"Too many rooms associated with name [{room_name}]")
                return -2
            if len(data) < 1:
                log(f"No rooms found for room [{room_name}]")
                return 0
            log(f"Room id [{data[0][0]}] found for [{room_name}]")
            return data[0][0]
        except Exception as e:
            log(f"Error while finding id of room [{room_name}]")
            return -1
    
    @classmethod
    def new_room(self, room_name, capacity) -> int:
        try:
            if self.get_id(room_name) < 1:
                log(f"room with name [{room_name}] already exists")
                return 0
            room_id = MainDB.execute("INSERT INTO rooms (room_name, capacity) VALUES(?, ?)", (room_name, capacity))
            log(f"Created room [{room_id}]")
            return room_id
        except Exception as e:
            log(f"Error while creating new room [{room_name}]: {e}")
    
    @classmethod
    def get_name(self, room_id) -> str:
        try:
            data = MainDB.query("SELECT room_name FROM rooms WHERE room_id = ?", (room_id))
            if len(data) > 1:
                log(f"Too many rooms associated with id [{room_id}]")
                return ""
            if len(data) < 1:
                log(f"No rooms found for room [{room_id}]")
                return ""
            log(f"room name [{data[0][1]}] found for [{room_id}]")
            return data[0][1]
        except Exception as e:
            log(f"Error while finding name of room [{room_id}]")
            return ""
    
    @classmethod
    def delete_room(self, room_id) -> int:
        try:
            if self.get_name(room_id) == "":
                log(f"No room with id [{room_id}] found to delete")
                return 0
            MainDB.execute("DELETE FROM rooms WHERE room_id = ?", (room_id,))
            log(f"Removed room [{room_id}]")
            return 1
        except Exception as e:
            log(f"Error while deleting room [{room_id}]: {e}")
            return -1

    @classmethod
    def rename(self, room_id, new_name) -> int:
        try:
            if self.get_name(room_id) == "":
                log(f"No room with id [{room_id}] found to rename")
                return 0
            MainDB.execute("UPDATE rooms SET room_name = ? WHERE room_id = ?", (new_name, room_id))
            log(f"Renamed room [{room_id}]")
            return 1
        except Exception as e:
            log(f"Error while renaming room [{room_id}]: {e}")
            return -1
    
    @classmethod
    def change_capacity(self, room_id, new_capacity) -> int:
        try:
            if self.get_name(room_id) == "":
                log(f"No room with id [{room_id}] found to change capacity")
                return 0
            MainDB.execute("UPDATE rooms SET capacity = ? WHERE room_id = ?", (new_capacity, room_id))
            log(f"Changed capacity of room [{room_id}]")
            return 1
        except Exception as e:
            log(f"Error while changing capacity of room [{room_id}]: {e}")
            return -1
    
    @classmethod
    def get_capacity(self, room_id) -> int:
        try:
            data = MainDB.query("SELECT capacity FROM rooms WHERE room_id = ?", (room_id))
            if len(data) > 1:
                log(f"Too many rooms associated with id [{room_id}]")
                return -2
            if len(data) < 1:
                log(f"No rooms found for room [{room_id}]")
                return 0
            log(f"Room capacity [{data[0][2]}] found for [{room_id}]")
            return data[0][2]
        except Exception as e:
            log(f"Error while finding capacity of room [{room_id}]")
            return -1

    @classmethod
    def occupie(self, room_id, start_time, end_time, reason="Užimtas") -> int:
        try:
            id = MainDB.execute("INSERT INTO room_occupation (room_id, busy_from, busy_to, reason) VALUES(?, ?, ?, ?)", (room_id, start_time, end_time, reason))
            log(f"Added busy details for id [{id}]")
            return id 
        except Exception as e:
            log(f"Error while trying to occupie room [{room_id}]: {e}")
            return -1

    @classmethod
    def change_occ_time(id, new_start_time = None, new_end_time = None) -> int:
        try:
            data = MainDB.query("SELECT * FROM room_occupation WHERE id = ?", (id,))
            if len(data) < 1:
                log(f"No room occupation with id [{id}] found")
                return -2
            if new_start_time == None:
                new_start_time = data[0][2]
            if new_end_time == None:
                new_start_time = data[0][3]
            MainDB.execute("UPDATE room_occupation SET busy_from = ?, busy_to = ? WHERE id = ?", (new_start_time, new_end_time, id))
            return 1
        except Exception as e:
            log(f"Error while changing time for room occ [{id}]: {e}")
            return -1
    
    @classmethod 
    def get_occupation_by_id(id) -> [()]:
        try:
            data = MainDB.query("SELECT * FROM room_occupation WHERE id = ?", (id,))
            if len(data) < 1:
                log(f"No room occupation with id [{id}] found")
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting occupation room [{id}]: {e}")
            return [()]

    @classmethod
    def get_occupation_by_room(room_id) -> [()]:
        try:
            data = MainDB.query("SELECT * FROM room_occupation WHERE room_id = ?", (room_id,))
            if len(data) < 1:
                log(f"No room occupation with for [{room_id}] found")
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting occupation for room [{room_id}]: {e}")
            return [()]
    
    @classmethod
    def free(self, id) -> int:
        try:
            data = MainDB.query("SELECT * FROM room_occupation WHERE id = ?", (id,))
            if len(data) < 1:
                log(f"No room occupation with id [{id}] found")
                return -2
            MainDB.execute("DELETE FROM room_occupation WHERE id = ?", (id,))
            return 1
        except Exception as e:
            log(f"Error while freeing room [{id}]: {e}")
            return -1

class Event_Guide_Relation:
    @classmethod
    def check_relation(self, event_id, guide_id) -> int:
        try:
            data = MainDB.query("SELECT * FROM event_guide_relation WHERE event_id = ?, guide_id = ?", (event_id, guide_id))
            if len(data) < 1:
                log(f"Relation {event_id}-{guide_id} not found")
                return 0
            return 1
        except Exception as e:
            log(f"Error while checking relation of {event_id}-{guide_id}")
            return -1

    @classmethod
    def get_guides(self, event_id) -> [()]:
        try:
            data = MainDB.query("SELECT guide_id FROM event_guide_relation WHERE event_id = ?", (event_id,))
            if len(data) < 1:
                log(f"No guides for event [{event_id}] found")
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting guides for event [{event_id}]")
            return [()]

    @classmethod
    def get_events(self, guide_id) -> [()]:
        try:
            data = MainDB.query("SELECT event_id FROM event_guide_relation WHERE guide_id = ?", (guide_id,))
            if len(data) < 1:
                log(f"No events for guide [{guide_id}] found")
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting events for guide [{guide_id}]")
            return [()]

    @classmethod
    def add_relation(self, event_id, guide_id) -> 1:
        try:
            if self.check_relation(event_id, guide_id) > 0:
                log(f"Relation between [{event_id}]-[{guide_id}] already exists")
                return 0
            MainDB.execute("INSERT INTO event_guide_relation (event_id, guide_id) VALUES()")
            return 1
        except Exception as e:
            log(f"Error while adding guide relation between [{event_id}]-[{guide_id}]")
            return -1
    
    @classmethod
    def remove_relation(self, event_id, guide_id):
        try:
            if self.check_relation(event_id, guide_id) < 1:
                log(f"No relation found to remove")
                return 0
            MainDB.execute("DELETE FROM event_guide_relation WHERE event_id = ?, guide_id = ?", (event_id, guide_id))
            log(f"Removed relation between guide [{guide_id}] and event [{event_id}]")
            return 1
        except Exception as e:
            log(f"Error while removing relation: {e}")
            return -1

class Event_Room_Relation:
    @classmethod
    def check_relation(self, event_id, room_id) -> int:
        try:
            data = MainDB.query("SELECT * FROM room_event_relation WHERE event_id = ?, room_id = ?", (event_id, room_id))
            if len(data) < 1:
                log(f"Relation {event_id}-{room_id} not found")
                return 0
            return 1
        except Exception as e:
            log(f"Error while checking relation of {event_id}-{room_id}")
            return -1

    @classmethod
    def get_rooms(self, event_id) -> [()]:
        try:
            data = MainDB.query("SELECT room_id FROM room_event_relation WHERE event_id = ?", (event_id,))
            if len(data) < 1:
                log(f"No rooms for event [{event_id}] found")
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting rooms for event [{event_id}]")
            return [()]

    @classmethod
    def get_events(self, room_id) -> [()]:
        try:
            data = MainDB.query("SELECT event_id FROM room_event_relation WHERE room_id = ?", (room_id,))
            if len(data) < 1:
                log(f"No events for room [{room_id}] found")
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting events for room [{room_id}]")
            return [()]

    @classmethod
    def add_relation(self, event_id, room_id) -> 1:
        try:
            if self.check_relation(event_id, room_id) > 0:
                log(f"Relation between [{event_id}]-[{room_id}] already exists")
                return 0
            MainDB.execute("INSERT INTO room_event_relation (event_id, room_id) VALUES()")
            return 1
        except Exception as e:
            log(f"Error while adding room relation between [{event_id}]-[{room_id}]")
            return -1
    
    @classmethod
    def remove_relation(self, event_id, room_id):
        try:
            if self.check_relation(event_id, room_id) < 1:
                log(f"No relation found to remove")
                return 0
            MainDB.execute("DELETE FROM room_event_relation WHERE event_id = ?, room_id = ?", (event_id, room_id))
            log(f"Removed relation between room [{room_id}] and event [{event_id}]")
            return 1
        except Exception as e:
            log(f"Error while removing relation: {e}")
            return -1

class Available_Events:
    @classmethod
    def find(self, id = None, event_id = None, room_id = None, guide_id = None) -> [()]:
        try:
            placeholder = ""
            values = ()
            if id != None:
                placeholder += "available_event_id = ?"
                values = values + (id,)
            if event_id != None:
                if placeholder != "":
                    placeholder += ", "
                placeholder += "event_id = ?"
                values = values + (event_id)
            if room_id != None:
                if placeholder != "":
                    placeholder += ", "
                placeholder += "room_id = ?"
                values = values + (room_id)
            if guide_id != None:
                if placeholder != "":
                    placeholder += ", "
                placeholder += "guide_id = ?"
                values = values + (guide_id)
            data = MainDB.query(f"SELECT * FROM available_events WHERE {placeholder}", values)
            log(f"Found {len(data)} available events")
            return data
        except Exception as e:
            log(f"Error while finding available event: {e}")
            return [()]

    @classmethod
    def new(self, event_id, room_id, guide_id) -> int:
        try:
            if len(self.find(event_id=event_id, room_id=room_id, guide_id=guide_id)) > 0:
                log(f"Duplicate available event found while adding new")
                return 0
            event_id = MainDB.execute("INSERT INTO available_events (even_id, room_id, guide_id) VALUES(?, ?, ?)", (event_id, room_id, guide_id))
            log(f"Made new available event [{event_id}]")
            return event_id
        except Exception as e:
            log(f"Error while adding new available event: {e}")
            return -1

    @classmethod
    def remove(self, id) -> int:
        try:
            if len(self.find(id=id)) < 1:
                log(f"No available event found to remove for [{id}]")
                return 0
            MainDB.execute("DELETE FROM available_events WHERE available_event_id = ?", (id,))
            log(f"Removed available_event: {id}")
            return 1
        except Exception as e:
            log(f"Error while removing available event {id}: {e}")
            return -1

class Occupied_Events:
    @classmethod
    def find(self, id = None, guide_oc_id = None, room_oc_id = None) -> [()]:
        try:
            placeholder = ""
            values = ()
            if id != None:
                placeholder += "available_event_id = ?"
                values = values + (id,)
            if event_id != None:
                if placeholder != "":
                    placeholder += ", "
                placeholder += "event_id = ?"
                values = values + (event_id)
            if room_id != None:
                if placeholder != "":
                    placeholder += ", "
                placeholder += "room_id = ?"
                values = values + (room_id)
            if guide_id != None:
                if placeholder != "":
                    placeholder += ", "
                placeholder += "guide_id = ?"
                values = values + (guide_id)
            data = MainDB.query(f"SELECT * FROM available_events WHERE {placeholder}", values)
            log(f"Found {len(data)} available events")
            return data
        except Exception as e:
            log(f"Error while finding available event: {e}")
            return [()]

















