from utils import log, min_times, min_times2, int_to_google_datetime
from database import MainDB
from config import Errors, FindError, FailedMethodError
from callender_api import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

class EmailSender:
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    @staticmethod
    def send_email(to_email, subject: str, body: str,
                   from_email: str = None, is_html: bool = False) -> bool:
        if not from_email:
            from_email = EmailSender.SMTP_USERNAME

        try:
            # Construct email
            msg = MIMEMultipart()
            msg["From"] = from_email
            msg["To"] = to_email
            msg["Subject"] = subject

            mime_type = "html" if is_html else "plain"
            msg.attach(MIMEText(body, mime_type))

            # Use SMTP over SSL
            with smtplib.SMTP_SSL(EmailSender.SMTP_HOST, int(EmailSender.SMTP_PORT)) as server:
                server.login(EmailSender.SMTP_USERNAME, EmailSender.SMTP_PASSWORD)
                server.sendmail(from_email, to_email, msg.as_string())
            log(f"Email sent to : {to_email}")
            return True

        except Exception as e:
            log(f"Failed to send email: {e}")
            return False
    @staticmethod
    def send_confirmation_email(to_email, event, time, duration) -> bool:
        if EmailSender.send_email(to_email, Flags.EMAIL_SUBJECT, Flags.EMAIL_BODY, False):
            return True
        else:
            return False



class Events:
    @classmethod
    def get_id(self, event_name) -> int:
        try:
            data = MainDB.query("SELECT event_id FROM events WHERE event_name = ?", (event_name,))
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            if len(data) > 1:
                raise FindError(Errors.duplicate_found)
            return data[0][0]
        except Exception as e:
            log(f"Error while getting event id of [{event_name}]: {e}")
            return -1
    
    @classmethod
    def find(self) -> []:
        try:
            data = MainDB.query("SELECT * FROM events")
            return data
        except Exception as e:
            log(f"Error while finding events: {e}")
            return -1

    @classmethod
    def new_event(self, event_name, duration, event_type) -> int:
        try:
            event_id = MainDB.execute("INSERT INTO events (event_name, duration, event_type) VALUES(?, ?, ?)", (event_name, duration, event_type))
            log(f"Created event [{event_id}]")
            return event_id
        except Exception as e:
            log(f"Error while creating new event [{event_name}]: {e}")
            return -1

    @classmethod
    def get_name(self, event_id) -> str:
        try:
            if event_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT event_name FROM events WHERE event_id = ?", (event_id,))
            if len(data) > 1:
                raise FindError(Errors.failed_find)
            if len(data) < 1:
                log(f"No events found for event [{event_id}]")
                return ""
            log(f"Event name [{data[0][0]}] found for [{event_id}]")
            return data[0][0]
        except Exception as e:
            log(f"Error while finding name of event [{event_id}]")
            return ""
    
    @classmethod
    def get_type(self, event_id) -> str:
        try:
            if event_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT event_type FROM events WHERE event_id = ?", (event_id,))
            if len(data) > 1:
                raise FindError(Errors.failed_find)
            if len(data) < 1:
                log(f"No events found for event [{event_id}]")
                return ""
            log(f"Event type [{data[0][0]}] found for [{event_id}]")
            return data[0][0]
        except Exception as e:
            log(f"Error while finding type of event [{event_id}]")
            return ""

    @classmethod
    def delete_event(self, event_id) -> int:
        try:
            if event_id < 1:
                raise ValueError(Errors.id_below_one)
            MainDB.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
            rooms = Event_Room_Relation.get_rooms(event_id)
            for room in rooms:
                if len(room) > 0:
                    Event_Room_Relation.remove_relation(event_id, room[0])
            guides = Event_Guide_Relation.get_guides(event_id)
            for guide in guides:
                if len(guide) > 0:
                    Event_Guide_Relation.remove_relation(event_id, guide[0])
            log(f"Removed event [{event_id}]")
            return 1
        except Exception as e:
            log(f"Error while deleting event [{event_id}]: {e}")
            return -1

    @classmethod
    def rename(self, event_id, new_name) -> int:
        try:
            if event_id < 1:
                raise ValueError(Errors.id_below_one)
            MainDB.execute("UPDATE events SET event_name = ? WHERE event_id = ?", (new_name, event_id))
            log(f"Renamed event [{event_id}]")
            return 1
        except Exception as e:
            log(f"Error while renaming event [{event_id}]: {e}")
            return -1
    
    @classmethod
    def change_duration(self, event_id, new_duration) -> int:
        try:
            if event_id < 1:
                raise ValueError(Errors.id_below_one)
            MainDB.execute("UPDATE events SET duration = ? WHERE event_id = ?", (new_duration, event_id))
            log(f"Changed duration of event [{event_id}]")
            return 1
        except Exception as e:
            log(f"Error while changing duration of event [{event_id}]: {e}")
            return -1
    
    @classmethod
    def get_duration(self, event_id) -> int:
        try:
            event_id = int(event_id)
            if event_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT duration FROM events WHERE event_id = ?", (event_id,))
            if len(data) < 1 or len(data) > 1:
                raise FindError(Errors.failed_find)
            log(f"Got duration of event [{event_id}]")
            return data[0][0]
        except Exception as e:
            log(f"Error while getting event [{event_id}] duration: {e}")
            return -1

