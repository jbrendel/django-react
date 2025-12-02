# Django-React Application

A full-stack web application with Django REST API backend and React TypeScript
frontend.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL
- pyenv (for virtual environment management)

### Quick Setup for Local Development

**1. Activate Python virtual environment:**
```bash
pyenv activate django-react
```

**2. Install backend dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**3. Set up database and run migrations:**
```bash
# Create database (adjust for your PostgreSQL setup)
createdb django_react_db

# Run migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser
```

**4. Install frontend dependencies:**
```bash
cd ../frontend
npm install
```

**5. Start development servers:**

Open two terminal windows/tabs:

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

**6. Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

---

## Project Structure

```
django-react/
├── backend/          # Django REST API
├── frontend/         # React TypeScript SPA
└── docs/            # Documentation
```

## Technology Stack

**Backend:**
- Django 5.x + Django REST Framework
- PostgreSQL
- JWT Authentication (djangorestframework-simplejwt)

**Frontend:**
- React 18+ with TypeScript
- Vite (build tool)
- React Router (routing)
- Axios (HTTP client)
- Zustand (state management)
- Tailwind CSS + Shadcn/ui (styling)

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete project documentation and development
  guidelines
- **[docs/CHOICES.md](docs/CHOICES.md)** - Detailed technology choice
  rationale and alternatives

## Development

See [CLAUDE.md](CLAUDE.md) for detailed development workflows, coding
standards, and deployment instructions.

## License

[Add your license here]
