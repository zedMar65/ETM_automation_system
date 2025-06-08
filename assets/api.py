from interface import Available_Events
import json
from utils import *
from users import *
from interface import *
import time
from datetime import datetime, date

class Utility:
    def update(certain_date):
        try:
            guides = Users.find(user_auth="guide")
            for guide in guides:
                guide_id = Guides.get_group_id(guide[0])
                time_in_time = int_to_time(certain_date)
                print(int_to_time(certain_date))
                day_number = date(int_to_time(certain_date)["year"], int_to_time(certain_date)["month"], int_to_time(certain_date)["day"]).weekday()
                guide_work_hours = WorkHours.find(guide_id=guide_id, week_day=day_number+1)
                if len(guide_work_hours) > 0:
                    if len(guide_work_hours[0]) > 0:
                        start_time = time_in_time
                        end_time = time_in_time
                        if guide_work_hours[0][3] > Flags.TIME_FIRST_SHOW:
                            start_time["hour"] = int(str(Flags.TIME_FIRST_SHOW)[:2])
                            start_time["minute"] = int(str(Flags.TIME_FIRST_SHOW)[2:])
                            end_time["hour"] = int(str(guide_work_hours[0][3])[:2])
                            end_time["minute"] = int(str(guide_work_hours[0][3])[:2])
                        elif guide_work_hours[0][4] < Flags.TIME_LAST_SHOW:
                            start_time["hour"] = int(str(guide_work_hours[0][4])[:2])
                            start_time["minute"] = int(str(guide_work_hours[0][4])[:2])
                            end_time["hour"] = int(str(Flags.TIME_LAST_SHOW)[:2])
                            end_time["minute"] = int(str(Flags.TIME_LAST_SHOW)[2:])
                        elif guide_work_hours[0][4] == Flags.TIME_LAST_SHOW and guide_work_hours[0][3] == Flags.TIME_FIRST_SHOW:
                            pass
                        else:
                            raise ValueError("Wrong tiime frames used")
                        Guides.occupie(guide_id, time_to_int(start_time), time_to_int(end_time), "Off work")
                        return 1
                    
                return 0
        except Exception as e:
            log(f"Error while doing Utility update: {e}")
            return 0
    def full_update(month):
        if month == 0:
            day = int_to_time(time_now())
        if month == 1:
            day = time_now()
            # next month
            day = add_times(day, 1000000)
            day = int_to_time(day)
        day["day"] = 1
        day["minute"] = 0
        day["hour"] = 0
        # next month
        certain_future_date = (add_times(time_to_int(day), 1000000))
        day = time_to_int(day)

        while day < certain_future_date:
            Utility.update(day)
            # next day
            day = add_times(day, 10000)
        return 1

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
    def fetch(data) -> [{}]:
        option = data["option"]
        if option == "user":
            dat = Users.find()
            users = {}
            for da in dat:
                if len(da) > 0:
                    users[str(da[0])] = {"id": da[0], "name": da[1], "email": da[2], "auth": da[3]}
            return users
        elif option == "room":
            dat = Rooms.find()
            rooms = {}
            for da in dat:
                if len(da) > 0:
                    rooms[str(da[0])] = {"id": da[0], "name": da[1], "capacity": da[2]}
            return rooms
        elif option == "event":
            dat = Events.find()
            events = {}
            for da in dat:
                if len(da) > 0:
                    events[str(da[0])] = {"id": da[0], "name": da[1], "duration": da[2]}
            return events
        elif option == "event-room":
            dat = Event_Room_Relation.find()
            events = {}
            i = 0
            for da in dat:
                if len(da) > 0:
                    events[i] = {"id": i, "event-name": Events.get_name(int(da[0])), "room-name": Rooms.get_name(int(da[1]))}
                i+=1
            return events
        elif option == "event-guide":
            dat = Event_Guide_Relation.find()
            events = {}
            i = 0
            for da in dat:
                if len(da) > 0:
                    events[i] = {"id": i, "event-name": Events.get_name(int(da[0])), "guide-name": Users.get_name(Guides.get_user_id(int(da[1])))}
                i+=1
            return events
        elif option == "guide-hour":
            dat = WorkHours.find()
            rooms = {}
            for da in dat:
                if len(da) > 0:
                    rooms[str(da[0])] = {"id": da[0], "name": Users.get_name(Guides.get_user_id(int(da[1]))), "day": da[2], "start-hour": da[3], "end-hour": da[4]}
            return rooms

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
    def remove(data) -> int:
        if data["option"] == "user":
            return Users.delete_user(int(data["id"]))
        elif data["option"] == "event":
            return Events.delete_event(int(data["id"]))
        elif data["option"] == "room":
            return Rooms.delete_room(int(data["id"]))
        elif data["option"] == "event-guide":
            return Event_Guide_Relation.remove_relation(Events.get_id(data["id"].split(",")[0]), Guides.get_group_id(Users.get_id(data["id"].split(",")[1])))
        elif data["option"] == "event-room":
            return Event_Room_Relation.remove_relation(Events.get_id(data["id"].split(",")[0]), Rooms.get_id(data["id"].split(",")[1]))
        elif data["option"] == "guide-hour":
            return WorkHours.remove(int(data["id"]))
        return 0
    def new(data) -> int:
        if data["option"] == "user":
            id = Users.new_user(data["name"], data["email"], data["password"])
            if data["auth"] == "guide":
                Guides.assign(id)
            elif data["auth"] == "admin":
                Admins.assign(id)
            elif data["auth"] == "mod":
                Mods.assign(id)
            return id
        elif data["option"] == "event":
            return Events.new_event(data["name"], data["duration"])
        elif data["option"] == "room":
            return Rooms.new_room(data["name"], data["capacity"])
        elif data["option"] == "event-guide":
            return Event_Guide_Relation.add_relation(Events.get_id(data["event-name"]), Guides.get_group_id(Users.get_id(data["guide-name"])))
        elif data["option"] == "event-room":
            return Event_Room_Relation.add_relation(Events.get_id(data["event-name"]), Rooms.get_id(data["room-name"]))
        elif data["option"] == "guide-hour":
            return WorkHours.add(Guides.get_group_id(Users.get_id(data["name"])), int(data["day"]), int(data["start-time"]), int(data["end-time"]))
        return 0
    def mod(data) -> int:
        if data["option"] == "user":
            return Users.mod_user(int(data["id"]), data["name"], data["email"], data["auth"])
        elif data["option"] == "event":
            Events.rename(int(data["id"]), data["name"])
            Events.change_duration(int(data["id"]), data["duration"])
            return 1
        elif data["option"] == "room":
            Rooms.change_capacity(int(data["id"]), data["capacity"])
            Rooms.rename(int(data["id"]), data["name"])
            return 1
        elif data["option"] == "guide-hour":
            WorkHours.update(int(data["id"]), int(data["day"]), int(data["start-hour"]), int(data["end-hour"]))
        return 0

    def mod_user(data) -> int:
        Users.mod_user(int(data["user_id"]), data["user_name"], data["user_email"], data["user_auth"])
        return 1

def check_and_run_monthly_task():
    while True:
        try:
            current_month = datetime.now().strftime("%Y-%m")
            last_run_month = None

            if os.path.exists(Flags.MONTHLY_TASK_FILE):
                with open(Flags.MONTHLY_TASK_FILE, "r") as f:
                    last_run_month = f.read().strip()
            if last_run_month == None:
                full_update(0)
                full_update(1)
            elif last_run_month != current_month:
                full_update(1)
                with open(Flags.MONTHLY_TASK_FILE, "w") as f:
                    f.write(current_month)
        except Exception as e:
            log(f"Error in monthly task checker: {e}")
        
        time.sleep(3600)  # check once every hour