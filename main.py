import streamlit as st
import json
import os

# Dateipfad für das Speichern der Nutzerdaten
DATA_FILE = "users_data.json"


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
    st.session_state.users = load_users()

if "selected_user" not in st.session_state:
    st.session_state.selected_user = None

# App-Bereich: Nutzer-Verwaltung
st.write("# Nutzermanagement")
st.write("## Nutzer-Verwaltung")

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

# Bestehende Nutzer anzeigen
with col2:
    st.subheader("Bestehende Nutzer")
    if st.session_state.users:
        user_options = [f"{user.name} ({user.email})" for user in st.session_state.users]
        selected_user = st.selectbox("Wählen Sie einen Nutzer aus:", options=user_options)
        st.write(f"Ausgewählter Nutzer: {selected_user}")
    else:
        st.info("Es sind keine Nutzer vorhanden.")

