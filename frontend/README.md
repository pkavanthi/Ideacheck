# Frontend

React + TypeScript + Vite UI for the National Resilience Intelligence Backbone API.

## Setup
```bash
cd frontend
cp .env.example .env     # VITE_API_URL defaults to http://localhost:8000
npm install
npm run dev              # http://localhost:3000 (matches backend CORS default)
```

Start the backend first (`uvicorn main:app --reload` in `backend/`). Sign in with the backend's `API_KEY`; it is kept in `sessionStorage` only for the browser session.

## Features
- Incidents and Resources tables with filtering, pagination, create / edit / delete
- API-key login with automatic sign-out on 401
- Server validation messages shown in forms

## Scripts
- `npm run dev` – dev server
- `npm run build` – typecheck + production build
