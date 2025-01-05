import streamlit as st



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


# Funktionen für die persistente Speicherung
def load_users():
    """Lade Nutzer aus der JSON-Datei."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return [User.from_dict(user) for user in data]
    return []


def save_users(users):
    """Speichere Nutzer in der JSON-Datei."""
    with open(DATA_FILE, "w") as file:
        json.dump([user.to_dict() for user in users], file)


# Initialisiere Nutzerliste in Session State
if "users" not in st.session_state:
    st.session_state.users = []  # Liste für User-Objekte

if "devices" not in st.session_state:
    st.session_state.devices = []  # Liste für Device-Objekte

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# App-Bereich: Nutzer-Verwaltung
st.write("# Nutzermanagement")

# Spalten für Aktionen
col1, col2 = st.columns(2)

# Nutzer hinzufügen
with col1:
    st.subheader("Nutzer anlegen")
    new_name = st.text_input("Geben Sie den Nutzernamen ein:")
    new_email = st.text_input("Geben Sie die E-Mail-Adresse ein:")
    if st.button("Nutzer hinzufügen"):
        if new_name and new_email:
            # Prüfen, ob die E-Mail bereits existiert
            if not any(user.email == new_email for user in st.session_state.users):
                new_user = User(email=new_email, name=new_name)
                st.session_state.users.append(new_user)
                save_users(st.session_state.users)  # Speichere Nutzer
                st.success(f"Nutzer '{new_user.name}' wurde hinzugefügt!")
            else:
                st.warning(f"Ein Nutzer mit der E-Mail '{new_email}' existiert bereits!")
        else:
            st.error("Bitte geben Sie sowohl einen Namen als auch eine E-Mail-Adresse ein.")

    # Nutzer anmelden
    with col2:
        st.subheader("Anmeldung")
        user_options = [f"{user.name} ({user.email})" for user in st.session_state.users]
        selected_user = st.selectbox("Wählen Sie einen Nutzer aus:", options=["---"] + user_options)
        if st.button("Anmelden"):
            if selected_user != "---":
                user = next((user for user in st.session_state.users if f"{user.name} ({user.email})" == selected_user), None)
                if user:
                    st.session_state.selected_user = user
                    st.session_state.authenticated = True
                    st.success(f"Willkommen, {user.name}!")
                    st.experimental_rerun()
                else:
                    st.error("Nutzer nicht gefunden.")
            else:
                st.error("Bitte einen Nutzer auswählen.")

else:
    # Nach erfolgreicher Anmeldung direkt zur Geräteverwaltung
    st.write(f"## Willkommen, {st.session_state.selected_user.name}")

    st.write("## Geräteverwaltung")

    # Gerät hinzufügen
    st.subheader("Gerät hinzufügen")
    new_device_name = st.text_input("Gerätename eingeben:", key="new_device_name")
    new_device_type = st.selectbox(
        "Gerätetyp auswählen:",
        ["Laptop", "Tablet", "Smartphone", "Drucker", "Andere"],
        key="new_device_type"
    )
    if st.button("Gerät hinzufügen"):
        if new_device_name and new_device_type:
            if not any(device.name == new_device_name for device in st.session_state.devices):
                new_device = Device(name=new_device_name, device_type=new_device_type)
                st.session_state.devices.append(new_device)
                st.success(f"Gerät '{new_device.name}' wurde erfolgreich hinzugefügt!")
            else:
                st.warning(f"Ein Gerät mit dem Namen '{new_device_name}' existiert bereits!")
        else:
            st.error("Bitte Gerätenamen und Typ ausfüllen.")

    # Bestehende Geräte anzeigen
    st.subheader("Bestehende Geräte")
    if st.session_state.devices:
        for idx, device in enumerate(st.session_state.devices):
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"{idx + 1}. {device}")

            # Button zum Aktivieren/Deaktivieren
            if device.status == "Inaktiv":
                if col2.button("Aktivieren", key=f"activate_{idx}"):
                    st.session_state.devices[idx].status = "Aktiv"
                    st.success(f"Gerät '{device.name}' wurde aktiviert.")
            else:
                if col2.button("Deaktivieren", key=f"deactivate_{idx}"):
                    st.session_state.devices[idx].status = "Inaktiv"
                    st.success(f"Gerät '{device.name}' wurde deaktiviert.")

            # Button zum Löschen
            if col3.button("Löschen", key=f"delete_{idx}"):
                st.session_state.devices.pop(idx)
                st.warning(f"Gerät '{device.name}' wurde gelöscht.")
                st.experimental_rerun()
    else:
        st.info("Es sind keine Nutzer vorhanden.")

