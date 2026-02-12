# KanMind Backend - Django REST API

Ein Django-basiertes Backend für eine Kanban-Board-Anwendung mit Benutzerauthentifizierung, Board-Management und Aufgabenverwaltung.

## 📋 Inhaltsverzeichnis

- [Technologie-Stack](#technologie-stack)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Database Setup](#database-setup)
- [API-Endpunkte](#api-endpunkte)
- [Entwicklung](#entwicklung)
- [Deployment](#deployment)
- [Fehlerbehebung](#fehlerbehebung)

## 🛠 Technologie-Stack

- **Backend Framework:** Django 6.0.2
- **API:** Django REST Framework 3.16.1
- **Datenbank:** SQLite (Entwicklung) / PostgreSQL (Produktion)
- **Authentifizierung:** Token-basierte Authentifizierung
- **CORS:** django-cors-headers für Frontend-Integration
- **Environment Management:** python-decouple

## 📦 Voraussetzungen

Stellen Sie sicher, dass folgende Software installiert ist:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (Python Package Installer)
- **Git** (optional, für Versionskontrolle)

## 🚀 Installation

### Schritt 1: Repository klonen/herunterladen

```bash
# Falls Sie Git verwenden
git clone <repository-url>
cd KanMind/BACKEND/KanMind

# Oder: Dateien manuell herunterladen und extrahieren
```

### Schritt 2: Virtuelle Umgebung erstellen

```bash
# Virtuelle Umgebung erstellen
python -m venv .venv

# Virtuelle Umgebung aktivieren
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### Schritt 3: Dependencies installieren

```bash
# Alle erforderlichen Pakete installieren
pip install -r requirements.txt
```

## ⚙️ Konfiguration

### Schritt 4: Umgebungsvariablen konfigurieren

Die sensiblen Daten werden in einer `.env` Datei verwaltet. **Erstellen Sie eine .env Datei basierend auf .env.example:**

```bash
# .env.example nach .env kopieren
cp .env.example .env

# Windows:
copy .env.example .env
```

**Bearbeiten Sie dann die .env Datei und passen Sie die Werte an:**
- Generieren Sie einen neuen `SECRET_KEY` (siehe Schritt 5)
- Konfigurieren Sie `ALLOWED_HOSTS` für Ihre Domain
- Setzen Sie `DEBUG=False` für Produktion

**⚠️ Sicherheitshinweise:**
- **NIEMALS** die `.env` Datei in Git committen (ist bereits in .gitignore)
- **Produktion:** Generieren Sie einen neuen SECRET_KEY für die Produktion
- **Produktion:** Setzen Sie `DEBUG=False`
- **Produktion:** Konfigurieren Sie `ALLOWED_HOSTS` entsprechend Ihrer Domain
- **Datenschutz:** Verwenden Sie starke, einzigartige Passwörter

### Schritt 5: Neuen SECRET_KEY generieren

**⚠️ WICHTIG:** Generieren Sie immer einen neuen SECRET_KEY für Ihre Installation:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Kopieren Sie den generierten Key und ersetzen Sie `your-secret-key-here` in Ihrer `.env` Datei.

## 🗄️ Database Setup

### Schritt 6: Datenbank-Migrationen durchführen

```bash
# Migrationen erstellen
python manage.py makemigrations

# Migrationen anwenden
python manage.py migrate
```

### Schritt 7: Superuser erstellen

```bash
# Administratorkonto erstellen
python manage.py createsuperuser
```

Folgen Sie den Anweisungen und geben Sie ein:
- Username
- Email-Adresse
- Passwort

## 🚀 Entwicklungsserver starten

### Schritt 8: Server starten

```bash
# Entwicklungsserver starten
python manage.py runserver
```

Der Server ist nun unter `http://127.0.0.1:8000` erreichbar.

**Admin-Interface:** `http://127.0.0.1:8000/admin` (mit Superuser-Credentials)

## 🔗 API-Endpunkte

### Authentifizierung
- `POST /api/auth/register/` - Benutzerregistrierung
- `POST /api/auth/login/` - Benutzeranmeldung
- `POST /api/auth/logout/` - Benutzerabmeldung

### Boards
- `GET /api/boards/` - Alle Boards abrufen
- `POST /api/boards/` - Neues Board erstellen
- `GET /api/boards/{id}/` - Board-Details
- `PUT /api/boards/{id}/` - Board aktualisieren
- `DELETE /api/boards/{id}/` - Board löschen

### Tasks
- `GET /api/tasks/` - Alle Aufgaben abrufen
- `POST /api/tasks/` - Neue Aufgabe erstellen
- `GET /api/tasks/{id}/` - Aufgaben-Details
- `PUT /api/tasks/{id}/` - Aufgabe aktualisieren
- `DELETE /api/tasks/{id}/` - Aufgabe löschen

## 💻 Entwicklung

### Projektstruktur

```
KanMind/
├── manage.py                 # Django Management-Skript
├── requirements.txt          # Python Dependencies
├── .env                     # Umgebungsvariablen (NICHT in Git!)
├── .env.example             # Beispiel-Umgebungsvariablen
├── .gitignore               # Git-Ignorier-Regeln
├── db.sqlite3               # SQLite Datenbank
├── core/                    # Django Hauptkonfiguration
│   ├── settings.py         # Django Einstellungen
│   ├── urls.py             # URL-Konfiguration
│   └── wsgi.py             # WSGI Konfiguration
├── auth_app/               # Benutzerauthentifizierung
│   ├── models.py           # Benutzerdatenmodelle
│   ├── api/                # Authentication API
├── boards_app/             # Board-Management
│   ├── models.py           # Board-Datenmodelle
│   ├── api/                # Board API
└── tasks_app/              # Aufgabenverwaltung
    ├── models.py           # Task-Datenmodelle
    └── api/                # Task API
```

### Code-Qualität

```bash
# Tests ausführen
python manage.py test

# Migrationsstatus überprüfen
python manage.py showmigrations

# Django Shell für Debugging
python manage.py shell
```

### Frontend Integration (CORS)

Das Backend ist für folgende Frontend-URLs konfiguriert:
- `http://localhost:3000` (React)
- `http://localhost:5000` (Flask/Vanilla JS)
- `http://localhost:5500` (Live Server)
- `http://localhost:8080` (Vue.js)

## 🚢 Deployment

### Produktionsumgebung vorbereiten

1. **Umgebungsvariablen für Produktion:**
   ```env
   SECRET_KEY=<your-production-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_ENGINE=django.db.backends.postgresql
   CORS_ALLOW_ALL_ORIGINS=False
   ```

2. **PostgreSQL für Produktion:**
   ```env
   DATABASE_NAME=kanmind_db
   DATABASE_USER=kanmind_user
   DATABASE_PASSWORD=your-secure-password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

3. **Statische Dateien sammeln:**
   ```bash
   python manage.py collectstatic
   ```

### Heroku Deployment

1. **Procfile erstellen:**
   ```
   web: gunicorn core.wsgi --log-file -
   ```

2. **runtime.txt erstellen:**
   ```
   python-3.9.16
   ```

3. **Requirements für Produktion erweitern:**
   ```
   gunicorn==20.1.0
   psycopg2-binary==2.9.7
   django-heroku==0.3.1
   ```

## 🔧 Fehlerbehebung

### Häufige Probleme

#### 1. Virtual Environment Aktivierungsprobleme
```bash
# Windows PowerShell Execution Policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. Port bereits in Verwendung
```bash
# Anderen Port verwenden
python manage.py runserver 8001
```

#### 3. Migrationsfehler
```bash
# Migrationen zurücksetzen
python manage.py migrate --fake-initial
```

#### 4. CORS-Fehler
- Überprüfen Sie die `CORS_ALLOWED_ORIGINS` in [settings.py](core/settings.py)
- Frontend-URL zur Liste hinzufügen

#### 5. Authentication Token Probleme
```bash
# Neue Tokens können im Django Admin erstellt werden
http://127.0.0.1:8000/admin/authtoken/tokenproxy/
```

## 📱 API-Nutzung Beispiele

### Benutzer registrieren
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "securepassword123",
    "password2": "securepassword123"
  }'
```

### Board erstellen (mit Authentication Token)
```bash
curl -X POST http://127.0.0.1:8000/api/boards/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "name": "Mein Kanban Board", 
    "description": "Projektmanagement Board"
  }'
```

## 🤝 Contributing

1. Fork das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Commit Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

## 📄 Lizenz

Dieses Projekt steht unter der MIT Lizenz. Siehe `LICENSE` Datei für Details.

## 📞 Support

Bei Fragen oder Problemen:
1. Überprüfen Sie die [Fehlerbehebung](#fehlerbehebung) Sektion
2. Suchen Sie nach bestehenden Issues
3. Erstellen Sie ein neues Issue mit detaillierter Beschreibung

---

**Entwicklungsumgebung erfolgreich eingerichtet!** 🎉

Nächste Schritte:
1. Frontend entwickeln und mit der API verbinden
2. Zusätzliche Features implementieren
3. Tests schreiben
4. Für Produktion deployen