class Rooms:
    @classmethod
    def get_id(self, room_name) -> int:
        try:
            data = MainDB.query("SELECT room_id FROM rooms WHERE room_name = ?", (room_name,))
            if len(data) > 1:
                raise FindError(Errors.failed_find)
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            log(f"Room id [{data[0][0]}] found for [{room_name}]")
            return data[0][0]
        except Exception as e:
            log(f"Error while finding id of room [{room_name}]: {e}")
            return -1
    
    @classmethod
    def find(self) -> []:
        try:
            data = MainDB.query("SELECT * FROM rooms")
            return data
        except Exception as e:
            log(f"Error while finding rooms: {e}")
            return -1
    

    @classmethod
    def new_room(self, room_name, capacity) -> int:
        try:
            room_id = MainDB.execute("INSERT INTO rooms (room_name, capacity) VALUES(?, ?)", (room_name, capacity))
            log(f"Created room [{room_id}]")
            return room_id
        except Exception as e:
            log(f"Error while creating new room [{room_name}]: {e}")
    
    @classmethod
    def get_name(self, room_id) -> str:
        try:
            if room_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT room_name FROM rooms WHERE room_id = ?", (room_id,))
            if len(data) > 1:
                raise FindError(Errors.failed_find)
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            log(f"room name [{data[0][0]}] found for [{room_id}]")
            return data[0][0]
        except Exception as e:
            log(f"Error while finding name of room [{room_id}]: {e}")
            return ""
    
    @classmethod
    def delete_room(self, room_id) -> int:
        try:
            if room_id < 1:
                raise ValueError(Errors.id_below_one)
            if self.get_name(room_id) == "":
                raise FindError(Errors.failed_find)
            MainDB.execute("DELETE FROM rooms WHERE room_id = ?", (room_id,))
            events = Event_Room_Relation.get_events(room_id)
            for event in events:
                if len(event) > 0:
                    Event_Room_Relation.remove_relation(event[0], room_id)
            log(f"Removed room [{room_id}]")
            return 1
        except Exception as e:
            log(f"Error while deleting room [{room_id}]: {e}")
            return -1

    @classmethod
    def rename(self, room_id, new_name) -> int:
        try:
            if room_id < 1:
                raise ValueError(Errors.id_below_one)
            if self.get_name(room_id) == "":
                raise FindError(Errors.failed_find)
            MainDB.execute("UPDATE rooms SET room_name = ? WHERE room_id = ?", (new_name, room_id))
            log(f"Renamed room [{room_id}]")
            return 1
        except Exception as e:
            log(f"Error while renaming room [{room_id}]: {e}")
            return -1
    
    @classmethod
    def change_capacity(self, room_id, new_capacity) -> int:
        try:
            if room_id < 1:
                raise ValueError(Errors.id_below_one)
            if self.get_name(room_id) == "":
                raise FindError(Errors.failed_find)
            MainDB.execute("UPDATE rooms SET capacity = ? WHERE room_id = ?", (new_capacity, room_id))
            log(f"Changed capacity of room [{room_id}]")
            return 1
        except Exception as e:
            log(f"Error while changing capacity of room [{room_id}]: {e}")
            return -1
    
    @classmethod
    def get_capacity(self, room_id) -> int:
        try:
            if room_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT capacity FROM rooms WHERE room_id = ?", (room_id,))
            if len(data) > 1:
                raise FindError(Errors.failed_find)
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            log(f"Room capacity [{data[0][0]}] found for [{room_id}]")
            return data[0][0]
        except Exception as e:
            log(f"Error while finding capacity of room [{room_id}]: {e}")
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
    def change_occ_time(self, id, new_start_time = None, new_end_time = None) -> int:
        try:
            if id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT * FROM room_occupation WHERE id = ?", (id,))
            if len(data) < 1:
                raise FindError(Errors.failed_find)
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
    def get_occupation_by_id(self, id) -> [()]:
        try:
            if id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT * FROM room_occupation WHERE id = ?", (id,))
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            return data
        except Exception as e:
            log(f"Error while getting occupation room [{id}]: {e}")
            return [()]

    @classmethod
    def get_occupation_by_room(self, room_id) -> [()]:
        try:
            if room_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT * FROM room_occupation WHERE room_id = ?", (room_id,))
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            return data
        except Exception as e:
            log(f"Error while getting occupation for room [{room_id}]: {e}")
            return [()]
    
    @classmethod
    def free(self, id) -> int:
        try:
            if id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT * FROM room_occupation WHERE id = ?", (id,))
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            MainDB.execute("DELETE FROM room_occupation WHERE id = ?", (id,))
            return 1
        except Exception as e:
            log(f"Error while freeing room [{id}]: {e}")
            return -1
    
    # this method needs testing
    @classmethod
    def get_occupied_full(self, id) -> []:
        intervals = self.get_occupation_by_room(id)
        set_count = self.get_capacity(id)

        if not intervals:
            return []
        if not intervals[0]:
            return []
        events = []
        for data in intervals:
            events.append((data[2], 1))   # start
            events.append((data[3], -1))  # end
        events.sort()

        active = 0
        last_time = None
        raw_result = []

        for time, delta in events:
            if last_time is not None and active >= set_count and last_time < time:
                raw_result.append((last_time, time))
            active += delta
            last_time = time

        # Merge touching intervals
        if not raw_result:
            return []

        merged = [raw_result[0]]
        for start, end in raw_result[1:]:
            last_start, last_end = merged[-1]
            if last_end >= start:  # touching or overlapping
                merged[-1] = (last_start, max(last_end, end))
            else:
                merged.append((start, end))

        return merged

