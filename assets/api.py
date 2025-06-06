from interface import Available_Events
import json
from utils import *
from users import *

class Fetch:
    def fetch_free_by_find(from_time, to_time, room_id=None, event_id=None, guide_id=None) -> [()]:
        try:
            free_events = []
            if to_time < from_time:
                raise ValueError(Errors.wrong_time)
            events = Available_Events.find(room_id=room_id, event_id=event_id, guide_id=guide_id)
            for event in events:
                availability = Available_Events.get_availability(event[0], from_time, to_time).append(event[0])
                free_events += availability
            return free_events
        except Exception as e:
            log(f"Error while fetching spots by find: {e}")
            return [()]
    def fetch_users() -> [{}]:
        data = Users.find()
        users = {}
        for da in data:
            if len(da) > 0:
                users[str(da[0])] = {"id": da[0], "name": da[1], "email": da[2], "auth": da[3]}
        return users
    

class Process:
    def handle_inquiry(data) -> [()]:
        try:
            option = data["option"]
            free_time = data["free_time"]
            time_frames = data["time_frame"]
            guides = data["guides"]
            events = data["event"]
            rooms = data["room"]

            # fix missing selection data
            for i in range(len(time_frames)):
                # convert time frames from js time to int time
                time_frames[i]["startTime"] = int(str(time_frames[i]["startTime"][:4]+time_frames[i]["startTime"].split("-")[1][:2]+time_frames[i]["startTime"].split("T")[0][8:]+time_frames[i]["startTime"].split("T")[1].split(":")[0]+time_frames[i]["startTime"].split(":")[1]))
                time_frames[i]["endTime"] = int(str(time_frames[i]["endTime"][:4]+time_frames[i]["endTime"].split("-")[1][:2]+time_frames[i]["endTime"].split("T")[0][8:]+time_frames[i]["endTime"].split("T")[1].split(":")[0]+time_frames[i]["endTime"].split(":")[1]))
            if len(time_frames) < 1:
                time_frames[0]["startTime"] = time_now()
                time_frames[0]["endTime"] = time_last()
                time_frames[0]["id"] = 0
            if len(guides) < 1:
                guides[0] = None
            if len(rooms) < 1:
                rooms[0] = None
            if len(events) < 1:
                events[0] = None
            
            possible_events = []
            if free_time:
                # dont ask, the 4 nested loops were neccesery:
                for time_frame in time_frames:
                    for guide in guides:
                        for room in rooms:
                            for event in events:
                                evs = Fetch.fetch_free_by_find(from_time=time_frame["startTime"], to_time=time_frame["endTime"], room_id=room, event_id=event, guide_id=guide)
                                if len(evs) > 0:
                                    if len(evs[0]) > 0:
                                        possible_events += evs
                    
            return possible_events
        except Exception as e:
            log(f"Error while handeling inquiry: {e}")

class Auth:
    def auth_via_pass(mail, passw) -> int:
        return Users.authenticate_user(mail, passw)
    def auth_via_cookie(cookie) -> int:
        return Users.authenticate_cookie(cookie)
    def get_cookie(uuid) -> str:
        return Users.get_cookie(uuid)
    def auth(uuid) -> str:
        return Users.get_auth(uuid)

class Commands:
    def remove_user(uuid) -> int:
        return Users.delete_user(uuid)
    def new_user(data) -> int:
        # print(data)
        id = Users.new_user(data["name"], data["email"], data["password"])
        # print(id)
        if data["auth"] == "guide":
            Guides.assign(id)
        elif data["auth"] == "mod":
            Mods.assign(id)
        elif data["auth"] == "admin":
            Admins.assign(id)
        return 1