from interface import Available_Events
import json
from utils import *
from users import *

class Fetch:
    def fetch_free_by_event(event_id) -> [()]:
        try:
            free_events = []
            from_time = time_now()
            to_time = time_last()
            if to_time < from_time:
                raise ValueError(Errors.wrong_time)
            events = Available_Events.find(event_id=event_id)
            for event in events:
                availability = Available_Events.get_availability(event[0], from_time, to_time).append(event[0])
                free_events += availability
            return free_events
        except Exception as e:
            log(f"Error while fetching spots by event: {e}")

    def fetch_free_by_time(from_time, to_time) -> [()]:
        try:
            free_events = []
            from_time = time_to_int(from_time)
            to_time = time_to_int(to_time)
            if to_time < from_time:
                raise ValueError(Errors.wrong_time)
            events = Available_Events.find()
            for event in events:
                availability = Available_Events.get_availability(event[0], from_time, to_time).append(event[0])
                free_events += availability
            return free_events
        except Exception as e:
            log(f"Error while fetching spots by time: {e}")

    def fetch_free_by_guide(guide_id) -> [()]:
        try:
            free_events = []
            from_time = time_now()
            to_time = time_last()
            if to_time < from_time:
                raise ValueError(Errors.wrong_time)
            events = Available_Events.find(guide_id=guide_id)
            for event in events:
                availability = Available_Events.get_availability(event[0], from_time, to_time).append(event[0])
                free_events += availability
            return free_events
        except Exception as e:
            log(f"Error while fetching spots by guide: {e}")

    def fetch_free_by_room(room_id) -> [()]:
        try:
            free_events = []
            from_time = time_now()
            to_time = time_last()
            if to_time < from_time:
                raise ValueError(Errors.wrong_time)
            events = Available_Events.find(room_id=room_id)
            for event in events:
                availability = Available_Events.get_availability(event[0], from_time, to_time).append(event[0])
                free_events += availability
            return free_events
        except Exception as e:
            log(f"Error while fetching spots by room: {e}")

class Process:
    def handle_inquiry(data) -> [()]:
        try:
            print(data)
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