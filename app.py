import streamlit as st
from PIL import Image

from config import RODO_TEKST, SEKCJE, SZABLONY
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

col1, col2 = st.columns(2)

with col1:
    st.header("Wpisz swoje dane")

    szablon = st.selectbox(
        "Wybierz układ i motyw",
        list(SZABLONY.keys()),
    )

    kolor_glowny, kolor_rgb, uklad = SZABLONY[szablon]

    st.write("---")
    name = st.text_input("Imię i Nazwisko", placeholder="Jan Kowalski")
    position = st.text_input("Stanowisko", placeholder="Python Developer")
    description = st.text_area("O sobie", placeholder="Powiedz coś o sobie :)")

    st.write("---")
    st.subheader("Dane kontaktowe")

    phone = ""
    phone_input = st.text_input("Telefon", placeholder="123 456 789")
    phone_digits = "".join([char for char in phone_input if char.isdigit()])
    if phone_digits:
        if len(phone_digits) != 9:
            st.caption("Numer telefonu powinien składać się z dokładnie 9 cyfr.")
            phone = phone_digits[:9]
        phone = f"{phone_digits[:3]} {phone_digits[3:6]} {phone_digits[6:9]}"


    email = st.text_input("Email", placeholder="jankowalski@email.com")
    if email:
        if "@" not in email:
            st.caption("Email powinien zawierać znak: '@'")
        elif email.startswith("@") or email.endswith("@"):
            st.caption("Email nie powinien zaczynać ani kończyć się znakiem '@'")
        elif "." not in email.split("@")[-1]:
            st.caption("Email powinien zawierać domenę, np. '.com'")

    location = st.text_input("Lokalizacja", placeholder="Warszawa, Polska")
    linkedin = st.text_input("LinkedIn (link)", placeholder="linkedin.com/in/username")
    github_link = st.text_input("GitHub (link)", placeholder="github.com/username")

    st.write("---")
    st.subheader("Zdjęcie profilowe")
    uploaded_file = st.file_uploader("Wybierz zdjęcie (JPG, PNG)", type=["jpg", "jpeg", "png"])

    formularz_sekcji("praca_form", "Doświadczenie zawodowe", {"company": "Firma", "role": "Rola / stanowisko", "years": "Lata zatrudnienia", "duty": "Obowiązki"}, "exp")
    formularz_sekcji("edu_form", "Edukacja", {"school": "Szkoła / Uczelnia", "field": "Kierunek / Profil", "years_edu": "Lata nauki"}, "edu")
    
    st.write("---")
    st.subheader("Umiejętności")
    wlacz = st.toggle("Włącz poziom zaawansowania")

    with st.form("skills_form", clear_on_submit=True):
        skill_name = st.text_input("Nazwa umiejętności",placeholder="np. Python, SQL, Git")
        skill_level = None
        if wlacz:
            skill_level = st.slider("Poziom zaawansowania",min_value=1,max_value=5,value=3)

        submit_skill = st.form_submit_button("Dodaj umiejętność")

        if submit_skill and skill_name:
            st.session_state.skills.append({"skill": skill_name,"level": skill_level})
            st.rerun()


    formularz_sekcji("lang_form", "Języki obce", {"lang": "Język", "level": "Poziom"}, "langs")
    formularz_sekcji("cert_form", "Certyfikaty i Kursy", {"cert": "Nazwa certyfikatu / kursu (np. AWS Certified, Kurs Python)"}, "cert")

    st.write("---")
    st.subheader("Ustawienia dodatkowe")
    dodaj_rodo = st.checkbox("Dodaj standardową klauzulę RODO na dole CV", value=True)

    if any(st.session_state[s] for s in sekcje):
        st.write("---")
        st.subheader("Zarządzaj wpisami")

        zarzadzaj_sekcja("exp", lambda j: f"Praca: {j['role']} w {j['company']}", "exp_manage")
        zarzadzaj_sekcja("edu", lambda e: f"Szkoła: {e['school']}", "edu_manage")
        zarzadzaj_sekcja(
            "skills",
            lambda s: (
                f"Umiejętność: {s['skill']}"
                if s["level"] is None
                else f"Umiejętność: {s['skill']} ({'★' * s['level']}{'☆' * (5 - s['level'])})"
            ),
            "skill_manage"
        )
        zarzadzaj_sekcja("langs", lambda l: f"Język: {l['lang']} ({l['level']})", "lang_manage")
        zarzadzaj_sekcja("cert", lambda c: f"Certyfikat: {c}", "cert_manage")


        if st.button("Wyczyść całe CV"):
            for s in sekcje:
                st.session_state[s] = []
            st.rerun()

