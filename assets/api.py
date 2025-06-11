from interface import Available_Events
import json
from utils import *
from users import *
from interface import *
import time
from datetime import datetime, date, timedelta

class Utility:
    def update(certain_date):
        try:
            guides = Users.find(user_auth="guide")
            for guide in guides:
                guide_id = Guides.get_group_id(guide[0])
                time_in_time = int_to_time(certain_date)
                year = time_in_time["year"]
                month = time_in_time["month"]
                day = time_in_time["day"]
                day_number = date(year, month, day).weekday()  # Monday = 0

                guide_work_hours = WorkHours.find(guide_id=guide_id, week_day=day_number + 1)
                if len(guide_work_hours) > 0 and len(guide_work_hours[0]) > 0:
                    start_time = time_in_time.copy()
                    end_time = time_in_time.copy()

                    # Occupy guide during normal working hours
                    if int(guide_work_hours[0][3]) > int(Flags.TIME_FIRST_SHOW):
                        start_time["hour"] = int(str(Flags.TIME_FIRST_SHOW)[:2])
                        start_time["minute"] = int(str(Flags.TIME_FIRST_SHOW)[2:])
                        end_time["hour"] = int(str(guide_work_hours[0][3])[:2])
                        end_time["minute"] = int(str(guide_work_hours[0][3])[2:])
                    elif int(guide_work_hours[0][4]) < int(Flags.TIME_LAST_SHOW):
                        start_time["hour"] = int(str(guide_work_hours[0][4])[:2])
                        start_time["minute"] = int(str(guide_work_hours[0][4])[2:])
                        end_time["hour"] = int(str(Flags.TIME_LAST_SHOW)[:2])
                        end_time["minute"] = int(str(Flags.TIME_LAST_SHOW)[2:])
                    elif guide_work_hours[0][4] == Flags.TIME_LAST_SHOW and guide_work_hours[0][3] == Flags.TIME_FIRST_SHOW:
                        pass
                    else:
                        raise ValueError(Errors.wrong_time)

                    # Add work-hour occupation
                    Guides.occupie(guide_id, time_to_int(start_time), time_to_int(end_time), "Off work")

                    # --- ✅ Add night block: today TIME_LAST_SHOW -> next day TIME_FIRST_SHOW ---

                # Block start: today at TIME_LAST_SHOW
                night_start = time_in_time.copy()
                night_start["hour"] = int(str(Flags.TIME_LAST_SHOW)[:2])
                night_start["minute"] = int(str(Flags.TIME_LAST_SHOW)[2:])

                # Block end: next day at TIME_FIRST_SHOW
                next_day = datetime(year, month, day) + timedelta(days=1)
                night_end = {
                    "year": next_day.year,
                    "month": next_day.month,
                    "day": next_day.day,
                    "hour": int(str(Flags.TIME_FIRST_SHOW)[:2]),
                    "minute": int(str(Flags.TIME_FIRST_SHOW)[2:])
                }

                Guides.occupie(guide_id, time_to_int(night_start), time_to_int(night_end), "Closed hours")

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
    def fetch_free_by_find(from_time, to_time, event_id) -> []:
        try:
            # print(room_id, guide_id, event_id)
            free_events = []
            if to_time < from_time:
                raise ValueError(Errors.wrong_time)
            events = Available_Events.find(event_id=event_id)
            for event in events:
                availability = Available_Events.get_availability(event[0], from_time, to_time)
                if len(availability) > 0:
                    for frame in availability:
                        free_events.append(frame)
            free_events = sorted(free_events, key=lambda x: (to_dt(x["start"]), -to_dt(x["end"]).timestamp()))

            # Squash overlapping or duplicate time ranges
            squashed = []
            for event in free_events:
                start = to_dt(event["start"])
                end = to_dt(event["end"])
            
                if not squashed:
                    squashed.append(event)
                    continue
                
                last = squashed[-1]
                last_start = to_dt(last["start"])
                last_end = to_dt(last["end"])
            
                # Check if this event is fully within the last one
                if start >= last_start and end <= last_end:
                    continue  # Skip this one
                
                squashed.append(event)
            return squashed
        except Exception as e:
            log(f"Error while fetching spots by find: {e}")
            return []
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
                    rooms[str(da[0])] = {"id": da[0], "name": Users.get_name(Guides.get_user_id(int(da[1]))), "day": da[2], "start-hour": str(da[3])[:2]+":"+str(da[3])[2:], "end-hour": str(da[4])[:2]+":"+str(da[4])[2:]}
            return rooms

class Process:
    def handle_inquiry(data) -> [()]:
        try:
            time = data["time"]
            date = data["date"]
            events = data["events"]
            if len(events) < 1:
                events = [None]
            # convert data from js format
            time[0] = time[0][:2]+time[0][3:]
            time[1] = time[1][:2]+time[1][3:]
            date = date.split("-")[0]+date.split("-")[1]+date.split("-")[2]
            from_time = date+time[0]
            to_time = date+time[1]
            
            possible_spots = {}
            for event in events:
                data = Fetch.fetch_free_by_find(from_time, to_time, event)
                if len(data) > 0:
                    for da in data:
                        possible_spots[Events.get_name(int(Available_Events.find(int(da["id"]))[0][1]))] = data;
            
            print(possible_spots)
            return possible_spots
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
            # print(data)
            
            return WorkHours.add(Guides.get_group_id(Users.get_id(data["name"])), int(data["day"]), data["start-time"][:2].zfill(2)+data["start-time"][3:].zfill(2), data["end-time"][:2].zfill(2)+data["end-time"][3:].zfill(2))
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
            WorkHours.update(int(data["id"]), int(data["day"]), data["start-hour"][:2].zfill(2)+data["start-hour"][3:].zfill(2), data["end-hour"][:2].zfill(2)+data["end-hour"][3:].zfill(2))
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