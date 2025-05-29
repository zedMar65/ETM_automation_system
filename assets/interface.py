from utils import log
from database import MainDB

def add_guide(name, event_ids) -> bool:
    try:
        MainDB.execute("INSERT INTO guides (guide_name) VALUES(?)", (name,))
        guide_id = MainDB._cursor.lastrowid
        for event_id in event_ids:
            MainDB.execute(
                "INSERT INTO event_guides (guide_id, event_id) VALUES(?, ?)", 
                (guide_id, event_id))
    except Exception as e:
        log(f"Error while adding guide:{e}")