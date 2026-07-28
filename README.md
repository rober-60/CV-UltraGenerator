# CV Creator

Aplikacja webowa do tworzenia CV w kilka minut — wypełniasz formularz, na bieżąco widzisz podgląd, a na końcu eksportujesz gotowy dokument do PDF, Word lub do formatu .txt.

## Funkcje

- Formularz danych osobowych, kontaktowych i opisu "O sobie"
- Sekcje: doświadczenie zawodowe, edukacja, umiejętności (z opcjonalną skalą zaawansowania), języki obce, certyfikaty i kursy
- Obsługa zakresu dat z rozpoznawaniem "Obecnie" (np. `2022 - Obecnie`)
- Wybór szablonu/motywu kolorystycznego i układu strony
- Upload zdjęcia profilowego — widoczne zarówno w podglądzie, jak i w eksportowanych plikach
- Live preview całego CV w czasie rzeczywistym
- Eksport do PDF, DOCX i czystego tekstu (TXT, przyjazny dla systemów ATS)
- Opcjonalna klauzula RODO dodawana automatycznie na dole dokumentu
- Walidacja formularzy — czytelny komunikat o brakujących wymaganych polach oraz podstawowa walidacja formatu emaila
- Zarządzanie wpisami: podgląd, usuwanie oraz zmiana kolejności wpisów (strzałki ↑/↓) w każdej sekcji
- Testy jednostkowe (pytest) dla logiki parsowania dat i walidacji formularzy

## Stack technologiczny

- [Streamlit](https://streamlit.io/) — interfejs i logika aplikacji
- [Pillow](https://python-pillow.org/) — obsługa zdjęcia profilowego
- [fpdf2](https://pyfpdf.github.io/fpdf2/) — generowanie PDF
- [python-docx](https://python-docx.readthedocs.io/) — generowanie DOCX
- [PyMuPDF](https://pymupdf.readthedocs.io/) — praca z plikami PDF
- [pytest](https://docs.pytest.org/) — testy jednostkowe (zależność deweloperska)

## Uruchomienie

```bash
# 1. Sklonuj repozytorium
git clone <adres-repo>
cd CV_creator

# 2. Stwórz środowisko wirtualne
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# 3. Zainstaluj zależności
pip install -r requirements.txt

# (opcjonalnie) zależności deweloperskie, np. do uruchamiania testów
pip install -r requirements-dev.txt

# 4. Uruchom aplikację
streamlit run app.py
```

Aplikacja otworzy się domyślnie pod adresem `http://localhost:8501`.

### Uruchamianie testów

```bash
pytest test_functions.py -v
```

## Struktura projektu

```
CV_creator/
├── app.py
├── functions.py
├── pdf_generator.py
├── docx_generator.py
├── text_generator.py
├── config.py
├── test_functions.py
├── Roboto-Regular.ttf
├── Roboto-Bold.ttf
├── requirements.txt
├── requirements-dev.txt
└── .gitignore
```