class Event_Guide_Relation:
    @classmethod
    def check_relation(self, event_id, guide_id) -> int:
        try:
            if event_id < 1 or guide_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT * FROM event_guide_relation WHERE event_id = ? AND guide_id = ?", (event_id, guide_id))
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            return 1
        except Exception as e:
            log(f"Error while checking relation of {event_id}-{guide_id}: {e}")
            return -1

    @classmethod
    def find(self) -> []:
        try:
            data = MainDB.query("SELECT * FROM event_guide_relation")
            return data
        except Exception as e:
            log(f"Error while finding event_guide_relations: {e}")
            return -1

    @classmethod
    def get_guides(self, event_id) -> [()]:
        try:
            if event_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT guide_id FROM event_guide_relation WHERE event_id = ?", (event_id,))
            if len(data) < 1:
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting guides for event [{event_id}]: {e}")
            return [()]

    @classmethod
    def get_events(self, guide_id) -> [()]:
        try:
            if guide_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT event_id FROM event_guide_relation WHERE guide_id = ?", (guide_id,))
            if len(data) < 1:
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting events for guide [{guide_id}]: {e}")
            return [()]

    @classmethod
    def add_relation(self, event_id, guide_id) -> int:
        try:
            if event_id < 1 or guide_id < 1:
                raise ValueError(Errors.id_below_one)
            MainDB.execute("INSERT INTO event_guide_relation (event_id, guide_id) VALUES(?, ?)", (event_id, guide_id))
            rooms = Event_Room_Relation.get_rooms(event_id)
            for room in rooms:
                if len(room) > 0:
                    Available_Events.new(event_id, room[0], guide_id)
            return 1
        except Exception as e:
            log(f"Error while adding guide relation between [{event_id}]-[{guide_id}]: {e}")
            return -1
    
    @classmethod
    def remove_relation(self, event_id, guide_id):
        try:
            if event_id < 1 or guide_id < 1:
                raise ValueError(Errors.id_below_one)
            if self.check_relation(event_id, guide_id) < 1:
                raise FindError(Errors.failed_find)
            MainDB.execute("DELETE FROM event_guide_relation WHERE event_id = ? AND guide_id = ?", (event_id, guide_id))
            events = Available_Events.find(event_id = event_id, guide_id = guide_id)
            for event in events:
                Available_Events.remove(event[0])
            log(f"Removed relation between guide [{guide_id}] and event [{event_id}]")
            return 1
        except Exception as e:
            log(f"Error while removing relation: {e}")
            return -1

