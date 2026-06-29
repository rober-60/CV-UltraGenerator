import streamlit as st
from PIL import Image
# Importujemy nasze moduły
from functions import formularz_sekcji, zarzadzaj_sekcja
from pdf_generator import generuj_pdf
from docx_generator import generuj_docx

st.set_page_config(layout="wide")

st.title("Generator CV")
st.subheader("Stwórz swoje portfolio w 5 minut")

sekcje = ["exp", "edu", "skills", "langs"]
for sekcja in sekcje:
    if sekcja not in st.session_state:
        st.session_state[sekcja] = []

# --- UKŁAD STRONY STREAMLIT ---
col1, col2 = st.columns(2)

with col1:
    st.header("Wpisz swoje dane")
    
    szablon = st.selectbox(
        "Wybierz układ i motyw", 
        ["Jednokolumnowy Granat", "Jednokolumnowy Zieleń", "Dwukolumnowy Nowoczesny"]
    )
    
    kolory = {
        "Jednokolumnowy Granat": ("#1E3A8A", (30, 58, 138), "single"),
        "Jednokolumnowy Zieleń": ("#065F46", (6, 95, 70), "single"),
        "Dwukolumnowy Nowoczesny": ("#1F2937", (31, 41, 55), "split")
    }
    kolor_glowny, kolor_rgb, uklad = kolory[szablon]

    st.write("---")
    name = st.text_input("Imię i Nazwisko", placeholder="Jan Kowalski")
    position = st.text_input("Stanowisko", placeholder="Python Developer")
    description = st.text_area("O sobie", placeholder="Powiedz coś o sobie :)")
    
    st.write("---")
    st.subheader("Zdjęcie profilowe")
    uploaded_file = st.file_uploader("Wybierz zdjęcie (JPG, PNG)", type=["jpg", "jpeg", "png"])

    formularz_sekcji("praca_form", "Doświadczenie zawodowe", {"company": "Firma", "role": "Rola / stanowisko", "years": "Lata zatrudnienia", "duty": "Obowiązki"}, "exp")
    formularz_sekcji("edu_form", "Edukacja", {"school": "Szkoła / Uczelnia", "field": "Kierunek / Profil", "years_edu": "Lata nauki"}, "edu")
    formularz_sekcji("skill_form", "Umiejętności", {"skill": "Wpisz umiejętność (np. Python, Git)"}, "skills")
    formularz_sekcji("lang_form", "Języki obce", {"lang": "Język", "level": "Poziom"}, "langs")

    if any(st.session_state[s] for s in sekcje):
        st.write("---")
        st.subheader("Zarządzaj wpisami")
        
        zarzadzaj_sekcja("Doświadczenie", "exp", lambda j: f"Praca: {j['role']} w {j['company']}", "exp")
        zarzadzaj_sekcja("Edukacja", "edu", lambda e: f"Szkoła: {e['school']}", "edu")
        zarzadzaj_sekcja("Umiejętności", "skills", lambda s: f"Skill: {s}", "skill")
        zarzadzaj_sekcja("Języki", "langs", lambda l: f"Język: {l['lang']} ({l['level']})", "lang")

        if st.button("Wyczyść całe CV"):
            for s in sekcje: st.session_state[s] = []
            st.rerun()


with col2:
    st.header("Podgląd Live")
    
    if uploaded_file:
        col_text, col_img = st.columns([3, 1])
        with col_text:
            if name: st.markdown(f"<h1 style='color: {kolor_glowny};'>{name}</h1>", unsafe_allow_html=True)
            if position: st.markdown(f"### *{position}*")
        with col_img:
            st.image(Image.open(uploaded_file), width=120)
    else:
        if name: st.markdown(f"<h1 style='color: {kolor_glowny};'>{name}</h1>", unsafe_allow_html=True)
        if position: st.markdown(f"### *{position}*")
            
    st.write("---")
    if description: st.write(description)

    if st.session_state.exp:
        st.markdown(f"<h3 style='color: {kolor_glowny};'>Doświadczenie zawodowe</h3>", unsafe_allow_html=True)
        for job in st.session_state.exp:
            naglowek_live = f"**{job['role']}** w *{job['company']}*"
            if job['years']: naglowek_live += f" ({job['years']})"
            st.markdown(naglowek_live)
            if job['duty']: st.write(job['duty'])
            st.write("---")

    if st.session_state.edu:
        st.markdown(f"<h3 style='color: {kolor_glowny};'>Edukacja</h3>", unsafe_allow_html=True)
        for edu in st.session_state.edu:
            szkola_live = f"**{edu['school']}**"
            if edu['years_edu']: szkola_live += f" ({edu['years_edu']})"
            st.markdown(szkola_live)
            if edu['field']: st.write(f"Kierunek: {edu['field']}")
            st.write("---")

    if st.session_state.skills:
        st.markdown(f"<h3 style='color: {kolor_glowny};'>Umiejętności</h3>", unsafe_allow_html=True)
        st.write(", ".join(st.session_state.skills))
        st.write("---")

    if st.session_state.langs:
        st.markdown(f"<h3 style='color: {kolor_glowny};'>Języki obce</h3>", unsafe_allow_html=True)
        for lang in st.session_state.langs:
            st.write(f"{lang['lang']} - {lang['level']}")
            
    if name:
        st.write("---")
        c_pdf, c_docx, _ = st.columns([1,1,4])
        
        with c_pdf:
            pdf_data = generuj_pdf(
                name, position, description, 
                st.session_state.exp, st.session_state.edu, 
                st.session_state.skills, st.session_state.langs, kolor_rgb, uklad=uklad
            )
            st.download_button(label="Pobierz jako PDF", data=pdf_data, file_name="CV.pdf", mime="application/pdf")
            
        with c_docx:
            docx_data = generuj_docx(
                name, position, description,
                st.session_state.exp, st.session_state.edu,
                st.session_state.skills, st.session_state.langs
            )
            st.download_button(label="Pobierz jako Word", data=docx_data, file_name="CV.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")