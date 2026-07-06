import streamlit as st

from config import SEKCJE, SZABLONY
from functions import formularz_sekcji, zarzadzaj_sekcja
from pdf_generator import generuj_pdf
from docx_generator import generuj_docx

st.set_page_config(layout="wide")

st.title("Generator CV")
st.subheader("Stwórz swoje portfolio w 5 minut")

sekcje = SEKCJE
for sekcja in sekcje:
    if sekcja not in st.session_state:
        st.session_state[sekcja] = []

# --- UKŁAD STRONY STREAMLIT ---
col1, col2 = st.columns(2)

with col1:
    st.header("Wpisz swoje dane")
    
    szablon = st.selectbox(
        "Wybierz układ i motyw", 
        list(SZABLONY.keys())
    )
    
    _, kolor_rgb, uklad = SZABLONY[szablon]

    st.write("---")
    name = st.text_input("Imię i Nazwisko", placeholder="Jan Kowalski")
    position = st.text_input("Stanowisko", placeholder="Python Developer")
    description = st.text_area("O sobie", placeholder="Powiedz coś o sobie :)")
    
    st.write("---")
    st.subheader("Dane kontaktowe")
    phone = st.text_input("Telefon", placeholder="+48 123 456 789")
    email = st.text_input("Email", placeholder="jan.kowalski@email.com")
    location = st.text_input("Lokalizacja", placeholder="Warszawa, Polska")
    linkedin = st.text_input("LinkedIn (link)", placeholder="linkedin.com/in/username")
    github_link = st.text_input("GitHub (link)", placeholder="github.com/username")

    st.write("---")
    st.subheader("Zdjęcie profilowe")
    uploaded_file = st.file_uploader("Wybierz zdjęcie (JPG, PNG)", type=["jpg", "jpeg", "png"])

    formularz_sekcji("praca_form", "Doświadczenie zawodowe", {"company": "Firma", "role": "Rola / stanowisko", "years": "Lata zatrudnienia", "duty": "Obowiązki"}, "exp")
    formularz_sekcji("edu_form", "Edukacja", {"school": "Szkoła / Uczelnia", "field": "Kierunek / Profil", "years_edu": "Lata nauki"}, "edu")
    formularz_sekcji("skill_form", "Umiejętności", {"skill": "Wpisz umiejętność (np. Python, Git)"}, "skills")
    formularz_sekcji("lang_form", "Języki obce", {"lang": "Język", "level": "Poziom"}, "langs")
    formularz_sekcji("cert_form", "Certyfikaty i Kursy", {"cert": "Nazwa certyfikatu / kursu (np. AWS Certified, Kurs Python)"}, "cert")
    
    st.write("---")
    st.subheader("Ustawienia dodatkowe")
    dodaj_rodo = st.checkbox("Dodaj standardową klauzulę RODO na dole CV", value=True)

    if any(st.session_state[s] for s in sekcje):
        st.write("---")
        st.subheader("Zarządzaj wpisami")
        
        zarzadzaj_sekcja("Doświadczenie", "exp", lambda j: f"Praca: {j['role']} w {j['company']}", "exp")
        zarzadzaj_sekcja("Edukacja", "edu", lambda e: f"Szkoła: {e['school']}", "edu")
        zarzadzaj_sekcja("Umiejętności", "skills", lambda s: f"Skill: {s}", "skill")
        zarzadzaj_sekcja("Języki", "langs", lambda l: f"Język: {l['lang']} ({l['level']})", "lang")
        zarzadzaj_sekcja("Certyfikaty", "cert", lambda c: f"Certyfikat: {c}", "cert")

        if st.button("Wyczyść całe CV"):
            for s in sekcje: st.session_state[s] = []
            st.rerun()

with col2:
    st.header("Podgląd Live")
    st.caption("Podgląd pokazuje dokładnie wygląd pliku PDF.")

    photo_bytes = uploaded_file.getvalue() if uploaded_file else None

    pdf_data = generuj_pdf(
        name=name,
        position=position,
        description=description,
        phone=phone,
        email=email,
        location=location,
        linkedin=linkedin,
        github=github_link,
        exp_list=st.session_state.exp,
        edu_list=st.session_state.edu,
        skills_list=st.session_state.skills,
        langs_list=st.session_state.langs,
        cert_list=st.session_state.cert,
        kolor_rgb=kolor_rgb,
        uklad=uklad,
        rodo=dodaj_rodo,
        photo_bytes=photo_bytes,
    )
    st.pdf(pdf_data, height=820)

    if uklad == "split":
        st.caption("Eksport Word ma układ jednokolumnowy — różni się od szablonu dwukolumnowego.")

    if name:
        st.write("---")
        c_pdf, c_docx, _ = st.columns([1, 1, 4])

        with c_pdf:
            st.download_button(
                label="Pobierz jako PDF",
                data=pdf_data,
                file_name="CV.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with c_docx:
            docx_data = generuj_docx(
                name,
                position,
                description,
                st.session_state.exp,
                st.session_state.edu,
                st.session_state.skills,
                st.session_state.langs,
                cert_list=st.session_state.cert,
                phone=phone,
                email=email,
                location=location,
                linkedin=linkedin,
                github=github_link,
                rodo=dodaj_rodo,
                photo_bytes=photo_bytes,
            )
            st.download_button(label="Pobierz jako Word", data=docx_data, file_name="CV.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)