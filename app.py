import streamlit as st

# Ustawienia strony na szeroki układ (fajne pod generator)
st.set_page_config(layout="wide")

st.title("Generator CV")
st.subheader("Stwórz swoje portfolio w 5 minut")

# Podział ekranu na dwie kolumny: Formularz i Podgląd
col1, col2 = st.columns(2)

with col1:
    st.header("Wpisz swoje dane")
    imie = st.text_input("Imię i Nazwisko", placeholder="Jan Kowalski")
    stanowisko = st.text_input("Stanowisko", placeholder="Python Developer")
    o_sobie = st.text_area("O sobie", placeholder="Krótki opis Twoich supermocy...")

with col2:
    st.header("Podgląd Live")
    if imie:
        st.markdown(f"# {imie}")
    if stanowisko:
        st.markdown(f"### *{stanowisko}*")
    st.write("---")
    if o_sobie:
        st.write(o_sobie)