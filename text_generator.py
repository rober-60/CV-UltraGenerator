def generuj_txt(name, position, description, exp_list, edu_list, skills_list, langs_list, cert_list=None, phone=None, email=None, location=None, linkedin=None, github=None, rodo=True):
    linie = []

    if name:
        linie.append(name.upper())
    if position:
        linie.append(position)

    bloki_kontaktowe = []
    if phone: bloki_kontaktowe.append(f"Tel: {phone}")
    if email: bloki_kontaktowe.append(f"Email: {email}")
    if location: bloki_kontaktowe.append(f"Lokalizacja: {location}")
    if linkedin: bloki_kontaktowe.append(f"LinkedIn: {linkedin}")
    if github: bloki_kontaktowe.append(f"GitHub: {github}")
    if bloki_kontaktowe:
        linie.append(" | ".join(bloki_kontaktowe))

    if description:
        linie.append("")
        linie.append(description)

    if exp_list:
        linie.append("")
        linie.append("DOŚWIADCZENIE ZAWODOWE")
        linie.append("-" * 30)
        for job in exp_list:
            naglowek = f"{job['role']} w {job['company']}"
            if job['years']:
                naglowek += f" ({job['years']})"
            linie.append(naglowek)
            if job['duty']:
                linie.append(job['duty'])
            linie.append("")

    if edu_list:
        linie.append("EDUKACJA")
        linie.append("-" * 30)
        for edu in edu_list:
            naglowek = edu['school']
            if edu['years_edu']:
                naglowek += f" ({edu['years_edu']})"
            linie.append(naglowek)
            if edu['field']:
                linie.append(f"Kierunek: {edu['field']}")
            linie.append("")

    if skills_list:
        linie.append("UMIEJĘTNOŚCI")
        linie.append("-" * 30)
        tekst_skilli = []
        for s in skills_list:
            if s["level"] is None:
                tekst_skilli.append(s["skill"])
            else:
                tekst_skilli.append(f"{s['skill']} ({s['level']}/5)")
        linie.append(", ".join(tekst_skilli))
        linie.append("")

    if langs_list:
        linie.append("JĘZYKI OBCE")
        linie.append("-" * 30)
        for lang in langs_list:
            linie.append(f"{lang['lang']} - {lang['level']}")
        linie.append("")

    if cert_list:
        linie.append("CERTYFIKATY I KURSY")
        linie.append("-" * 30)
        for cert in cert_list:
            linie.append(f"- {cert}")
        linie.append("")

    if rodo:
        linie.append("Wyrażam zgodę na przetwarzanie moich danych osobowych dla potrzeb niezbędnych do realizacji procesu rekrutacji (zgodnie z rozporządzeniem o ochronie danych osobowych RODO).")

    return "\n".join(linie)