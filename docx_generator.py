import io

from docx import Document
from docx.shared import Inches, Pt, RGBColor

from config import RODO_TEKST


def generuj_docx(
    name,
    position,
    description,
    exp_list,
    edu_list,
    skills_list,
    langs_list,
    cert_list=None,
    phone="",
    email="",
    location="",
    linkedin="",
    github="",
    rodo=True,
    photo_bytes=None,
):
    doc = Document()

    if photo_bytes:
        doc.add_picture(io.BytesIO(photo_bytes), width=Inches(1.2))

    if name:
        doc.add_heading(name, level=0)
    if position:
        p = doc.add_paragraph()
        p.add_run(position).italic = True

    kontakt = []
    if phone:
        kontakt.append(f"Tel: {phone}")
    if email:
        kontakt.append(f"Email: {email}")
    if location:
        kontakt.append(f"Lokalizacja: {location}")
    if linkedin:
        kontakt.append(f"LinkedIn: {linkedin}")
    if github:
        kontakt.append(f"GitHub: {github}")
    if kontakt:
        doc.add_paragraph(" | ".join(kontakt))

    if description:
        doc.add_paragraph(description)

    if exp_list:
        doc.add_heading("Doświadczenie zawodowe", level=1)
        for job in exp_list:
            naglowek_pracy = f"{job['role']} w {job['company']}"
            if job["years"]:
                naglowek_pracy += f" ({job['years']})"
            doc.add_heading(naglowek_pracy, level=2)
            if job["duty"]:
                doc.add_paragraph(job["duty"])

    if edu_list:
        doc.add_heading("Edukacja", level=1)
        for edu in edu_list:
            naglowek_szkoly = edu["school"]
            if edu["years_edu"]:
                naglowek_szkoly += f" ({edu['years_edu']})"
            doc.add_heading(naglowek_szkoly, level=2)
            if edu["field"]:
                doc.add_paragraph(f"Kierunek: {edu['field']}")

    if skills_list:
        doc.add_heading("Umiejętności", level=1)
        doc.add_paragraph(", ".join(skills_list))

    if langs_list:
        doc.add_heading("Języki obce", level=1)
        for lang in langs_list:
            doc.add_paragraph(f"{lang['lang']} - {lang['level']}")

    if cert_list:
        doc.add_heading("Certyfikaty i Kursy", level=1)
        for cert in cert_list:
            doc.add_paragraph(f"- {cert}")

    if rodo:
        doc.add_paragraph()
        p_rodo = doc.add_paragraph()
        p_rodo.alignment = 1
        run_rodo = p_rodo.add_run(RODO_TEKST)
        run_rodo.font.size = Pt(8)
        run_rodo.font.color.rgb = RGBColor(120, 120, 120)

    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()
