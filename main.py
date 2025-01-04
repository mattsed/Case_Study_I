import streamlit as st

if "sb_current_device" not in st.session_state:
    st.session_state.sb_current_device = ""

# Eine Überschrift der ersten Ebene
st.write("# Gerätemanagement")

# Eine Überschrift der zweiten Ebene
st.write("## Geräteauswahl")

# Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis

st.session_state.sb_current_device = st.selectbox(label='Gerät auswählen',
        options = ["Gerät_A", "Gerät_B", "Gerät_C"])

st.write(F"Das ausgewählte Gerät ist {st.session_state.sb_current_device}")

st.write("## Wartungskosten")

# Callbacks for the number inputs
def update_price_from_euro():
    st.session_state.price_dollar = st.session_state.price_euro * 1.1

def update_price_from_dollar():
    st.session_state.price_euro = st.session_state.price_dollar * 0.9

# Number inputs for the maintenance costs
st.number_input(label="Wartungskosten in Euro", 
                            key = "price_euro",
                            on_change=update_price_from_euro)

st.number_input(label="Wartungskosten in Dollar", 
                            key = "price_dollar",
                            on_change=update_price_from_dollar)


col1, col2 = st.columns(2)

with col1:
   st.header("A cat")
   #st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
   st.header("A dog")
   #st.image("https://static.streamlit.io/examples/dog.jpg")

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)