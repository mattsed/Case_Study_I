import streamlit as st
import json
import os
from datetime import datetime

# Dateipfade für das Speichern der Nutzerdaten und Gerätedaten
USER_DATA_FILE = "users_data.json"
DEVICE_DATA_FILE = "devices_data.json"

##################################################################################################################################

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

###########################################################################################################################################

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

###############################################################################################################################################

# Initialisiere Nutzer- und Gerätelisten in Session State
if "users" not in st.session_state:
    st.session_state.users = load_users()

if "devices" not in st.session_state:
    st.session_state.devices = load_devices()

###############################################################################################################################################

# Seiten-Logik
def show_user_management():
    st.write("## Nutzerverwaltung")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Nutzer anlegen")
        new_name = st.text_input("Name des Nutzers:")
        new_email = st.text_input("E-Mail des Nutzers:")
        if st.button("Nutzer hinzufügen"):
            if new_name and new_email:
                if not any(user.email == new_email for user in st.session_state.users):
                    new_user = User(email=new_email, name=new_name)
                    st.session_state.users.append(new_user)
                    save_users(st.session_state.users)
                    st.success(f"Nutzer '{new_name}' wurde hinzugefügt!")
                else:
                    st.warning("Ein Nutzer mit dieser E-Mail existiert bereits!")
            else:
                st.error("Bitte alle Felder ausfüllen!")

    with col2:
        st.subheader("Vorhandene Nutzer")
        if st.session_state.users:
            for user in st.session_state.users:
                st.write(f"- {user.name} ({user.email})")
        else:
            st.info("Keine Nutzer vorhanden.")


def show_device_management():
    st.write("## Geräteverwaltung")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gerät anlegen")
        device_id = st.number_input("Geräte-ID", min_value=1, step=1)
        device_name = st.text_input("Gerätename")
        responsible_person = st.selectbox(
            "Verantwortliche Person", options=st.session_state.users, format_func=lambda user: user.name
        )
        creation_date = st.date_input("Erstellungsdatum", value=datetime.now())
        end_of_life = st.date_input("End-of-Life Datum")

        if st.button("Gerät hinzufügen"):
            if device_name and responsible_person and creation_date and end_of_life:
                new_device = Device(
                    id=device_id,
                    name=device_name,
                    responsible_person=responsible_person,
                    creation_date=datetime.combine(creation_date, datetime.min.time()),
                    end_of_life=datetime.combine(end_of_life, datetime.min.time()),
                )
                st.session_state.devices.append(new_device)
                save_devices(st.session_state.devices)
                st.success(f"Gerät '{new_device.name}' wurde erfolgreich hinzugefügt!")
            else:
                st.error("Bitte alle Pflichtfelder ausfüllen!")

    with col2:
        st.subheader("Vorhandene Geräte")
        for device in st.session_state.devices:
            st.write(device)

#####################################################################################################################################

# Hauptmenü
st.write("# Gerätemanagement System")
st.write("## Navigation")

menu_option = st.selectbox("Wählen Sie eine Option:", ["Nutzerverwaltung", "Geräteverwaltung"])

st.markdown("<br><br>", unsafe_allow_html=True)

if menu_option == "Nutzerverwaltung":
    show_user_management()
elif menu_option == "Geräteverwaltung":
    show_device_management()
