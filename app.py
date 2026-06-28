import streamlit as st
from PIL import Image
from fpdf import FPDF
import io

# Ustawienia strony
st.set_page_config(layout="wide")

st.title("Generator CV")
st.subheader("Stwórz swoje portfolio w 5 minut")

# --- INICJALIZACJA PAMIĘCI ---
sekcje = ["exp", "edu", "skills", "langs"]
for sekcja in sekcje:
    if sekcja not in st.session_state:
        st.session_state[sekcja] = []

# --- FUNKCJE POMOCNICZE (SPRZĄTANIE KODU) ---

def formularz_sekcji(id_formularza, naglowek, pola, klucz_pamieci):
    """Generuje uniwersalny formularz na podstawie podanych pól."""
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
            # Sprawdzamy czy pierwszy element formularza nie jest pusty
            pierwszy_klucz = list(pola.keys())[0]
            if dane_wpisu[pierwszy_klucz]:
                # Jeśli to zwykły skill (pojedynczy string), zapisz go bezpośrednio, inaczej słownik
                wpis = dane_wpisu[pierwszy_klucz] if len(pola) == 1 else dane_wpisu
                st.session_state[klucz_pamieci].append(wpis)
                st.rerun()

def zarzadzaj_sekcja(naglowek, klucz_pamieci, funkcja_formatowania, klucz_id):
    """Wyświetla listę wpisów z danej sekcji i pozwala je usuwać."""
    if st.session_state[klucz_pamieci]:
        for index, element in enumerate(st.session_state[klucz_pamieci]):
            c1, c2 = st.columns([4, 1])
            c1.write(funkcja_formatowania(element))
            if c2.button("Usuń", key=f"del_{klucz_id}_{index}"):
                st.session_state[klucz_pamieci].pop(index)
                st.rerun()

# --- FUNKCJA GENERUJĄCA PDF ---
def generuj_pdf(name, position, description, exp_list, edu_list, skills_list, langs_list, kolor_rgb):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.add_font("Roboto", "", "Roboto-Regular.ttf")
    pdf.add_font("Roboto", "B", "Roboto-Bold.ttf")
    pdf.set_font("Roboto", size=12)
    
    if name:
        pdf.set_font("Roboto", style="B", size=24)
        pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
        pdf.cell(200, 10, txt=name, ln=True)
        
    if position:
        pdf.set_font("Roboto", style="", size=14)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(200, 10, txt=position, ln=True)
        
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)
    
    if description:
        pdf.set_font("Roboto", size=11)
        pdf.multi_cell(0, 6, txt=description)
        pdf.ln(5)
        
    if exp_list:
        pdf.ln(5)
        pdf.set_font("Roboto", style="B", size=16)
        pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
        pdf.cell(200, 10, txt="Doswiadczenie zawodowe", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        for job in exp_list:
            pdf.set_font("Roboto", style="B", size=12)
            naglowek_pracy = f"{job['role']} w {job['company']}"
            if job['years']: naglowek_pracy += f" ({job['years']})"
            pdf.cell(200, 8, txt=naglowek_pracy, ln=True)
            if job['duty']:
                pdf.set_font("Roboto", size=11)
                pdf.multi_cell(0, 6, txt=job['duty'])
            pdf.ln(4)

    if edu_list:
        pdf.ln(5)
        pdf.set_font("Roboto", style="B", size=16)
        pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
        pdf.cell(200, 10, txt="Edukacja", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        for edu in edu_list:
            pdf.set_font("Roboto", style="B", size=12)
            naglowek_szkoły = edu['school']
            if edu['years_edu']: naglowek_szkoły += f" ({edu['years_edu']})"
            pdf.cell(200, 8, txt=naglowek_szkoły, ln=True)
            if edu['field']:
                pdf.set_font("Roboto", size=11)
                pdf.cell(200, 6, txt=f"Kierunek: {edu['field']}", ln=True)
            pdf.ln(4)

    if skills_list:
        pdf.ln(5)
        pdf.set_font("Roboto", style="B", size=16)
        pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
        pdf.cell(200, 10, txt="Umiejetnosci", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.set_font("Roboto", size=11)
        pdf.multi_cell(0, 6, txt=", ".join(skills_list))

    if langs_list:
        pdf.ln(5)
        pdf.set_font("Roboto", style="B", size=16)
        pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
        pdf.cell(200, 10, txt="Jezyki obce", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.set_font("Roboto", size=11)
        for lang in langs_list:
            pdf.cell(200, 6, txt=f"{lang['lang']} - {lang['level']}", ln=True)
            
    return bytes(pdf.output())


# --- UKŁAD STRONY STREAMLIT ---
col1, col2 = st.columns(2)

with col1:
    st.header("Wpisz swoje dane")
    
    szablon = st.selectbox("Wybierz motyw kolorystyczny", ["Klasyczny Granat", "Nowoczesna Zieleń", "Elegancki Ciemny"])
    kolory = {
        "Klasyczny Granat": ("#1E3A8A", (30, 58, 138)),
        "Nowoczesna Zieleń": ("#065F46", (6, 95, 70)),
        "Elegancki Ciemny": ("#1F2937", (31, 41, 55))
    }
    kolor_glowny, kolor_rgb = kolory[szablon]

    st.write("---")
    name = st.text_input("Imię i Nazwisko", placeholder="Jan Kowalski")
    position = st.text_input("Stanowisko", placeholder="Python Developer")
    description = st.text_area("O sobie", placeholder="Powiedz coś o sobie :)")
    
    st.write("---")
    st.subheader("Zdjęcie profilowe")
    uploaded_file = st.file_uploader("Wybierz zdjęcie (JPG, PNG)", type=["jpg", "jpeg", "png"])

    # GENEROWANIE FORMULARZY PRZEZ FUNKCJĘ
    formularz_sekcji("praca_form", "Doświadczenie zawodowe", {"company": "Firma", "role": "Rola / stanowisko", "years": "Lata zatrudnienia", "duty": "Obowiązki"}, "exp")
    formularz_sekcji("edu_form", "Edukacja", {"school": "Szkoła / Uczelnia", "field": "Kierunek / Profil", "years_edu": "Lata nauki"}, "edu")
    formularz_sekcji("skill_form", "Umiejętności", {"skill": "Wpisz umiejętność (np. Python, Git)"}, "skills")
    formularz_sekcji("lang_form", "Języki obce", {"lang": "Język", "level": "Poziom"}, "langs")

    # ZARZĄDZANIE DANYMI PRZEZ FUNKCJĘ
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
        pdf_data = generuj_pdf(
            name, position, description, 
            st.session_state.exp, st.session_state.edu, 
            st.session_state.skills, st.session_state.langs, kolor_rgb
        )
        st.download_button(label="Pobierz swoje CV w formacie PDF", data=pdf_data, file_name="CV.pdf", mime="application/pdf")