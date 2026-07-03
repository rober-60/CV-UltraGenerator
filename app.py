import streamlit as st
from PIL import Image
# Importujemy nasze moduły
from functions import formularz_sekcji, zarzadzaj_sekcja
from pdf_generator import generuj_pdf
from docx_generator import generuj_docx

st.set_page_config(layout="wide")

st.title("Generator CV")
st.subheader("Stwórz swoje portfolio w 5 minut")

sekcje = ["exp", "edu", "skills", "langs","cert"]
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
    
    # Przygotowanie listy z kontaktami (przydaje się w obu układach)
    bloki_kontaktowe = []
    if phone: bloki_kontaktowe.append(f"Tel: {phone}")
    if email: bloki_kontaktowe.append(f"Email: {email}")
    if location: bloki_kontaktowe.append(f"Lokalizacja: {location}")
    if linkedin: bloki_kontaktowe.append(f"LinkedIn: {linkedin}")
    if github_link: bloki_kontaktowe.append(f"GitHub: {github_link}")

    st.write("---") # Oddzielenie nagłówka "Podgląd live"

    # ==========================================
    # PODGLĄD: UKŁAD DWUKOLUMNOWY (SPLIT)
    # ==========================================
    if uklad == "split":
        # Dzielimy podgląd na dwie kolumny (lewa węższa, prawa szersza)
        prev_col1, prev_col2 = st.columns([1, 2.5])
        
        with prev_col1:
            if uploaded_file:
                st.image(Image.open(uploaded_file), width=120)
                
            if bloki_kontaktowe:
                st.markdown(f"<h4 style='color: {kolor_glowny};'>Kontakt</h4>", unsafe_allow_html=True)
                for kontakt in bloki_kontaktowe:
                    st.write(kontakt)
                st.write("---")
                
            if st.session_state.skills:
                st.markdown(f"<h4 style='color: {kolor_glowny};'>Umiejętności</h4>", unsafe_allow_html=True)
                for skill in st.session_state.skills:
                    st.write(f"- {skill}")
                st.write("---")
                
            if st.session_state.langs:
                st.markdown(f"<h4 style='color: {kolor_glowny};'>Języki</h4>", unsafe_allow_html=True)
                for lang in st.session_state.langs:
                    st.write(f"{lang['lang']} ({lang['level']})")

        with prev_col2:
            if name: st.markdown(f"<h1 style='color: {kolor_glowny}; margin-top: 0;'>{name}</h1>", unsafe_allow_html=True)
            if position: st.markdown(f"### *{position}*")
            if description:
                st.write(description)
                
            if st.session_state.exp:
                st.write("---")
                st.markdown(f"<h3 style='color: {kolor_glowny};'>Doświadczenie zawodowe</h3>", unsafe_allow_html=True)
                for job in st.session_state.exp:
                    naglowek_live = f"**{job['role']}** w *{job['company']}*"
                    if job['years']: naglowek_live += f" ({job['years']})"
                    st.markdown(naglowek_live)
                    if job['duty']: st.write(job['duty'])

            if st.session_state.edu:
                st.write("---")
                st.markdown(f"<h3 style='color: {kolor_glowny};'>Edukacja</h3>", unsafe_allow_html=True)
                for edu in st.session_state.edu:
                    szkola_live = f"**{edu['school']}**"
                    if edu['years_edu']: szkola_live += f" ({edu['years_edu']})"
                    st.markdown(szkola_live)
                    if edu['field']: st.write(f"Kierunek: {edu['field']}")

            if st.session_state.cert:
                st.write("---")
                st.markdown(f"<h3 style='color: {kolor_glowny};'>Certyfikaty i Kursy</h3>", unsafe_allow_html=True)
                for cert in st.session_state.cert:
                    st.write(f"- {cert}")

    # ==========================================
    # PODGLĄD: UKŁAD JEDNOKOLUMNOWY (SINGLE)
    # ==========================================
    else:
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
            
        if bloki_kontaktowe:
            st.markdown(f"<p style='color: gray; font-size: 14px;'>{' | '.join(bloki_kontaktowe)}</p>", unsafe_allow_html=True)
            
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
                
        if st.session_state.cert:
            st.markdown(f"<h3 style='color: {kolor_glowny};'>Certyfikaty i Kursy</h3>", unsafe_allow_html=True)
            st.write(", ".join(st.session_state.cert))
            st.write("---")

    # Wyświetlanie klauzuli RODO na samym dole podglądu live
    if dodaj_rodo:
        st.write(" ")
        st.markdown("<p style='color: gray; font-size: 11px; text-align: center; font-style: italic;'>Wyrażam zgodę na przetwarzanie moich danych osobowych dla potrzeb niezbędnych do realizacji procesu rekrutacji (zgodnie z rozporządzeniem o ochronie danych osobowych RODO).</p>", unsafe_allow_html=True)

    # --- PRZYCISKI POBIERANIA ---
    if name:
        st.write("---")
        c_pdf, c_docx, _ = st.columns([1,1,4])
        
        with c_pdf:
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
                rodo=dodaj_rodo
            )
            st.download_button(label="Pobierz jako PDF", data=pdf_data, file_name="CV.pdf", mime="application/pdf", use_container_width=True)
            
        with c_docx:
            docx_data = generuj_docx(
                name, position, description,
                st.session_state.exp, st.session_state.edu,
                st.session_state.skills, st.session_state.langs,
                rodo=dodaj_rodo
            )
            st.download_button(label="Pobierz jako Word", data=docx_data, file_name="CV.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)