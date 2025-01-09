import streamlit as st
from devices import Device, load_devices, save_devices
from users import User, load_users, save_users 
from datetime import datetime

# Dateipfade für das Speichern der Nutzerdaten und Gerätedaten
#USER_DATA_FILE = "users_data.json"
#DEVICE_DATA_FILE = "devices_data.json"

##################################################################################################################################

# Initialisiere Nutzer- und Gerätelisten in Session State
if "users" not in st.session_state:
    st.session_state.users = load_users()

if "devices" not in st.session_state:
    st.session_state.devices = load_devices()

##################################################################################################################################

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
            st.write(f"- {device.name}, ID: {device.id} ")

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
