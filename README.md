# 🚌 Rozkład Jazdy Brodnica

**System informacji pasażerskiej dla komunikacji miejskiej w Brodnicy**

---

## ⚠️ Uwaga - Projekt w rozwoju

🚧 **Ten projekt jest obecnie w fazie rozwoju i nie jest kompletny!**

- ⏰ **Godziny odjazdów mogą być nieaktualne**
- 🗺️ **Niektóre trasy mogą być niepełne lub testowe**  
- 🔧 **System może zawierać błędy i być niestabilny**
- 📱 **Funkcjonalności są dodawane i testowane**

**❌ Nie używaj tego systemu do planowania rzeczywistych podróży!**

---

## 📋 Opis projektu

Profesjonalna aplikacja webowa do sprawdzania rozkładów jazdy autobusów miejskich w Brodnicy. System umożliwia:

- 🗺️ **Planowanie podróży** - wybór przystanku startowego i docelowego
- 🚌 **Przeglądanie tras** - szczegółowe informacje o liniach autobusowych  
- 🤖 **Asystent AI** - chatbot pomocny w znajdowaniu połączeń
- 📱 **Responsywny design** - działa na komputerze i telefonie
- ⏱️ **Aktualizacje na żywo** - dane odświeżane co 30 sekund

---

## 🚀 Szybki start

### Wymagania

- Python 3.8+
- Flask
- Ollama (dla chatbota AI)

### Instalacja

1. **Sklonuj repozytorium:**
```bash
git clone [adres-repo]
cd buss
```

2. **Utwórz środowisko wirtualne:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# lub
.venv\Scripts\activate     # Windows
```

3. **Zainstaluj zależności:**
```bash
pip install -r requirements.txt
```

4. **Zainstaluj Ollama (dla chatbota):**
```bash
# Pobierz Ollama z https://ollama.ai
ollama pull llama3.2:1b
```

5. **Uruchom aplikację:**
```bash
python app.py
```

6. **Otwórz w przeglądarce:**
```
http://localhost:5001
```

---

## 🏗️ Struktura projektu

```
buss/
├── app.py                 # Główna aplikacja Flask
├── requirements.txt       # Zależności Python
├── README.md             # Ten plik
├── static/
│   ├── css/
│   │   ├── style.css                # Style główne
│   │   └── background-options.css   # Tło aplikacji
│   ├── images/
│   │   └── background.JPG           # Zdjęcie tła
│   └── js/
│       └── script.js                # Logika frontend
└── templates/
    └── index.html                   # Szablon strony
```

---

## 🤖 Chatbot AI

Aplikacja zawiera zaawansowany chatbot AI oparty na modelu **LLaMA 3.2**, który:

- ✅ Odpowiada na pytania o połączenia autobusowe
- ✅ Zna aktualne rozkłady jazdy  
- ✅ Pomaga planować podróże
- ✅ Działa w języku polskim

---

## 🎨 Funkcjonalności

### 🗺️ Planowanie podróży
- Wybór przystanku startowego z listy
- Wybór przystanku docelowego
- Automatyczne znajdowanie połączeń
- Wyświetlanie dostępnych tras

### ℹ️ Szczegółowe informacje  
- Rozwinięcie tras z wszystkimi przystankami
- Czasy przejazdu między przystankami
- Informacje o liniach autobusowych
- Legenda z opisem systemu

### 💎 Interface użytkownika
- Elegancki design z tłem fotograficznym
- Responsywność na wszystkich urządzeniach  
- Profesjonalne ikony i animacje
- Intuicyjna nawigacja

---

## 🛠️ Stack technologiczny

- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **AI:** Ollama + LLaMA 3.2
- **Styling:** Custom CSS + Font Awesome
- **Database:** In-memory (JSON structure)

---

## � Screenshot

![Bus Schedule App](static/images/background.JPG)

---

## �📞 Kontakt

W przypadku pytań lub problemów z projektem, skontaktuj się z deweloperem.

---

## 📝 Licencja

Ten projekt jest dostępny na licencji MIT.

---

<div align="center">

**Ostatnia aktualizacja:** 2 sierpnia 2025  
**Status:** 🚧 W rozwoju  
**Wersja:** 0.1.0-alpha

[![Made with ❤️ in Poland](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red.svg)](https://en.wikipedia.org/wiki/Poland)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)

</div>