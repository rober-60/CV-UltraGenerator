import streamlit as st

def formularz_sekcji(id_formularza, naglowek, pola, klucz_pamieci):
    st.write("---")
    st.subheader(naglowek)
    with st.form(id_formularza, clear_on_submit=True):
        dane_wpisu = {}
        for klucz_pola, nazwa_pola in pola.items():
            if klucz_pola == "level":
                dane_wpisu[klucz_pola] = st.selectbox(nazwa_pola, ["A1", "A2", "B1", "B2", "C1", "C2", "Ojczysty"])
            elif klucz_pola == "duty":
                dane_wpisu[klucz_pola] = st.text_area(nazwa_pola)
            else:
                dane_wpisu[klucz_pola] = st.text_input(nazwa_pola)
        
        if st.form_submit_button(f"Dodaj {naglowek.lower()}"):
            pierwszy_klucz = list(pola.keys())[0]
            if dane_wpisu[pierwszy_klucz]:
                wpis = dane_wpisu[pierwszy_klucz] if len(pola) == 1 else dane_wpisu
                st.session_state[klucz_pamieci].append(wpis)
                st.rerun()

def zarzadzaj_sekcja(naglowek, klucz_pamieci, funkcja_formatowania, klucz_id):
    if st.session_state[klucz_pamieci]:
        for index, element in enumerate(st.session_state[klucz_pamieci]):
            c1, c2 = st.columns([4, 1])
            c1.write(funkcja_formatowania(element))
            if c2.button("Usuń", key=f"del_{klucz_id}_{index}"):
                st.session_state[klucz_pamieci].pop(index)
                st.rerun()