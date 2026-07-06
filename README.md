# Leave Management System

A full-stack leave approval system with a React front end and FastAPI backend. Employees can request leave by type, managers can approve/reject requests, and administrators can manage leave type policies.

## Frontend (React)
- Navigate to `frontend/` and run `npm install` to install dependencies.
- Start the dev server with `npm start` (uses Create React App under the hood).
- Configurable API endpoint via `frontend/.env` (`REACT_APP_API_BASE_URL`, defaults to `http://localhost:8000`).
- Features: authentication, leave type overview, request form, leave type management (admin), pending approvals dashboard (manager).

## Backend (FastAPI)
- Create a virtual environment and install dependencies from `backend/requirements.txt`.
- Copy `.env.example` to `.env` and adjust secrets if needed.
- Run the server with `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`.
- API includes authentication (`/auth/register`, `/auth/login`), leave type CRUD, leave request workflows, and entitlement summaries.

## Data & Business Rules
- Leave types have annual allowances, descriptions, and approval requirements.
- Users receive entitlements per leave type automatically when they register.
- Leave requests validate overlapping dates and available balance before reserving days.
- Managers/admins can approve or reject requests; approvals decrement balances.

## Development Notes
- SQLAlchemy + SQLite are used for persistence. Switch `SQLALCHEMY_DATABASE_URL` via `.env` for PostgreSQL.
- Alembic is included in `backend/requirements.txt` for future migrations.
- Frontend uses React Router for navigation, Axios for API integration, and context for auth state.