class Event_Room_Relation:
    @classmethod
    def check_relation(self, event_id, room_id) -> int:
        try:
            if event_id < 1 or room_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT * FROM room_event_relation WHERE event_id = ? AND room_id = ?", (event_id, room_id))
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            return 1
        except Exception as e:
            log(f"Error while checking relation of {event_id}-{room_id}: {e}")
            return -1

    @classmethod
    def find(self) -> []:
        try:
            data = MainDB.query("SELECT * FROM room_event_relation")
            return data
        except Exception as e:
            log(f"Error while finding event_room_relations: {e}")
            return -1

    @classmethod
    def get_rooms(self, event_id) -> [()]:
        try:
            if event_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT room_id FROM room_event_relation WHERE event_id = ?", (event_id,))
            if len(data) < 1:
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting rooms for event [{event_id}]: {e}")
            return [()]

    @classmethod
    def get_events(self, room_id) -> [()]:
        try:
            if room_id < 1:
                raise ValueError(Errors.id_below_one)
            data = MainDB.query("SELECT event_id FROM room_event_relation WHERE room_id = ?", (room_id,))
            if len(data) < 1:
                return [()]
            return data
        except Exception as e:
            log(f"Error while getting events for room [{room_id}]: {e}")
            return [()]

    @classmethod
    def add_relation(self, event_id, room_id) -> int:
        try:
            if event_id < 1 or room_id < 1:
                raise ValueError(Errors.id_below_one)
            MainDB.execute("INSERT INTO room_event_relation (event_id, room_id) VALUES(?, ?)", (event_id, room_id))
            guides = Event_Guide_Relation.get_guides(event_id)
            for guide in guides:
                if len(guide) > 0:
                    Available_Events.new(event_id, room_id, guide[0])
            return 1
        except Exception as e:
            log(f"Error while adding room relation between [{event_id}]-[{room_id}]: {e}")
            return -1
    
    @classmethod
    def remove_relation(self, event_id, room_id):
        try:
            if event_id < 1 or room_id < 1:
                raise ValueError(Errors.id_below_one)
            if self.check_relation(event_id, room_id) < 1:
                raise FindError(Errors.failed_find)
            MainDB.execute("DELETE FROM room_event_relation WHERE event_id = ? AND room_id = ?", (event_id, room_id))
            events = Available_Events.find(event_id = event_id, room_id = room_id)
            for event in events:
                Available_Events.remove(event[0])
            log(f"Removed relation between room [{room_id}] and event [{event_id}]")
            return 1
        except Exception as e:
            log(f"Error while removing relation: {e}")
            return -1

