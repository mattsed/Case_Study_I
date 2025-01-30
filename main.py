import streamlit as st
import json
import os
from devices import Device, load_devices, save_devices
from users import User, load_users, save_users 
from datetime import datetime

RESERVATIONS_FILE = "reservations.json"

# Reservierungsklasse definieren
class Reservation:
    def __init__(self, device, user, start_date, end_date):
        if isinstance(device, str) or isinstance(user, str):
            raise ValueError("Device oder User wurden als String gespeichert, erwartet wird ein Dictionary.")
        
        self.device = Device(**device) if isinstance(device, dict) else device
        self.user = User(**user) if isinstance(user, dict) else user
        self.start_date = start_date
        self.end_date = end_date

# Funktion zum Speichern der Reservierungen in JSON-Datei
def save_reservations(reservations):
    with open(RESERVATIONS_FILE, "w") as f:
        json.dump([{
            "device": vars(r.device) if isinstance(r.device, Device) else r.device,
            "user": vars(r.user) if isinstance(r.user, User) else r.user,
            "start_date": r.start_date,
            "end_date": r.end_date
        } for r in reservations], f, default=str)

# Funktion zum Laden der Reservierungen aus JSON-Datei
def load_reservations():
    if os.path.exists(RESERVATIONS_FILE):
        with open(RESERVATIONS_FILE, "r") as f:
            reservations_data = json.load(f)
            return [Reservation(res["device"], res["user"], res["start_date"], res["end_date"]) for res in reservations_data]
    return []

# Initialisiere Nutzer-, Geräte- und Reservierungsliste in Session State
if "users" not in st.session_state:
    st.session_state.users = load_users()

if "devices" not in st.session_state:
    st.session_state.devices = load_devices()

if "reservations" not in st.session_state:
    try:
        st.session_state.reservations = load_reservations()
    except ValueError as e:
        st.error(f"Fehler beim Laden der Reservierungen: {e}")
        st.session_state.reservations = []

# Reservierungsmanagement
def show_reservation_management():
    st.write("## Reservierungsverwaltung")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Neue Reservierung anlegen")
        selected_device = st.selectbox(
            "Wähle ein Gerät:", st.session_state.devices, format_func=lambda d: f"{d.name} (ID: {d.id})"
        )
        selected_user = st.selectbox(
            "Wähle einen Nutzer:", st.session_state.users, format_func=lambda u: f"{u.name} ({u.email})"
        )
        start_date = st.date_input("Startdatum der Reservierung", value=datetime.now())
        end_date = st.date_input("Enddatum der Reservierung", value=datetime.now())

        if st.button("Reservierung erstellen"):
            if start_date <= end_date:
                # Prüfen, ob das Gerät bereits reserviert ist
                overlapping_reservation = any(
                    res.device.id == selected_device.id and not (end_date < res.start_date or start_date > res.end_date)
                    for res in st.session_state.reservations
                )

                if overlapping_reservation:
                    st.error("Dieses Gerät ist im angegebenen Zeitraum bereits reserviert!")
                else:
                    new_reservation = Reservation(selected_device, selected_user, str(start_date), str(end_date))
                    st.session_state.reservations.append(new_reservation)
                    save_reservations(st.session_state.reservations)
                    st.success(f"Reservierung für '{selected_device.name}' durch '{selected_user.name}' erfolgreich erstellt!")
                    st.rerun()
            else:
                st.error("Das Enddatum muss nach dem Startdatum liegen!")
    
    with col2:
        st.subheader("Bestehende Reservierungen")
        if st.session_state.reservations:
            for res in st.session_state.reservations:
                st.write(f"{res.device.name} reserviert von {res.user.name} ({res.start_date} - {res.end_date})")
        else:
            st.info("Keine Reservierungen vorhanden.")

        # Auswahl einer Reservierung zum Löschen
        if st.session_state.reservations:
            res_to_delete = st.selectbox("Reservierung zum Löschen wählen:", st.session_state.reservations, 
                                        format_func=lambda r: f"{r.device.name} - {r.user.name} ({r.start_date} - {r.end_date})")
            if st.button("Reservierung löschen"):
                st.session_state.reservations = [res for res in st.session_state.reservations if res.device.id != res_to_delete.device.id or res.user.email != res_to_delete.user.email or res.start_date != res_to_delete.start_date or res.end_date != res_to_delete.end_date]
                save_reservations(st.session_state.reservations)
                st.success("Reservierung erfolgreich gelöscht!")
                st.rerun()

# Dummy-Funktionen für Nutzer- und Gerätemanagement
def show_user_management():
    st.write("## Nutzerverwaltung")
    st.info("Hier könnte die Nutzerverwaltung implementiert werden.")

def show_device_management():
    st.write("## Geräteverwaltung")
    st.info("Hier könnte die Geräteverwaltung implementiert werden.")

# Hauptmenü
st.write("# Gerätemanagement System")
st.write("## Navigation")

menu_option = st.selectbox("Wählen Sie eine Option:", ["Nutzerverwaltung", "Geräteverwaltung", "Reservierungsverwaltung"])

st.markdown("<br><br>", unsafe_allow_html=True)

if menu_option == "Nutzerverwaltung":
    show_user_management()
elif menu_option == "Geräteverwaltung":
    show_device_management()
elif menu_option == "Reservierungsverwaltung":
    show_reservation_management()
