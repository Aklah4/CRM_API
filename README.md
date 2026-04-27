# Task Management & CRM API

A backend REST API for managing tasks and customer relationships, with role-based access control (RBAC) and production-grade query features.

**Stack:** Python 3.10+ · Flask · SQLAlchemy 2.x · MySQL 8.x · Flask-JWT-Extended · Flask-Smorest

---

## Prerequisites

- Python 3.10+
- MySQL 8.x running locally

---

## Local setup

### 1. Clone and create a virtual environment

```bash
git clone <your-repo-url>
cd crm_api
python -m venv venv
```

Activate it:

- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your MySQL credentials and secret keys.

### 4. Create the database

Log into MySQL and run:

```sql
CREATE DATABASE task_crm_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Run database migrations

```bash
flask db upgrade
```

### 6. Start the server

```bash
python run.py
```

The API will be available at `http://localhost:5000`.

---

## Health check

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{ "status": "ok", "env": "development" }
```

---

## Project scope

See [SCOPE.md](SCOPE.md) for the full feature list, sprint plan, and definition of done.
