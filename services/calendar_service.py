import json
import uuid
from datetime import datetime
from pathlib import Path

CURRENT_DIR = Path.cwd()


class CalendarService:

    def __init__(self, file_path="events/calendar_events.json"):
        self.file_path = CURRENT_DIR/file_path
        print('path file')

    def create_event(self, title: str, description: str, datetime_str: str):

        event = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "datetime": datetime_str
        }

        try:
            with open(self.file_path, "r") as f:
                events = json.load(f)
        except FileNotFoundError:
            events = []

        events.append(event)

        with open(self.file_path, "w") as f:
            json.dump(events, f, indent=2)

        print('event created')

        return event


service = CalendarService()

if __name__ == "__main__":
    print(CURRENT_DIR)