class Available_Events:
    @classmethod
    def find(self, id = None, event_id = None, room_id = None, guide_id = None) -> [()]:
        try:
            if id == None and event_id == None and room_id == None and guide_id == None:
                return MainDB.query(f"SELECT * FROM available_events")
            placeholder = ""
            values = ()
            if id != None:
                placeholder += "available_event_id = ?"
                values = values + (id,)
            if event_id != None:
                if placeholder != "":
                    placeholder += " AND "
                placeholder += "event_id = ?"
                values = values + (event_id,)
            if room_id != None:
                if placeholder != "":
                    placeholder += " AND "
                placeholder += "room_id = ?"
                values = values + (room_id,)
            if guide_id != None:
                if placeholder != "":
                    placeholder += " AND "
                placeholder += "guide_id = ?"
                values = values + (guide_id,)
            data = MainDB.query(f"SELECT * FROM available_events WHERE {placeholder}", values)
            log(f"Found {len(data)} available events")
            return data
        except Exception as e:
            log(f"Error while finding available event: {e}")
            return [()]

    @classmethod
    def new(self, event_id, room_id, guide_id) -> int:
        try:
            if event_id < 1 or room_id < 1 or guide_id < 1:
                raise ValueError(Errors.id_below_one)
            event_id = MainDB.execute("INSERT INTO available_events (event_id, room_id, guide_id) VALUES(?, ?, ?)", (event_id, room_id, guide_id))
            log(f"Made new available event [{event_id}]")
            return event_id
        except Exception as e:
            log(f"Error while adding new available event: {e}")
            return -1

    @classmethod
    def remove(self, id) -> int:
        try:
            if id < 1:
                raise ValueError(Errors.id_below_one)
            data = self.find(id=id)
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            MainDB.execute("DELETE FROM available_events WHERE available_event_id = ?", (id,))
            occupations = Occupied_Events.find(available_event_id=id)
            for occupation in occupations:
                if len(occupation) > 0:
                    Occupied_Events.delete(occupation[0])
            log(f"Removed available_event: {id}")
            return 1
        except Exception as e:
            log(f"Error while removing available event {id}: {e}")
            return -1

    @classmethod 
    # Please do not judge this code, it's tryinh its best.
    # May god help it
    def get_availability(self, id, time_from, time_to) -> [()]:
        try:
            if id < 1:
                raise ValueError(Errors.id_below_one)

            data = self.find(id=id)[0]
            if len(data) < 1:
                raise FindError(Errors.failed_find)

            event_duration = Events.get_duration(data[1])

            from users import Guides

            # Get guide occupation times
            guide_oc_temp = Guides.get_occupation_by_guide(data[3])
            guide_oc = [(g[2], g[3]) for g in guide_oc_temp if len(g) > 0]

            # Get room occupation times
            room_oc = Rooms.get_occupied_full(data[2])
            time_from = int(time_from)
            time_to = int(time_to)
            # Combine all unavailability
            all_oc = []
            for start, end in guide_oc + room_oc:
                start = int(start)
                end = int(end)
                if start < end:
                    all_oc.append((max(start, time_from), min(end, time_to)))  # Clip to window
            all_oc = [oc for oc in all_oc if oc[0] < oc[1]]
            all_oc.sort()

            # ✅ If there are no conflicts, return full window as free (if it’s long enough)
            if not all_oc:
                if min_times2(time_to, time_from) >= event_duration:
                    return [{"id": id, "start": str(time_from), "end": str(time_to)}]
                else:
                    return [{}]
            # Merge overlapping/touching unavailabilities
            merged = []
            for start, end in all_oc:
                if not merged:
                    merged.append((start, end))
                else:
                    last_start, last_end = merged[-1]
                    if last_end >= start:
                        merged[-1] = (last_start, max(last_end, end))
                    else:
                        merged.append((start, end))

            # Invert merged intervals to find free time
            free = []
            current = time_from
            for start, end in merged:
                if current < start and min_times2(start, current) >= event_duration:
                    free.append((current, start))
                current = max(current, end)

            if current < time_to and min_times2(time_to, current) >= event_duration:
                free.append((current, time_to))
            for i in range(len(free)):
                free[i] = {"id": id,"start": str(free[i][0]), "end": str(free[i][1])}
            return free

        except Exception as e:
            log(f"Error in get_availability: {e}")
            return [{}]

