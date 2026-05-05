# E-Learning Platform

A production-oriented full-stack E-Learning platform built with a Django REST API backend and a React frontend.

## Tech Stack

- Backend: Django 5, Django REST Framework, SimpleJWT, Channels
- Frontend: React 18, Vite, React Query, Zustand
- Database: PostgreSQL (Neon in production), SQLite (local option)
- Deployment: Render (backend), Vercel (frontend)

## Core Features

- JWT-based authentication (signup, login, token refresh, profile endpoints)
- Courses catalog with details, enrollments, and structured curriculum
- 5-phase learning flow with readings, videos, and phase checkpoints
- Quiz engine with MCQ validation and progress tracking
- Certificate generation workflow for completed learning paths
- Production-ready API docs at `/api/docs/`

## Project Structure

- `backend/` Django project, apps, API, business logic
- `frontend/` React SPA and API client integration
- `generate_report.py` utility for project documentation output

## Local Development (Windows)

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
$env:USE_SQLITE="1"
$env:DJANGO_SETTINGS_MODULE="config.settings.development"
python manage.py migrate
python seed.py
python manage.py runserver 0.0.0.0:8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` and calls backend APIs through configured base URL/proxy.

## Testing

```powershell
cd backend
$env:DJANGO_SETTINGS_MODULE="config.settings.test"
python -m pytest tests -q
```

## Deployment Notes

- Backend (Render): set `DJANGO_SETTINGS_MODULE=config.settings.production` and Postgres env vars.
- Frontend (Vercel): set `VITE_API_BASE_URL=https://<your-render-domain>/api/v1`.
- Add CORS/CSRF trusted origins on backend for the Vercel frontend URL.

## Collaboration Credit

This project was built by **Muhammad Haseeb** with support from partner **Ghania Tanveer**.  
GitHub profile: [ghaniatanveer](https://github.com/ghaniatanveer)
