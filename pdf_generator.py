from fpdf import FPDF

def generuj_pdf(name, position, description, exp_list, edu_list, skills_list, langs_list, kolor_rgb, uklad="single"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.add_font("Roboto", "", "Roboto-Regular.ttf")
    pdf.add_font("Roboto", "B", "Roboto-Bold.ttf")
    pdf.set_font("Roboto", size=12)
    
    # --- UKŁAD DWUKOLUMNOWY (SPLIT) ---
    if uklad == "split":
        pdf.set_fill_color(243, 244, 246) 
        pdf.rect(0, 0, 65, 297, "F")
        pdf.set_xy(10, 15)
        
        if name:
            pdf.set_font("Roboto", style="B", size=18)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.multi_cell(50, 8, txt=name)
            pdf.ln(2)
            
        if position:
            pdf.set_font("Roboto", style="", size=11)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(50, 6, txt=position)
            pdf.ln(10)
            
        pdf.set_text_color(0, 0, 0)
        
        if skills_list:
            pdf.set_font("Roboto", style="B", size=13)
            pdf.cell(50, 8, txt="UMIEJĘTNOŚCI", ln=True)
            pdf.set_font("Roboto", size=10)
            for skill in skills_list:
                pdf.cell(50, 5, txt=f"- {skill}", ln=True)
            pdf.ln(8)
            
        if langs_list:
            pdf.set_font("Roboto", style="B", size=13)
            pdf.cell(50, 8, txt="JĘZYKI", ln=True)
            pdf.set_font("Roboto", size=10)
            for lang in langs_list:
                pdf.cell(50, 5, txt=f"{lang['lang']} ({lang['level']})", ln=True)
                
        pdf.set_xy(72, 15)
        if description:
            pdf.set_font("Roboto", size=11)
            pdf.multi_cell(125, 6, txt=description)
            pdf.ln(5)
            
        if exp_list:
            pdf.ln(5)
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
                if job['years']: naglowek_pracy += f" ({job['years']})"
                pdf.cell(125, 6, txt=naglowek_pracy, ln=True)
                if job['duty']:
                    pdf.set_xy(72, pdf.get_y())
                    pdf.set_font("Roboto", size=10)
                    pdf.multi_cell(125, 5, txt=job['duty'])
                pdf.ln(3)

        if edu_list:
            pdf.ln(5)
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
                naglowek_szkoły = edu['school']
                if edu['years_edu']: naglowek_szkoły += f" ({edu['years_edu']})"
                pdf.cell(125, 6, txt=naglowek_szkoły, ln=True)
                if edu['field']:
                    pdf.set_xy(72, pdf.get_y())
                    pdf.set_font("Roboto", size=10)
                    pdf.cell(125, 5, txt=f"Kierunek: {edu['field']}", ln=True)
                pdf.ln(3)

    # --- UKŁAD JEDNOKOLUMNOWY ---
    else:
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
            pdf.cell(200, 10, txt="Doświadczenie zawodowe", ln=True)
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
            pdf.cell(200, 10, txt="Umiejętności", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            pdf.set_font("Roboto", size=11)
            pdf.multi_cell(0, 6, txt=", ".join(skills_list))

        if langs_list:
            pdf.ln(5)
            pdf.set_font("Roboto", style="B", size=16)
            pdf.set_text_color(kolor_rgb[0], kolor_rgb[1], kolor_rgb[2])
            pdf.cell(200, 10, txt="Języki obce", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            pdf.set_font("Roboto", size=11)
            for lang in langs_list:
                pdf.cell(200, 6, txt=f"{lang['lang']} - {lang['level']}", ln=True)
            
    return bytes(pdf.output())