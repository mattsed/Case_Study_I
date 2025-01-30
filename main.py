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

# Funktion zum Speichern der Reservierungen
def save_reservations(reservations):
    with open(RESERVATIONS_FILE, "w") as f:
        json.dump([{
            "device": vars(r.device),
            "user": vars(r.user),
            "start_date": r.start_date,
            "end_date": r.end_date
        } for r in reservations], f, default=str)

# Funktion zum Laden der Reservierungen
def load_reservations():
    if os.path.exists(RESERVATIONS_FILE):
        with open(RESERVATIONS_FILE, "r") as f:
            reservations_data = json.load(f)
            return [Reservation(res["device"], res["user"], res["start_date"], res["end_date"]) for res in reservations_data]
    return []

# Initialisierung der Session State Variablen
if "users" not in st.session_state:
    st.session_state.users = load_users() if os.path.exists("users.json") else []

if "devices" not in st.session_state:
    st.session_state.devices = load_devices() if os.path.exists("devices.json") else []

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
    
    with col2:
        st.subheader("Bestehende Reservierungen")
        if st.session_state.reservations:
            for res in st.session_state.reservations:
                st.write(f"{res.device.name} reserviert von {res.user.name} ({res.start_date} - {res.end_date})")
        else:
            st.info("Keine Reservierungen vorhanden.")

# Nutzerverwaltung
def show_user_management():
    st.write("## Nutzerverwaltung")
    
    # Neue Nutzer hinzufügen
    with st.form("add_user_form"):
        name = st.text_input("Name des Nutzers")
        email = st.text_input("E-Mail-Adresse")
        submit_button = st.form_submit_button("Nutzer hinzufügen")

        if submit_button:
            if name and email:
                new_user = User(name, email)
                st.session_state.users.append(new_user)
                save_users(st.session_state.users)
                st.success(f"Nutzer {name} hinzugefügt!")
                st.rerun()
            else:
                st.error("Bitte Name und E-Mail eingeben!")

    # Nutzer anzeigen und löschen
    st.write("### Bestehende Nutzer")
    if st.session_state.users:
        user_to_delete = st.selectbox("Nutzer zum Löschen wählen:", st.session_state.users, 
                                      format_func=lambda u: f"{u.name} ({u.email})")
        if st.button("Nutzer löschen"):
            st.session_state.users = [u for u in st.session_state.users if u.email != user_to_delete.email]
            save_users(st.session_state.users)
            st.success(f"Nutzer {user_to_delete.name} wurde gelöscht.")
            st.rerun()
    else:
        st.info("Keine Nutzer vorhanden.")

# Geräteverwaltung
def show_device_management():
    st.write("## Geräteverwaltung")
    
    # Neues Gerät hinzufügen
    with st.form("add_device_form"):
        device_name = st.text_input("Gerätename")
        device_id = st.text_input("Geräte-ID")
        submit_button = st.form_submit_button("Gerät hinzufügen")

        if submit_button:
            if device_name and device_id:
                new_device = Device(device_name, device_id)
                st.session_state.devices.append(new_device)
                save_devices(st.session_state.devices)
                st.success(f"Gerät {device_name} hinzugefügt!")
                st.rerun()
            else:
                st.error("Bitte Gerätename und Geräte-ID eingeben!")

    # Geräte anzeigen und löschen
    st.write("### Bestehende Geräte")
    if st.session_state.devices:
        device_to_delete = st.selectbox("Gerät zum Löschen wählen:", st.session_state.devices, 
                                        format_func=lambda d: f"{d.name} (ID: {d.id})")
        if st.button("Gerät löschen"):
            st.session_state.devices = [d for d in st.session_state.devices if d.id != device_to_delete.id]
            save_devices(st.session_state.devices)
            st.success(f"Gerät {device_to_delete.name} wurde gelöscht.")
            st.rerun()
    else:
        st.info("Keine Geräte vorhanden.")

# Hauptmenü
st.write("# Gerätemanagement System")
st.write("## Navigation")

menu_option = st.selectbox("Wählen Sie eine Option:", ["Nutzerverwaltung", "Geräteverwaltung", "Reservierungsverwaltung"])

# Aufruf der richtigen Funktion basierend auf der Auswahl
if menu_option == "Nutzerverwaltung":
    show_user_management()
elif menu_option == "Geräteverwaltung":
    show_device_management()
elif menu_option == "Reservierungsverwaltung":
    show_reservation_management()
