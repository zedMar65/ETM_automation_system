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
        return 1
        log("MainDB init complete")
    except Exception as e:
        log(f"Error while Initing MainDB: {e}")
        return -1
class Users:
    @classmethod
    def new_user(self, user_name, user_mail, user_pass) -> int:
        try:
            user_salt = str(uuid.UUID(bytes=secrets.token_bytes(16)))
            pass_hash = hash(user_pass+user_salt)
            cookie = user_mail + str(uuid.UUID(bytes=secrets.token_bytes(16)))
            user_id = MainDB.execute("INSERT INTO users (user_name, user_mail, user_auth, user_pass_hash user_salt, cookie) VALUES(?, ?, ?, ?, ?, ?)", (user_name, user_mail, "user", user_hash, user_salt, cookie))
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
            data = MainDB.query("SELECT user_id, user_pass_hash, user_salt FROM users WHERE user_mail = ?", (user_mail))
            if len(data) > 1:
                log(f"User authenticate find returned to many users, user_mail: {user_mail}")
                return -1
            elif len(data) < 1:
                log(f"No user with mail {user_mail} found, while authenticating")
                return 0;
            (user_id, user_hash, user_salt) = data[0]
            if hash(user_pass+user_salt) == user_hash:
                log(f"Authentication of user {user_id} sucessfull")
                return 1
            return 0
        except Exception as e:
            log(f"Error while authenticating user: {e}")
            return -1
    
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
            MainDB.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            log(f"Deleted user: {user_id}")
            return 1
        except Exception as e:
            log("Error while deleting user: {e}")
            return -1

class Group(ABC):
    @classmethod
    def assign(self, user_id) -> int:
        try:
            Users.update_user(user_id, new_auth = self.get_auth())
            guide_id = MainDB.execute(f"INSERT INTO {self.get_table} (user_id) VALUES(?)", (user_id,))
            log(f"Assigned user {user_id}, to {self.get_auth()}")
            return guide_id
        except Exception as e:
            log(f"Error while creating guide[{user_id}]: {e}")
            return -1
    
    @classmethod
    def update(self, group_id, new_user_id=None) -> int:
        try:
            if new_user_id != None:
                MainDB.execute(f"UPDATE {self.get_table()} SET user_id = ? WHERE {self.get_auth}_id = ?", (new_user_id, group_id))
            log(f"Updated group user {group_id}")
            return 1
        except Exception as e:
            log(f"Error while updating {self.get_auth}, [{group_id}]: {e}")
            return -1

    @classmethod
    def remove(self, group_id) -> int:
        try:
            MainDB.execute(f"DELETE FROM {self.get_table()} WHERE {self.get_auth}_id = ?", (group_id,))
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
                log(f"Retrieved {self.get_auth()} user's [{user_id}] user_id")                
                return data[0][0]
            log(f"Failed querry for {self.get_auth()} user's [{group_id}] user_id")
            return 0
        except Exception as e:
            return -1
            log(f"Error while retrieving {self.get_auth()} [{group_id}] user_id: {e}")
    
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
    def get_table(self) -> str:
        return "admins"

class Mods(Group):
    @classmethod
    def get_auth(self) -> str:
        return "mod"
    def get_table(self) -> str:
        return "mods"

class Guides(Group):
    @classmethod
    def get_auth(self) -> str:
        return "guide"
    def get_table(self) -> str:
        return "guides"