# Project Scope — Task Management & CRM API

**Last updated:** 2026-04-25
**Status:** Locked for v1

---

## One-line goal

A backend REST API where users can manage tasks and customer relationships, with role-based access control and production-grade query features.

## Emphasis

Tasks and Customers are **equal-weight first-class resources**. Both get full CRUD, full query features, full RBAC, full documentation. Tasks may optionally link to customers, but neither is "the main one."

## Time horizon

No deadline. The goal is **deep understanding**, not speed. Each concept gets explained, written, and reviewed before moving on.

---

## In scope (the must-haves)

### 1. Authentication

- User registration
- Login / logout
- JWT access + refresh tokens
- Password hashing (bcrypt)
- Token expiry and refresh flow

### 2. Authorization (RBAC)

- Three roles: `admin`, `manager`, `user`
- Endpoint-level role gates via `@role_required(...)` decorator
- Resource-level ownership rules:
  - Users see/edit only their own resources
  - Managers see/edit their team's
  - Admins see/edit everything

### 3. Tasks resource (full CRUD)

- Fields: `title`, `description`, `status`, `priority`, `due_date`, `assigned_to`, `customer_id` (optional)
- Statuses: `todo`, `in_progress`, `done`, `archived`
- Priorities: `low`, `medium`, `high`, `urgent`

### 4. Customers resource (full CRUD)

- Fields: `name`, `email`, `phone`, `company`, `status`, `tags`, `notes`, `assigned_to`
- Statuses: `lead`, `prospect`, `active`, `churned`

### 5. Query features (on all list endpoints)

- Pagination — `?page=2&limit=20`
- Filtering — `?status=todo&priority=high,urgent`
- Sorting — `?sort=-due_date,title`
- Search — `?search=acme` (full-text on selected fields)
- Field selection — `?fields=id,title,status`

### 6. Error handling

- Consistent JSON error shape: `{ "success": false, "error": { "message": "...", "statusCode": 400, "details": [...] } }`
- Correct HTTP status codes: 200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500
- Validation errors include the field that failed and why

### 7. OpenAPI documentation

- Auto-generated from Marshmallow schemas via Flask-Smorest
- Interactive Swagger UI at `/docs`
- Every endpoint documented with examples

---

## Out of scope (explicit non-goals for v1)

These are **not** part of this project. If you find yourself building them, you're scope-creeping.

- ❌ Frontend / UI — this is JSON-only
- ❌ Email sending (no password reset emails, no notifications)
- ❌ File uploads (no avatars, no attachments)
- ❌ WebSockets / real-time features
- ❌ Third-party integrations (Slack, Google Calendar, Stripe, etc.)
- ❌ Multi-tenancy (single org, single user pool)
- ❌ Audit logs ("who changed what when")
- ❌ Analytics / reporting endpoints
- ❌ Soft deletes (delete = gone)
- ❌ Comprehensive automated test suite (optional bonus only)
- ❌ Live deployment (we cover what's needed _to_ deploy, but don't deploy)

---

## Definition of Done

The project is finished when **all** of the following are true:

- [ ] All 7 core features work end-to-end
- [ ] Two users can be registered with different roles, each can login and get tokens
- [ ] Tasks can be created, listed (with pagination + filter + sort + search), updated, deleted
- [ ] Customers can be created, listed (same query features), updated, deleted
- [ ] Tasks can be linked to customers; `GET /customers/:id/tasks` works
- [ ] RBAC blocks unauthorized actions with the correct status codes
- [ ] `/docs` shows complete interactive Swagger UI
- [ ] `README.md` explains how to clone and run locally
- [ ] `requirements.txt` and `.env.example` are committed

---

## Tech stack (locked)

| Layer                    | Choice                                |
| ------------------------ | ------------------------------------- |
| Language                 | Python 3.10+                          |
| Framework                | Flask                                 |
| ORM                      | SQLAlchemy 2.x (via Flask-SQLAlchemy) |
| Database                 | MySQL 8.x                             |
| Auth                     | Flask-JWT-Extended                    |
| Validation/Serialization | Marshmallow                           |
| API framework            | Flask-Smorest                         |
| Password hashing         | bcrypt (via Flask-Bcrypt or passlib)  |
| Rate limiting            | Flask-Limiter                         |
| Env management           | python-dotenv                         |

---

## Sprint plan

| Sprint                 | Goal                                                               | Demo                                              |
| ---------------------- | ------------------------------------------------------------------ | ------------------------------------------------- |
| 0 — Foundation         | App boots, MySQL connected                                         | `/health` returns JSON, `SELECT 1` works          |
| 1 — Authentication     | JWT register/login/refresh                                         | Register + login via curl, get tokens             |
| 2 — Authorization      | RBAC + ownership rules                                             | Admin sees all users, regular user gets 403       |
| 3 — Tasks resource     | Task CRUD + Swagger UI                                             | Create tasks via `/docs`, see auto-generated spec |
| 4 — Customers resource | Customer CRUD + task↔customer link                                 | Full CRM data model                               |
| 5 — Query layer        | Pagination, filter, sort, search                                   | `/tasks?status=todo&sort=-due_date&page=2` works  |
| 6 — Production polish  | Error handling, status codes, rate limit, security headers, README | API ready to demo / put on portfolio              |

---

## Scope-creep policy

If during the build you (or I) suggest a feature not on the in-scope list above, it goes into `BACKLOG.md` instead of getting built. Examples of things that will sound tempting but aren't in v1:

- "Let's add comments on tasks"
- "Let's track who created vs assigned a task"
- "Let's add tags as a separate table"
- "Let's add team/group concept"
- "Let's add password reset"
- "Let's add 2FA"

All of these are great ideas. None of them are in v1.
