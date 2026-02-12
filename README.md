# KanMind Backend - Django REST API

A Django-based backend for a Kanban board application with user authentication, board management, and task management.

## 📋 Table of Contents

- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## 🛠 Technology Stack

- **Backend Framework:** Django 6.0.2
- **API:** Django REST Framework 3.16.1
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Authentication:** Token-based Authentication
- **CORS:** django-cors-headers for Frontend Integration
- **Environment Management:** python-decouple

## 📦 Prerequisites

Make sure the following software is installed:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (Python Package Installer)
- **Git** (optional, for version control)

## 🚀 Installation

### Step 1: Clone/Download Repository

```bash
# If using Git
git clone <repository-url>
cd KanMind/BACKEND/KanMind

# Or: Download and extract files manually
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 4: Configure Environment Variables

Sensitive data is managed in a `.env` file. **Create a .env file based on .env.example:**

```bash
# Copy .env.example to .env
cp .env.example .env

# Windows:
copy .env.example .env
```

**Then edit the .env file and adjust the values:**
- Generate a new `SECRET_KEY` (see Step 5)
- Configure `ALLOWED_HOSTS` for your domain
- Set `DEBUG=False` for production

**⚠️ Security Notes:**
- **NEVER** commit the `.env` file to Git (already included in .gitignore)
- **Production:** Generate a new SECRET_KEY for production
- **Production:** Set `DEBUG=False`
- **Production:** Configure `ALLOWED_HOSTS` according to your domain
- **Privacy:** Use strong, unique passwords

### Step 5: Generate New SECRET_KEY

**⚠️ IMPORTANT:** Always generate a new SECRET_KEY for your installation:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key and replace `your-secret-key-here` in your `.env` file.

## 🗄️ Database Setup

### Step 6: Run Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 7: Create Superuser

```bash
# Create administrator account
python manage.py createsuperuser
```

Follow the instructions and enter:
- Username
- Email address
- Password

## 🚀 Start Development Server

### Step 8: Start Server

```bash
# Start development server
python manage.py runserver
```

The server is now accessible at `http://127.0.0.1:8000`.

**Admin Interface:** `http://127.0.0.1:8000/admin` (with superuser credentials)

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Boards
- `GET /api/boards/` - Get all boards
- `POST /api/boards/` - Create new board
- `GET /api/boards/{id}/` - Board details
- `PUT /api/boards/{id}/` - Update board
- `DELETE /api/boards/{id}/` - Delete board

### Tasks
- `GET /api/tasks/` - Get all tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

## 💻 Development

### Project Structure

```
KanMind/
├── manage.py                 # Django Management Script
├── requirements.txt          # Python Dependencies
├── .env                     # Environment Variables (NOT in Git!)
├── .env.example             # Example Environment Variables
├── .gitignore               # Git Ignore Rules
├── db.sqlite3               # SQLite Database
├── core/                    # Django Main Configuration
│   ├── settings.py         # Django Settings
│   ├── urls.py             # URL Configuration
│   └── wsgi.py             # WSGI Configuration
├── auth_app/               # User Authentication
│   ├── models.py           # User Data Models
│   ├── api/                # Authentication API
├── boards_app/             # Board Management
│   ├── models.py           # Board Data Models
│   ├── api/                # Board API
└── tasks_app/              # Task Management
    ├── models.py           # Task Data Models
    └── api/                # Task API
```

### Code Quality

```bash
# Check PEP 8 compliance
flake8 core/ auth_app/ boards_app/ tasks_app/

# Check import order
isort --check-only core/ auth_app/ boards_app/ tasks_app/

# Automatically format code
black core/ auth_app/ boards_app/ tasks_app/

# Automatically sort imports
isort core/ auth_app/ boards_app/ tasks_app/

# Run tests
python manage.py test

# Check migration status
python manage.py showmigrations

# Django Shell for debugging
python manage.py shell
```

### Frontend Integration (CORS)

The backend is configured for the following frontend URLs:
- `http://localhost:3000` (React)
- `http://localhost:5000` (Flask/Vanilla JS)
- `http://localhost:5500` (Live Server)
- `http://localhost:8080` (Vue.js)

## 🚢 Deployment

### Prepare Production Environment

1. **Environment Variables for Production:**
   ```env
   SECRET_KEY=<your-production-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_ENGINE=django.db.backends.postgresql
   CORS_ALLOW_ALL_ORIGINS=False
   ```

2. **PostgreSQL for Production:**
   ```env
   DATABASE_NAME=kanmind_db
   DATABASE_USER=kanmind_user
   DATABASE_PASSWORD=your-secure-password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

### Heroku Deployment

1. **Create Procfile:**
   ```
   web: gunicorn core.wsgi --log-file -
   ```

2. **Create runtime.txt:**
   ```
   python-3.9.16
   ```

3. **Extend Requirements for Production:**
   ```
   gunicorn==20.1.0
   psycopg2-binary==2.9.7
   django-heroku==0.3.1
   ```

## 🔧 Troubleshooting

### Common Issues

#### 1. Virtual Environment Activation Problems
```bash
# Windows PowerShell Execution Policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

#### 3. Migration Errors
```bash
# Reset migrations
python manage.py migrate --fake-initial
```

#### 4. CORS Errors
- Check `CORS_ALLOWED_ORIGINS` in [settings.py](core/settings.py)
- Add frontend URL to the list

#### 5. Authentication Token Issues
```bash
# New tokens can be created in Django Admin
http://127.0.0.1:8000/admin/authtoken/tokenproxy/
```

## 📱 API Usage Examples

### Register User
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

### Create Board (with Authentication Token)
```bash
curl -X POST http://127.0.0.1:8000/api/boards/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "name": "My Kanban Board", 
    "description": "Project Management Board"
  }'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

## 📞 Support

For questions or issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Search for existing issues
3. Create a new issue with detailed description

---

**Development environment successfully set up!** 🎉

Next steps:
1. Develop frontend and connect to API
2. Implement additional features
3. Write tests
4. Deploy to production