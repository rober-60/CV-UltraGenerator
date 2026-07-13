import io
import os
import tempfile

import fitz
from fpdf import FPDF
from PIL import Image

from config import RODO_ODSTEP_DOL_MM, RODO_REZERWA_EXTRA_MM, RODO_TEKST


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


def _wysokosc_rodo(pdf):
    pdf.set_font("Roboto", size=7)
    szerokosc = pdf.w - pdf.l_margin - pdf.r_margin
    linie = pdf.multi_cell(
        szerokosc, 3.5, RODO_TEKST, align="C", dry_run=True, output="LINES"
    )
    return len(linie) * 3.5


def _limit_tresci(pdf, zarezerwowany_dol):
    return pdf.h - zarezerwowany_dol


def _miejsce_na_tresc(pdf, zarezerwowany_dol, potrzebne=0):
    return pdf.get_y() + potrzebne <= _limit_tresci(pdf, zarezerwowany_dol)


def _bezpieczny_multi_cell(pdf, w, h, txt, zarezerwowany_dol, **kwargs):
    if not _miejsce_na_tresc(pdf, zarezerwowany_dol, h):
        return False
    linie = pdf.multi_cell(w, h, txt, dry_run=True, output="LINES", **kwargs)
    if not _miejsce_na_tresc(pdf, zarezerwowany_dol, len(linie) * h):
        return False
    pdf.multi_cell(w, h, txt, **kwargs)
    return True


def _dodaj_rodo(pdf, wysokosc_rodo):
    pdf.page = 1
    pdf.set_auto_page_break(auto=False)
    szerokosc = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_xy(pdf.l_margin, pdf.h - wysokosc_rodo - RODO_ODSTEP_DOL_MM)
    pdf.set_font("Roboto", size=7)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(szerokosc, 3.5, RODO_TEKST, align="C")


