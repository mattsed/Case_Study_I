import json
import os

USER_DATA_FILE = "users_data.json"

# Definition der User-Klasse
class User:
    def __init__(self, email: str, name: str):
        self.email = email
        self.name = name

    def __repr__(self):
        return f"{self.name} ({self.email})"

    def to_dict(self):
        """Konvertiere User-Objekt in ein Dictionary."""
        return {"email": self.email, "name": self.name}

    @staticmethod
    def from_dict(data):
        """Erstelle ein User-Objekt aus einem Dictionary."""
        return User(email=data["email"], name=data["name"])
    

# Spezifische Funktionen für Nutzer
def load_users():
    """Lade Nutzer aus der JSON-Datei."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            data = json.load(file)
            return [User.from_dict(user) for user in data]
    return []

def save_users(users):
    """Speichere Nutzer in der JSON-Datei."""
    with open(USER_DATA_FILE, "w") as file:
        json.dump([user.to_dict() for user in users], file)