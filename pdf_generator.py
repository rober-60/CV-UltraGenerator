import io
import os
import tempfile

from fpdf import FPDF
from PIL import Image

from config import RODO_MARGIN_MM, RODO_TEKST


def _temp_image_path(photo_bytes):
    img = Image.open(io.BytesIO(photo_bytes))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    img.save(tmp.name, format="JPEG", quality=90)
    tmp.close()
    return tmp.name


def _embed_photo(pdf, photo_bytes, x, y, w):
    path = _temp_image_path(photo_bytes)
    try:
        pdf.image(path, x=x, y=y, w=w)
    finally:
        os.unlink(path)


def _dodaj_rodo(pdf, uklad):
    pdf.page = 1
    pdf.set_auto_page_break(auto=False)
    pdf.set_y(-RODO_MARGIN_MM)
    pdf.set_font("Roboto", size=7)
    pdf.set_text_color(120, 120, 120)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 3.5, txt=RODO_TEKST, align="C")


def generuj_pdf(
    name,
    position,
    description,
    phone,
    email,
    location,
    linkedin,
    github,
    exp_list,
    edu_list,
    skills_list,
    langs_list,
    cert_list,
    kolor_rgb,
    uklad="single",
    rodo=True,
    photo_bytes=None,
):
    pdf = FPDF()
    pdf.add_page()
    dolny_margines = RODO_MARGIN_MM + 2 if rodo else 15
    pdf.set_auto_page_break(auto=True, margin=dolny_margines)

    pdf.add_font("Roboto", "", "Roboto-Regular.ttf")
    pdf.add_font("Roboto", "B", "Roboto-Bold.ttf")
    pdf.set_font("Roboto", size=12)

    if uklad == "split":
        pdf.set_fill_color(243, 244, 246)
        pdf.rect(0, 0, 65, 297, "F")

        y_left = 15
        if photo_bytes:
            _embed_photo(pdf, photo_bytes, x=12, y=y_left, w=45)
            y_left += 50

        pdf.set_xy(10, y_left)

        if name:
            pdf.set_font("Roboto", style="B", size=18)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.multi_cell(50, 8, txt=name)
            pdf.ln(2)

        if position:
            pdf.set_font("Roboto", style="", size=11)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(50, 6, txt=position)
            pdf.ln(8)

        pdf.set_text_color(0, 0, 0)

        if phone or email or location or linkedin or github:
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(50, 6, txt="KONTAKT", ln=True)
            pdf.set_font("Roboto", size=9)
            if phone:
                pdf.cell(50, 5, txt=f"Tel: {phone}", ln=True)
            if email:
                pdf.cell(50, 5, txt=f"Email: {email}", ln=True)
            if location:
                pdf.cell(50, 5, txt=f"Miejscowość: {location}", ln=True)
            if linkedin:
                pdf.cell(50, 5, txt=f"LinkedIn: {linkedin}", ln=True)
            if github:
                pdf.cell(50, 5, txt=f"GitHub: {github}", ln=True)
            pdf.ln(8)

        if skills_list:
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(50, 6, txt="UMIEJĘTNOŚCI", ln=True)
            pdf.set_font("Roboto", size=10)
            for skill in skills_list:
                pdf.cell(50, 5, txt=f"- {skill}", ln=True)
            pdf.ln(8)

        if langs_list:
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(50, 6, txt="JĘZYKI", ln=True)
            pdf.set_font("Roboto", size=10)
            for lang in langs_list:
                pdf.cell(50, 5, txt=f"{lang['lang']} ({lang['level']})", ln=True)
            pdf.ln(8)

        if cert_list:
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(50, 6, txt="CERTYFIKATY", ln=True)
            pdf.set_font("Roboto", size=9)
            for cert in cert_list:
                pdf.multi_cell(50, 5, txt=f"- {cert}")

        pdf.set_xy(72, 15)
        if description:
            pdf.set_font("Roboto", size=11)
            pdf.multi_cell(125, 6, txt=description)
            pdf.ln(5)

        if exp_list:
            pdf.ln(3)
            pdf.set_xy(72, pdf.get_y())
            pdf.set_font("Roboto", style="B", size=14)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(125, 8, txt="Doświadczenie zawodowe", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(72, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)

            for job in exp_list:
                pdf.set_xy(72, pdf.get_y())
                pdf.set_font("Roboto", style="B", size=11)
                naglowek_pracy = f"{job['role']} w {job['company']}"
                if job["years"]:
                    naglowek_pracy += f" ({job['years']})"
                pdf.cell(125, 6, txt=naglowek_pracy, ln=True)
                if job["duty"]:
                    pdf.set_xy(72, pdf.get_y())
                    pdf.set_font("Roboto", size=10)
                    pdf.multi_cell(125, 5, txt=job["duty"])
                pdf.ln(2)

        if edu_list:
            pdf.ln(3)
            pdf.set_xy(72, pdf.get_y())
            pdf.set_font("Roboto", style="B", size=14)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(125, 8, txt="Edukacja", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(72, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)

            for edu in edu_list:
                pdf.set_xy(72, pdf.get_y())
                pdf.set_font("Roboto", style="B", size=11)
                naglowek_szkoly = edu["school"]
                if edu["years_edu"]:
                    naglowek_szkoly += f" ({edu['years_edu']})"
                pdf.cell(125, 6, txt=naglowek_szkoly, ln=True)
                if edu["field"]:
                    pdf.set_xy(72, pdf.get_y())
                    pdf.set_font("Roboto", size=10)
                    pdf.cell(125, 5, txt=f"Kierunek: {edu['field']}", ln=True)
                pdf.ln(2)

    else:
        if photo_bytes:
            _embed_photo(pdf, photo_bytes, x=165, y=10, w=35)

        if name:
            pdf.set_font("Roboto", style="B", size=24)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(150 if photo_bytes else 200, 10, txt=name, ln=True)
        if position:
            pdf.set_font("Roboto", style="", size=14)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(150 if photo_bytes else 200, 10, txt=position, ln=True)

        pdf.ln(2)
        pdf.set_font("Roboto", size=10)
        pdf.set_text_color(50, 50, 50)
        bloki_kontaktowe = []
        if phone:
            bloki_kontaktowe.append(f"Tel: {phone}")
        if email:
            bloki_kontaktowe.append(f"Email: {email}")
        if location:
            bloki_kontaktowe.append(f"Miejscowosc: {location}")
        if linkedin:
            bloki_kontaktowe.append(f"LinkedIn: {linkedin}")
        if github:
            bloki_kontaktowe.append(f"GitHub: {github}")

        if bloki_kontaktowe:
            pdf.cell(200, 5, txt=" | ".join(bloki_kontaktowe), ln=True)

        pdf.ln(5)
        pdf.set_text_color(0, 0, 0)

        if description:
            pdf.set_font("Roboto", size=11)
            pdf.multi_cell(0, 6, txt=description)
            pdf.ln(5)

        if exp_list:
            pdf.ln(3)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Doświadczenie zawodowe", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            for job in exp_list:
                pdf.set_font("Roboto", style="B", size=12)
                naglowek_pracy = f"{job['role']} w {job['company']}"
                if job["years"]:
                    naglowek_pracy += f" ({job['years']})"
                pdf.cell(200, 8, txt=naglowek_pracy, ln=True)
                if job["duty"]:
                    pdf.set_font("Roboto", size=11)
                    pdf.multi_cell(0, 6, txt=job["duty"])
                pdf.ln(2)

        if edu_list:
            pdf.ln(3)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Edukacja", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            for edu in edu_list:
                pdf.set_font("Roboto", style="B", size=12)
                naglowek_szkoly = edu["school"]
                if edu["years_edu"]:
                    naglowek_szkoly += f" ({edu['years_edu']})"
                pdf.cell(200, 8, txt=naglowek_szkoly, ln=True)
                if edu["field"]:
                    pdf.set_font("Roboto", size=11)
                    pdf.cell(200, 6, txt=f"Kierunek: {edu['field']}", ln=True)
                pdf.ln(2)

        if skills_list:
            pdf.ln(3)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Umiejętności", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            pdf.set_font("Roboto", size=11)
            pdf.multi_cell(0, 6, txt=", ".join(skills_list))

        if langs_list:
            pdf.ln(3)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Języki obce", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            pdf.set_font("Roboto", size=11)
            for lang in langs_list:
                pdf.cell(200, 6, txt=f"{lang['lang']} - {lang['level']}", ln=True)

        if cert_list:
            pdf.ln(3)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Certyfikaty i Kursy", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            pdf.set_font("Roboto", size=11)
            for cert in cert_list:
                pdf.cell(200, 6, txt=f"- {cert}", ln=True)

    if rodo:
        _dodaj_rodo(pdf, uklad)

    return bytes(pdf.output())
