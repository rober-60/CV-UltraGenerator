from docx import Document
import io

def generuj_docx(name, position, description, exp_list, edu_list, skills_list, langs_list, rodo=True):
    doc = Document()
    
    if name:
        doc.add_heading(name, level=0)
    if position:
        p = doc.add_paragraph()
        p.add_run(position).italic = True
        
    if description:
        doc.add_paragraph(description)
        
    if exp_list:
        doc.add_heading("Doświadczenie zawodowe", level=1)
        for job in exp_list:
            naglowek_pracy = f"{job['role']} w {job['company']}"
            if job['years']: naglowek_pracy += f" ({job['years']})"
            doc.add_heading(naglowek_pracy, level=2)
            if job['duty']:
                doc.add_paragraph(job['duty'])

    if edu_list:
        doc.add_heading("Edukacja", level=1)
        for edu in edu_list:
            naglowek_szkoły = edu['school']
            if edu['years_edu']: naglowek_szkoły += f" ({edu['years_edu']})"
            doc.add_heading(naglowek_szkoły, level=2)
            if edu['field']:
                doc.add_paragraph(f"Kierunek: {edu['field']}")

    if skills_list:
        doc.add_heading("Umiejętności", level=1)
        doc.add_paragraph(", ".join(skills_list))

    if langs_list:
        doc.add_heading("Języki obce", level=1)
        for lang in langs_list:
            doc.add_paragraph(f"{lang['lang']} - {lang['level']}")
        
    if rodo:
        doc.add_paragraph() # Pusta linia odstępu
        p_rodo = doc.add_paragraph()
        p_rodo.alignment = 1 # Wyśrodkowanie tekstu w python-docx
        run_rodo = p_rodo.add_run("Wyrażam zgodę na przetwarzanie moich danych osobowych dla potrzeb niezbędnych do realizacji procesu rekrutacji (zgodnie z rozporządzeniem o ochronie danych osobowych RODO).")
        run_rodo.font.size = 101600 # Odpowiednik małej czcionki (8-9 pkt)
        run_rodo.font.color.rgb = (120, 120, 120)

    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()