with col2:
    st.header("Podgląd Live")

    bloki_kontaktowe = []
    if phone:
        bloki_kontaktowe.append(f"Tel: {phone}")
    if email:
        bloki_kontaktowe.append(f"Email: {email}")
    if location:
        bloki_kontaktowe.append(f"Lokalizacja: {location}")
    if linkedin:
        bloki_kontaktowe.append(f"LinkedIn: {linkedin}")
    if github_link:
        bloki_kontaktowe.append(f"GitHub: {github_link}")

    st.write("---")

    if uklad == "split":
        prev_col1, prev_col2 = st.columns([1, 2.5])

        with prev_col1:
            if uploaded_file:
                st.image(Image.open(uploaded_file), width=120)

            if name:
                st.markdown(f"<h3 style='color: {kolor_glowny}; margin-bottom: 0;'>{name}</h3>", unsafe_allow_html=True)
            if position:
                st.markdown(f"<p style='color: gray; margin-top: 4px;'>{position}</p>", unsafe_allow_html=True)

            if bloki_kontaktowe:
                st.write("---")
                st.markdown(f"<h4 style='color: {kolor_glowny};'>Kontakt</h4>", unsafe_allow_html=True)
                for kontakt in bloki_kontaktowe:
                    st.write(kontakt)

            if st.session_state.skills:
                st.write("---")
                st.markdown(f"<h4 style='color: {kolor_glowny};'>Umiejętności</h4>", unsafe_allow_html=True)
                for s in st.session_state.skills:
                    if s["level"] is None:
                        st.write(f"{s['skill']}")
                    else:
                        gwiazdki = "★" * s['level'] + "☆" * (5 - s['level'])
                        st.write(f"**{s['skill']}** \n{gwiazdki}")

            if st.session_state.langs:
                st.write("---")
                st.markdown(f"<h4 style='color: {kolor_glowny};'>Języki</h4>", unsafe_allow_html=True)
                for lang in st.session_state.langs:
                    st.write(f"{lang['lang']} ({lang['level']})")

            if st.session_state.cert:
                st.write("---")
                st.markdown(f"<h4 style='color: {kolor_glowny};'>Certyfikaty</h4>", unsafe_allow_html=True)
                for cert in st.session_state.cert:
                    st.write(f"- {cert}")

        with prev_col2:
            if description:
                st.write(description)

            if st.session_state.exp:
                st.write("---")
                st.markdown(f"<h3 style='color: {kolor_glowny};'>Doświadczenie zawodowe</h3>", unsafe_allow_html=True)
                for job in st.session_state.exp:
                    naglowek_live = f"**{job['role']}** w *{job['company']}*"
                    if job["years"]:
                        naglowek_live += f" ({job['years']})"
                    st.markdown(naglowek_live)
                    if job["duty"]:
                        st.write(job["duty"])

            if st.session_state.edu:
                st.write("---")
                st.markdown(f"<h3 style='color: {kolor_glowny};'>Edukacja</h3>", unsafe_allow_html=True)
                for edu in st.session_state.edu:
                    szkola_live = f"**{edu['school']}**"
                    if edu["years_edu"]:
                        szkola_live += f" ({edu['years_edu']})"
                    st.markdown(szkola_live)
                    if edu["field"]:
                        st.write(f"Kierunek: {edu['field']}")

    else:
        if uploaded_file:
            col_text, col_img = st.columns([3, 1])
            with col_text:
                if name:
                    st.markdown(f"<h1 style='color: {kolor_glowny};'>{name}</h1>", unsafe_allow_html=True)
                if position:
                    st.markdown(f"### *{position}*")
            with col_img:
                st.image(Image.open(uploaded_file), width=120)
        else:
            if name:
                st.markdown(f"<h1 style='color: {kolor_glowny};'>{name}</h1>", unsafe_allow_html=True)
            if position:
                st.markdown(f"### *{position}*")

        if bloki_kontaktowe:
            st.markdown(
                f"<p style='color: gray; font-size: 14px;'>{' | '.join(bloki_kontaktowe)}</p>",
                unsafe_allow_html=True,
            )

        st.write("---")
        if description:
            st.write(description)

        if st.session_state.exp:
            st.markdown(f"<h3 style='color: {kolor_glowny};'>Doświadczenie zawodowe</h3>", unsafe_allow_html=True)
            for job in st.session_state.exp:
                naglowek_live = f"**{job['role']}** w *{job['company']}*"
                if job["years"]:
                    naglowek_live += f" ({job['years']})"
                st.markdown(naglowek_live)
                if job["duty"]:
                    st.write(job["duty"])
                st.write("---")

        if st.session_state.edu:
            st.markdown(f"<h3 style='color: {kolor_glowny};'>Edukacja</h3>", unsafe_allow_html=True)
            for edu in st.session_state.edu:
                szkola_live = f"**{edu['school']}**"
                if edu["years_edu"]:
                    szkola_live += f" ({edu['years_edu']})"
                st.markdown(szkola_live)
                if edu["field"]:
                    st.write(f"Kierunek: {edu['field']}")
                st.write("---")

        if st.session_state.skills:
            st.markdown(f"<h3 style='color: {kolor_glowny};'>Umiejętności</h3>", unsafe_allow_html=True)
            bloki_skilli = [
                (
                    f"**{s['skill']}**"
                    if s["level"] is None
                    else f"**{s['skill']}** ({'★' * s['level']}{'☆' * (5 - s['level'])})"
                )
    for s in st.session_state.skills
]
            st.write(", ".join(bloki_skilli))
            st.write("---")

        if st.session_state.langs:
            st.markdown(f"<h3 style='color: {kolor_glowny};'>Języki obce</h3>", unsafe_allow_html=True)
            for lang in st.session_state.langs:
                st.write(f"{lang['lang']} - {lang['level']}")

        if st.session_state.cert:
            st.markdown(f"<h3 style='color: {kolor_glowny};'>Certyfikaty i Kursy</h3>", unsafe_allow_html=True)
            st.write(", ".join(st.session_state.cert))
            st.write("---")

    if dodaj_rodo:
        st.write(" ")
        st.markdown(
            f"<p style='color: gray; font-size: 11px; text-align: center; font-style: italic;'>{RODO_TEKST}</p>",
            unsafe_allow_html=True,
        )

    if name:
        st.write("---")
        photo_bytes = uploaded_file.getvalue() if uploaded_file else None
        c_pdf, c_docx, _ = st.columns([1, 1, 4])

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
                rodo=dodaj_rodo,
                photo_bytes=photo_bytes,
            )
            st.download_button(
                label="Pobierz jako PDF",
                data=pdf_data,
                file_name="CV.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with c_docx:
            docx_data = generuj_docx(
                name=name,
                position=position,
                description=description,
                exp_list=st.session_state.exp,
                edu_list=st.session_state.edu,
                skills_list=st.session_state.skills,
                langs_list=st.session_state.langs,
                cert_list=st.session_state.cert,
                phone=phone,
                email=email,
                location=location,
                linkedin=linkedin,
                github=github_link,
                rodo=dodaj_rodo,
                photo_bytes=photo_bytes
            )
            st.download_button(
                label="Pobierz jako Word",
                data=docx_data,
                file_name="CV.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )