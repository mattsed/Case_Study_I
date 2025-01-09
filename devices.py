import json
import os
from datetime import datetime
from users import User

DEVICE_DATA_FILE = "devices_data.json"
# Definition der Device-Klasse
class Device:
    def __init__(self, id: int, name: str, responsible_person: User, creation_date: datetime, end_of_life: datetime):
        self.id = id
        self.name = name
        self.responsible_person = responsible_person
        self.creation_date = creation_date
        self.end_of_life = end_of_life

    def __repr__(self):
        return f"Gerät: {self.name}, Verantwortlich: {self.responsible_person.name}"

    def to_dict(self):
        """Konvertiere Device-Objekt in ein Dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "responsible_person": self.responsible_person.to_dict(),
            "creation_date": self.creation_date.isoformat(),
            "end_of_life": self.end_of_life.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        """Erstelle ein Device-Objekt aus einem Dictionary."""
        return Device(
            id=data["id"],
            name=data["name"],
            responsible_person=User.from_dict(data["responsible_person"]),
            creation_date=datetime.fromisoformat(data["creation_date"]),
            end_of_life=datetime.fromisoformat(data["end_of_life"]),
        )
    
# Spezifische Funktionen für Geräte
def load_devices():
    """Lade Geräte aus der JSON-Datei."""
    if os.path.exists(DEVICE_DATA_FILE):
        with open(DEVICE_DATA_FILE, "r") as file:
            data = json.load(file)
            return [Device.from_dict(device) for device in data]
    return []


def save_devices(devices):
    """Speichere Geräte in der JSON-Datei."""
    with open(DEVICE_DATA_FILE, "w") as file:
        json.dump([device.to_dict() for device in devices], file)