class Occupied_Events:
    @classmethod
    def find(self, id = None, guide_oc_id = None, room_oc_id = None, available_event_id = None, busy_from = None, busy_to = None) -> [()]:
        try:
            placeholder = ""
            values = ()
            if id != None:
                placeholder += "id = ?"
                values = values + (id,)
            if guide_oc_id != None:
                if placeholder != "":
                    placeholder += " AND "
                placeholder += "guide_oc_id = ?"
                values = values + (guide_oc_id,)
            if room_oc_id != None:
                if placeholder != "":
                    placeholder += " AND "
                placeholder += "room_oc_id = ?"
                values = values + (room_oc_id,)
            if available_event_id != None:
                if placeholder != "":
                    placeholder += " AND "
                placeholder += "available_event_id = ?"
                values = values + (available_event_id,)
            if busy_from != None:
                if placeholder != "":
                    placeholder += " AND "
                placeholder += "busy_from = ?"
                values = values + (busy_from,)
            if busy_to != None:
                if placeholder != "":
                    placeholder += " AND "
                placeholder += "busy_to = ?"
                values = values + (busy_to,)
            data = MainDB.query(f"SELECT * FROM occupied_events WHERE {placeholder}", values)
            log(f"Found {len(data)} occupied events")
            return data
        except Exception as e:
            log(f"Error while finding occupied event: {e}")
            return [()]
    
    @classmethod
    def new(self, busy_from, busy_to, available_event_id, booker, email, phone, pay_method, istaiga, people, person, extra_info) -> int:
        try:
            if available_event_id < 1:
                raise ValueError(config.errors.id_below_one)
            event = Available_Events.find(id=available_event_id)
            from users import Guides, Users
            guide_oc_id = Guides.occupie(event[0][3] , busy_from, busy_to, f"Event {Events.get_name(event[0][1])} at {[Rooms.get_name(event[0][2])]}")
            if guide_oc_id < 1:
                raise FailedMethodError(Errors.occupie_failed)
            room_oc_id = Rooms.occupie(event[0][2], busy_from, busy_to, f"Event {Events.get_name(event[0][1])} with guide {Users.get_name(Guides.get_user_id(event[0][3]))}")
            if room_oc_id < 1:
                raise FailedMethodError(Errors.occupie_failed)
        
            id = MainDB.execute("INSERT INTO occupied_events (guide_oc_id, room_oc_id, available_event_id, busy_from, busy_to, responsible, email, phone, pay_method, istaiga, people, person, extra_info) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (guide_oc_id, room_oc_id, available_event_id, busy_from, busy_to, booker, email, phone, pay_method, istaiga, people, person, extra_info))
            # write a full body later

            GoogleCalendarBot.create_event(
                summary=f"{Events.get_name(event[0][1])}",
                start_time=int_to_google_datetime(busy_from),
                end_time=int_to_google_datetime(busy_to),
                # attendees=[Users.find(user_id=Guides.get_user_id(event[0][3]))[0][2]],
                description=f"""
                    Room: {Rooms.get_name(event[0][2])}
                    Guide: {Users.get_name(Guides.get_user_id(event[0][3]))}
                    Booker: {booker}
                    Contact-email: {email}
                    Contact-phone: {phone}
                    Leading-person: {person}
                    Number-of-people: {people}
                    Įstaiga: {istaiga}
                    Pay-method: {pay_method}
                    Extra: {extra_info}
                """
            )

            EmailSender.send_confirmation_email(
                to_email=email,
                event = Events.get_name(event[0][1]),
                time = int_to_google_datetime(busy_from),
                duration = Events.get_duration(event[0][1])
            )
            log(f"Ocupied new event [{id}]")
            return id
        except Exception as e:
            log(f"Error while adding new occupied event: {e}")
            return -1
    
    @classmethod
    def delete(self, id) -> int:
        try:
            if id < 1:
                raise ValueError(Errors.id_below_one)
            data = self.find(id=id)
            if len(data) < 1:
                raise FindError(Errors.failed_find)
            MainDB.execute("DELETE FROM occupied_events WHERE id = ?", (id,))
            from users import Guides

            Guides.free(data[0][2])
            Rooms.free(data[0][3])
            log(f"Deleted occupied event {id}")
            return 1
        except Exception as e:
            log(f"Error while deleting occupied event [{id}]: {e}")
            return -1
    
    @classmethod
    def change_time(self, id, new_from, new_to) -> id:
        try:
            if id < 1:
                raise ValueError(Errors.id_below_one)
            if len(self.find(id=id)) < 1:
                raise FindError(Errors.failed_find)
            MainDB.execute(f"UPDATE occupied_events SET busy_from = ?, busy_to = ? WHERE id = ?", (new_from, new_to, id))
            log(f"Changed time of occupied event [{id}]")
            return 1
        except Exception as e:
            log(f"Error while changing time of event [{id}]: {e}")
            return -1
    
    @classmethod
    def change_comment(self, id, comment):
        try:
            if id < 1:
                raise ValueError(Errors.id_below_one)
            if len(self.find(id=id)) < 1:
                raise FindError(Errors.failed_find)
            MainDB.execute(f"UPDATE occupied_events SET comment = ? WHERE id = ?", (comment, id))
            log(f"Changed comment of occupied event [{id}]")
            return 1
        except Exception as e:
            log(f"Error while changing comment of event [{id}]: {e}")
            return -1
