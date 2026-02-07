# Research Development System (RDS)

RDS is an academic infrastructure platform that enforces research rigor before any drafting occurs. The system encodes supervision logic, measurable quality scoring, and AI transparency at the data-model and workflow levels.

## Architecture

- **Backend:** Django + Django REST Framework, PostgreSQL, JWT authentication.
- **Frontend:** React (Vite) with a mobile-first, low-bandwidth layout.
- **AI governance:** All AI output is stored separately, traceable to student responses, and auditable through AI transparency logs.

## Core safeguards encoded in the data model

- **Thinking precedes writing:** Proposal sections record completeness scores and thresholds to block progression until inputs are sufficient.
- **No generation without completeness:** Generated sections require source response IDs and AI contribution percentages.
- **Alignment enforcement:** Alignment checks are stored as blocking or non-blocking events tied to proposals.
- **Supervisor oversight:** Supervisor reviews are recorded with statuses and comments.
- **Audit trail:** Versioning and export records capture snapshots and compliance statements.
- **Guardrails:** Methodology guardrails require variables for quantitative designs and enforce analysis plans.

## Repository layout

```
backend/      Django project and core app
frontend/     React app for student + supervisor experiences
```

## Backend setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary
cd backend
python manage.py migrate
python manage.py runserver
```

## Frontend setup

```bash
cd frontend
npm install
npm run start
```

## Data integrity requirements

- AI-generated sections must reference student response IDs.
- AI contributions are logged with model name, prompt, and input response IDs.
- Quality scores and Defense Readiness Index are computed and auditable.
- Supervisor prompts surface blocking examiner-style feedback when critical gaps remain.
