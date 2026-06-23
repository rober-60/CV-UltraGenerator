import streamlit as st
from PIL import Image
from fpdf import FPDF
import io

# Ustawienia strony
st.set_page_config(layout="wide")

st.title("Generator CV")
st.subheader("Stwórz swoje portfolio w 5 minut")

if "exp" not in st.session_state:
    st.session_state.exp = []

def generuj_pdf(name, position, description, exp_list, kolor_rgb):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Rejestracja czcionki z polskimi znakami
    pdf.add_font("Roboto", "", "Roboto-Regular.ttf")
    pdf.add_font("Roboto", "B", "Roboto-Bold.ttf")
    
    pdf.set_font("Roboto", size=12)
    
    # Imię i Nazwisko
    if name:
        pdf.set_font("Roboto", style="B", size=24)
        pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
        pdf.cell(200, 10, txt=name, ln=True)
        
    # Stanowisko
    if position:
        pdf.set_font("Roboto", style="", size=14)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(200, 10, txt=position, ln=True)
        
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)
    
    # O sobie
    if description:
        pdf.set_font("Roboto", size=11)
        pdf.multi_cell(0, 6, txt=description)
        pdf.ln(5)
        
    # Doświadczenie zawodowe
    if exp_list:
        pdf.ln(5)
        pdf.set_font("Roboto", style="B", size=16)
        pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
        pdf.cell(200, 10, txt="Doświadczenie zawodowe", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        for job in exp_list:
            pdf.set_font("Roboto", style="B", size=12)
            naglowek_pracy = f"{job['role']} w {job['company']} ({job['years']})"
            pdf.cell(200, 8, txt=naglowek_pracy, ln=True)
            
            pdf.set_font("Roboto", size=11)
            pdf.multi_cell(0, 6, txt=job['duty'])
            pdf.ln(4)
            
    # Zamieniamy bytearray na czyste bytes, których wymaga Streamlit
    return bytes(pdf.output())

# Podział ekranu na dwie kolumny: Formularz i Podgląd
col1, col2 = st.columns(2)

with col1:
    st.header("Wpisz swoje dane")
    
    st.subheader("Wygląd CV")
    szablon = st.selectbox(
        "Wybierz motyw kolorystyczny",
        ["Klasyczny Granat", "Nowoczesna Zieleń", "Elegancki Ciemny"]
    )
    
    # Mapowanie kolorów (Hex dla Streamlita, RGB dla PDF)
    if szablon == "Klasyczny Granat":
        kolor_glowny = "#1E3A8A"
        kolor_rgb = (30, 58, 138)
    elif szablon == "Nowoczesna Zieleń":
        kolor_glowny = "#065F46"
        kolor_rgb = (6, 95, 70)
    else:
        kolor_glowny = "#1F2937"
        kolor_rgb = (31, 41, 55)

    st.write("---")
    name = st.text_input("Imię i Nazwisko", placeholder="Jan Kowalski")
    position = st.text_input("Stanowisko", placeholder="Python Developer")
    description = st.text_area("O sobie", placeholder="Powiedz coś o sobie :)")
    
    st.write("---")
    st.subheader("Zdjęcie profilowe")
    uploaded_file = st.file_uploader("Wybierz zdjęcie (JPG, PNG)", type=["jpg", "jpeg", "png"])

    st.write("---")
    st.subheader("Doświadczenie zawodowe")

    with st.form("praca_form", clear_on_submit=True):
        company = st.text_input("Firma", placeholder="Firma")
        role = st.text_input("Rola w firmie lub stanowisko", placeholder="Rola")
        years = st.text_input("Lata zatrudnienia", placeholder="2010-2015")
        duty = st.text_area("Obowiązki w firmie", placeholder="Opisz swoje obowiązki")

        button = st.form_submit_button("Dodaj miejsce pracy")

        if button and company and role:
            new_company = {
                "company": company,
                "role": role,
                "years": years,
                "duty": duty
            }
            st.session_state.exp.append(new_company)
            st.success(f"Dodano {company}")
            st.rerun()

    # Zarządzanie dodanymi miejscami pracy
    if st.session_state.exp:
        st.write("---")
        st.subheader("Zarządzaj dodanymi miejscami pracy:")
        
        for index, job in enumerate(st.session_state.exp):
            col_info, col_delete = st.columns([4, 1])
            with col_info:
                st.write(f"{job['role']} w {job['company']}")
            with col_delete:
                if st.button("Usuń", key=f"delete_{index}"):
                    st.session_state.exp.pop(index)
                    st.rerun()

        st.write("---")
        if st.button("Wyczyść całe CV i zacznij od nowa"):
            st.session_state.exp = []
            st.rerun()


with col2:
    st.header("Podgląd Live")
    
    if uploaded_file:
        col_text, col_img = st.columns([3, 1])
        with col_text:
            if name:
                st.markdown(f"<h1 style='color: {kolor_glowny};'>{name}</h1>", unsafe_allow_html=True)
            if position:
                st.markdown(f"### *{position}*")
        with col_img:
            image = Image.open(uploaded_file)
            st.image(image, width=120)
    else:
        if name:
            st.markdown(f"<h1 style='color: {kolor_glowny};'>{name}</h1>", unsafe_allow_html=True)
        if position:
            st.markdown(f"### *{position}*")
            
    st.write("---")
    if description:
        st.write(description)

    if st.session_state.exp:
        st.write("---")
        st.markdown(f"<h3 style='color: {kolor_glowny};'>Doświadczenie zawodowe</h3>", unsafe_allow_html=True)
        for job in st.session_state.exp:
            st.markdown(f"**{job['role']}** w *{job['company']}* ({job['years']})")
            st.write(job['duty'])
            st.write("---")
            
    # --- PRZYCISK POBIERANIA PDF ---
    if name:
        st.write("---")
        pdf_data = generuj_pdf(name, position, description, st.session_state.exp, kolor_rgb)
        st.download_button(
            label="Pobierz swoje CV w formacie PDF",
            data=pdf_data,
            file_name="CV.pdf",
            mime="application/pdf"
        )