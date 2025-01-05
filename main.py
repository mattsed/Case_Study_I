import streamlit as st



# Definition der User-Klasse
class User:
    def __init__(self, email: str, name: str):
        self.email = email
        self.name = name

    def __repr__(self):
        return f"{self.name} ({self.email})"

# Initialisierung von Session State für die Benutzerverwaltung
if "users" not in st.session_state:
    st.session_state.users = []  # Liste für User-Objekte

# App-Bereich: Nutzer-Verwaltung
st.write("# Nutzermanagement")
st.write("## Nutzer-Verwaltung")

# Spalten für Benutzeraktionen.\venv\Scripts\activate
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
                st.success(f"Nutzer '{new_user.name}' mit der E-Mail '{new_user.email}' wurde erfolgreich hinzugefügt!")
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
        st.info("Es sind keine Nutzer angelegt.")

# Geräteauswahl
st.write("## Geräteauswahl")

if "sb_current_device" not in st.session_state:
    st.session_state.sb_current_device = ""

st.session_state.sb_current_device = st.selectbox(
    label="Gerät auswählen",
    options=["Gerät_A", "Gerät_B", "Gerät_C"]
)

st.write(f"Das ausgewählte Gerät ist: {st.session_state.sb_current_device}")