def _tylko_pierwsza_strona(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    if len(doc) <= 1:
        doc.close()
        return pdf_bytes
    doc.select([0])
    wynik = doc.tobytes()
    doc.close()
    return wynik


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
    pdf.set_auto_page_break(auto=False)

    pdf.add_font("Roboto", "", "Roboto-Regular.ttf")
    pdf.add_font("Roboto", "B", "Roboto-Bold.ttf")
    pdf.set_font("Roboto", size=12)

    wysokosc_rodo = _wysokosc_rodo(pdf) if rodo else 0
    zarezerwowany_dol = wysokosc_rodo + RODO_REZERWA_EXTRA_MM if rodo else 10

    if uklad == "split":
        pdf.set_fill_color(243, 244, 246)
        pdf.rect(0, 0, 65, pdf.h, "F")

        y_left = 15
        if photo_bytes:
            _embed_photo(pdf, photo_bytes, x=12, y=y_left, w=45)
            y_left += 50

        pdf.set_xy(10, y_left)

        if name and _miejsce_na_tresc(pdf, zarezerwowany_dol, 8):
            pdf.set_font("Roboto", style="B", size=18)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            _bezpieczny_multi_cell(pdf, 50, 8, name, zarezerwowany_dol)
            pdf.ln(2)

        if position and _miejsce_na_tresc(pdf, zarezerwowany_dol, 6):
            pdf.set_font("Roboto", style="", size=11)
            pdf.set_text_color(100, 100, 100)
            _bezpieczny_multi_cell(pdf, 50, 6, position, zarezerwowany_dol)
            pdf.ln(8)

        pdf.set_text_color(0, 0, 0)

        if (phone or email or location or linkedin or github) and _miejsce_na_tresc(
            pdf, zarezerwowany_dol, 6
        ):
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(50, 6, txt="KONTAKT", ln=True)
            pdf.set_font("Roboto", size=9)
            if phone and _miejsce_na_tresc(pdf, zarezerwowany_dol, 5):
                pdf.cell(50, 5, txt=f"Tel: {phone}", ln=True)
            if email and _miejsce_na_tresc(pdf, zarezerwowany_dol, 5):
                pdf.cell(50, 5, txt=f"Email: {email}", ln=True)
            if location and _miejsce_na_tresc(pdf, zarezerwowany_dol, 5):
                pdf.cell(50, 5, txt=f"Miejscowość: {location}", ln=True)
            if linkedin and _miejsce_na_tresc(pdf, zarezerwowany_dol, 5):
                pdf.cell(50, 5, txt=f"LinkedIn: {linkedin}", ln=True)
            if github and _miejsce_na_tresc(pdf, zarezerwowany_dol, 5):
                pdf.cell(50, 5, txt=f"GitHub: {github}", ln=True)
            pdf.ln(8)

        if skills_list:
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(50, 6, txt="UMIEJĘTNOŚCI", ln=True)
            for s in skills_list:
                pdf.set_font("Roboto", style="B", size=10)
                pdf.cell(50, 4, txt=s['skill'], ln=True)
                pdf.set_font("Roboto", size=9)
                pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2]) # gwiazdki w kolorze motywu!
                if s["level"] is None:
                    pass
                else:
                    kropki = "● " * s["level"] + "○ " * (5 - s["level"])
                    pdf.cell(50, 4, txt=kropki.strip(), ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(1)
            pdf.ln(5)

        if langs_list and _miejsce_na_tresc(pdf, zarezerwowany_dol, 6):
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(50, 6, txt="JĘZYKI", ln=True)
            pdf.set_font("Roboto", size=10)
            for lang in langs_list:
                if not _miejsce_na_tresc(pdf, zarezerwowany_dol, 5):
                    break
                pdf.cell(50, 5, txt=f"{lang['lang']} ({lang['level']})", ln=True)
            pdf.ln(8)

        if cert_list and _miejsce_na_tresc(pdf, zarezerwowany_dol, 6):
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(50, 6, txt="CERTYFIKATY", ln=True)
            pdf.set_font("Roboto", size=9)
            for cert in cert_list:
                if not _bezpieczny_multi_cell(pdf, 50, 5, f"- {cert}", zarezerwowany_dol):
                    break

        pdf.set_xy(72, 15)
        if description:
            _bezpieczny_multi_cell(pdf, 125, 6, description, zarezerwowany_dol)
            pdf.ln(5)

        if exp_list and _miejsce_na_tresc(pdf, zarezerwowany_dol, 14):
            pdf.ln(3)
            pdf.set_xy(72, pdf.get_y())
            pdf.set_font("Roboto", style="B", size=14)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(125, 8, txt="Doświadczenie zawodowe", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(72, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)

            for job in exp_list:
                if not _miejsce_na_tresc(pdf, zarezerwowany_dol, 6):
                    break
                pdf.set_xy(72, pdf.get_y())
                pdf.set_font("Roboto", style="B", size=11)
                naglowek_pracy = f"{job['role']} w {job['company']}"
                if job["years"]:
                    naglowek_pracy += f" ({job['years']})"
                pdf.cell(125, 6, txt=naglowek_pracy, ln=True)
                if job["duty"]:
                    pdf.set_xy(72, pdf.get_y())
                    pdf.set_font("Roboto", size=10)
                    _bezpieczny_multi_cell(pdf, 125, 5, job["duty"], zarezerwowany_dol)
                pdf.ln(2)

        if edu_list and _miejsce_na_tresc(pdf, zarezerwowany_dol, 14):
            pdf.ln(3)
            pdf.set_xy(72, pdf.get_y())
            pdf.set_font("Roboto", style="B", size=14)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(125, 8, txt="Edukacja", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(72, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)

            for edu in edu_list:
                if not _miejsce_na_tresc(pdf, zarezerwowany_dol, 6):
                    break
                pdf.set_xy(72, pdf.get_y())
                pdf.set_font("Roboto", style="B", size=11)
                naglowek_szkoly = edu["school"]
                if edu["years_edu"]:
                    naglowek_szkoly += f" ({edu['years_edu']})"
                pdf.cell(125, 6, txt=naglowek_szkoly, ln=True)
                if edu["field"] and _miejsce_na_tresc(pdf, zarezerwowany_dol, 5):
                    pdf.set_xy(72, pdf.get_y())
                    pdf.set_font("Roboto", size=10)
                    pdf.cell(125, 5, txt=f"Kierunek: {edu['field']}", ln=True)
                pdf.ln(2)

    else:
        if photo_bytes:
            _embed_photo(pdf, photo_bytes, x=165, y=10, w=35)

        if name and _miejsce_na_tresc(pdf, zarezerwowany_dol, 10):
            pdf.set_font("Roboto", style="B", size=24)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(150 if photo_bytes else 200, 10, txt=name, ln=True)
        if position and _miejsce_na_tresc(pdf, zarezerwowany_dol, 10):
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

        if bloki_kontaktowe and _miejsce_na_tresc(pdf, zarezerwowany_dol, 5):
            pdf.cell(200, 5, txt=" | ".join(bloki_kontaktowe), ln=True)

        pdf.ln(5)
        pdf.set_text_color(0, 0, 0)

        if description:
            _bezpieczny_multi_cell(pdf, 0, 6, description, zarezerwowany_dol)
            pdf.ln(5)

        if exp_list and _miejsce_na_tresc(pdf, zarezerwowany_dol, 16):
            pdf.ln(3)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Doświadczenie zawodowe", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            for job in exp_list:
                if not _miejsce_na_tresc(pdf, zarezerwowany_dol, 8):
                    break
                pdf.set_font("Roboto", style="B", size=12)
                naglowek_pracy = f"{job['role']} w {job['company']}"
                if job["years"]:
                    naglowek_pracy += f" ({job['years']})"
                pdf.cell(200, 8, txt=naglowek_pracy, ln=True)
                if job["duty"]:
                    pdf.set_font("Roboto", size=11)
                    _bezpieczny_multi_cell(pdf, 0, 6, job["duty"], zarezerwowany_dol)
                pdf.ln(2)

        if edu_list and _miejsce_na_tresc(pdf, zarezerwowany_dol, 16):
            pdf.ln(3)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Edukacja", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            for edu in edu_list:
                if not _miejsce_na_tresc(pdf, zarezerwowany_dol, 8):
                    break
                pdf.set_font("Roboto", style="B", size=12)
                naglowek_szkoly = edu["school"]
                if edu["years_edu"]:
                    naglowek_szkoly += f" ({edu['years_edu']})"
                pdf.cell(200, 8, txt=naglowek_szkoly, ln=True)
                if edu["field"] and _miejsce_na_tresc(pdf, zarezerwowany_dol, 6):
                    pdf.set_font("Roboto", size=11)
                    pdf.cell(200, 6, txt=f"Kierunek: {edu['field']}", ln=True)
                pdf.ln(2)

            if skills_list:
                pdf.ln(5)
                pdf.set_font("Roboto", style="B", size=16)
                pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
                pdf.cell(200, 10, txt="Umiejętności", ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(5)
                
                pdf.set_font("Roboto", size=11)
                tekst_skilli = []
                for s in skills_list:
                    if s["level"] is None:
                        tekst_skilli.append(s["skill"])
                    else:
                        kropki = "●" * s["level"] + "○" * (5 - s["level"])
                        tekst_skilli.append(f"{s['skill']} ({kropki})")
                    
                pdf.multi_cell(0, 6, txt=", ".join(tekst_skilli))

        if langs_list and _miejsce_na_tresc(pdf, zarezerwowany_dol, 16):
            pdf.ln(3)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Języki obce", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            pdf.set_font("Roboto", size=11)
            for lang in langs_list:
                if not _miejsce_na_tresc(pdf, zarezerwowany_dol, 6):
                    break
                pdf.cell(200, 6, txt=f"{lang['lang']} - {lang['level']}", ln=True)

        if cert_list and _miejsce_na_tresc(pdf, zarezerwowany_dol, 16):
            pdf.ln(3)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Certyfikaty i Kursy", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            pdf.set_font("Roboto", size=11)
            for cert in cert_list:
                if not _miejsce_na_tresc(pdf, zarezerwowany_dol, 6):
                    break
                pdf.cell(200, 6, txt=f"- {cert}", ln=True)

    if rodo:
        _dodaj_rodo(pdf, wysokosc_rodo)

    return _tylko_pierwsza_strona(bytes(pdf.output()))
