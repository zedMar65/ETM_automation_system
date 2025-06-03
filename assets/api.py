from interface import Available_Events

def fetch_free_by_event(event_id) -> [()]:
    try:
        free_events = []
        from_time = time_now()
        to_time = time_last()
        if to_time < from_time:
            raise ValueError(Errors.wrong_time)
        events = Available_Events.find(event_id=event_id)
        for event in events:
            availability = Available_Events.get_availability(event[0], from_time, to_time)
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
            availability = Available_Events.get_availability(event[0], from_time, to_time)
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
            availability = Available_Events.get_availability(event[0], from_time, to_time)
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
            availability = Available_Events.get_availability(event[0], from_time, to_time)
            free_events += availability
        return free_events
    except Exception as e:
        log(f"Error while fetching spots by room: {e}")
