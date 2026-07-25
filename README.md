# CV Generator

Aplikacja webowa do tworzenia CV w kilka minut — wypełniasz formularz, na bieżąco widzisz podgląd, a na końcu eksportujesz gotowy dokument do PDF lub Word.

# 1. Funkcje
  Formularz danych osobowych, kontaktowych i opisu "O sobie"
  Sekcje: doświadczenie zawodowe, edukacja, umiejętności (z opcjonalną skalą zaawansowania), języki obce, certyfikaty i kursy
  Obsługa zakresu dat z rozpoznawaniem "Obecnie" (np. 2022 - Obecnie)
  Wybór szablonu/motywu kolorystycznego i układu strony
  Upload zdjęcia profilowego — widoczne zarówno w podglądzie, jak i w eksportowanych plikach
  Live preview całego CV w czasie rzeczywistym
  Eksport do PDF i DOCX
  Opcjonalna klauzula RODO dodawana automatycznie na dole dokumentu
  Zarządzanie wpisami (podgląd i usuwanie dodanych sekcji)
  
# 2. Stack technologiczny
  Streamlit — interfejs i logika aplikacji
  Pillow — obsługa zdjęcia profilowego
  fpdf2 — generowanie PDF
  python-docx — generowanie DOCX
  PyMuPDF — praca z plikami PDF
  
# 3. Uruchomienie
  bash
  # 3.1. Sklonuj repozytorium
  git clone <adres-repo>
  cd CV_creator
  
  # 3.2. Stwórz środowisko wirtualne
  python -m venv venv
  venv\Scripts\activate      # Windows
  source venv/bin/activate   # Linux/Mac
  
  # 3.3. Zainstaluj zależności
  pip install -r requirements.txt
  
  # 3.4. Uruchom aplikację
  streamlit run app.py

  Aplikacja otworzy się domyślnie pod adresem http://localhost:8501.

# 4. Struktura projektu
  CV_creator/
  ├── app.py                # Główny plik aplikacji Streamlit — UI i live preview
  ├── functions.py          # Logika formularzy sekcji i zarządzania wpisami
  ├── pdf_generator.py      # Generowanie CV w formacie PDF
  ├── docx_generator.py     # Generowanie CV w formacie DOCX
  ├── config.py             # Konfiguracja sekcji, szablonów i tekstu RODO
  ├── Roboto-Regular.ttf    # Font użyty przy generowaniu PDF
  ├── Roboto-Bold.ttf       # Font użyty przy generowaniu PDF
  ├── requirements.txt
  └── .gitignore
