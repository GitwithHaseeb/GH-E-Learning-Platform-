# E-Learning Platform (Django REST API + React)

Production-style monorepo: **Django 5 + DRF** backend and **React 18 + Vite** frontend.

## Quick start (Windows / local demo)

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

Demo admin: `admin@demo.com` / `Adminpass123!` (after `seed.py`).

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` — API calls proxy to `http://127.0.0.1:8000`.

### Tests

```powershell
cd backend
$env:DJANGO_SETTINGS_MODULE="config.settings.test"
python -m pytest tests -q
```

### Word report

```powershell
cd ..
pip install python-docx
python generate_report.py --output E_Learning_Project_Report.docx
```

## Structure

- `backend/` — Django project (`config/`), apps under `apps/`, shared `core/`
- `frontend/` — Vite React SPA
- `generate_report.py` — DOCX generator
- `docs/` — extra notes (optional)

## Environment

See `backend/.env.example`. For PostgreSQL + Redis production paths, set `USE_SQLITE=0` and provide DB/Redis URLs.

## Notes

- **JWT**: access/refresh via `/api/v1/auth/login/`; optional HttpOnly cookies set on login view.
- **Stripe**: without `STRIPE_SECRET_KEY`, checkout creates a **paid demo order** so flows remain testable.
- **WebSocket**: `ws://localhost:8000/ws/chat/<room_name>/` (same-site session auth easiest in dev).
- **Elasticsearch**: not bundled; use `search` query param via DRF `SearchFilter` (swap to ES later).
