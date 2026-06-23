# Blog & Newsletter System

A FastAPI REST API combining two modules — blog management and newsletter management — with JWT-based admin authentication. Fully containerized with Docker.

## Features

- **Public blog** — read published articles, no auth required
- **Admin blog** — full CRUD on articles, JWT protected
- **Newsletter** — public subscribe/unsubscribe, admin send & history
- **Auth** — admin login returning a JWT, bcrypt-hashed passwords

## Tech Stack

FastAPI · SQLAlchemy · SQLite · Pydantic · python-jose (JWT) · passlib (bcrypt) · Docker

## Project Structure

```
app/
├── main.py            # entry point, includes all routers
├── database.py        # SQLAlchemy connection + session
├── core/              # config (.env) + security (JWT, hashing)
├── models/            # SQLAlchemy tables
├── schemas/           # Pydantic validation
└── routers/           # public_blog, admin_blog, newsletter, auth
```

## API Routes

| Method | Route | Auth | Description |
|---|---|---|---|
| POST | `/auth/login` | — | Admin login → JWT |
| GET | `/articles` | — | List published articles |
| GET | `/articles/{slug}` | — | Article detail |
| POST | `/admin/article` | JWT | Create article |
| PUT | `/admin/articles/{id}` | JWT | Update article |
| DELETE | `/admin/articles/{id}` | JWT | Delete article |
| POST | `/admin/articles/{id}/publish` | JWT | Publish / unpublish |
| POST | `/subscribe` | — | Subscribe to newsletter |
| GET | `/unsubscribe/{email}` | — | Unsubscribe |
| GET | `/admin/subscribers` | JWT | List active subscribers |
| POST | `/admin/newsletter/send` | JWT | Send a newsletter |
| GET | `/admin/newsletter/history` | JWT | Send history |

## Getting Started

Clone the repo, then create your `.env` from the example:

```bash
cp .env.example .env
```

### With Docker (recommended)

```bash
docker compose up
```

### Without Docker

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open the interactive docs at `http://localhost:8000/docs`

## Roadmap

- [ ] Real email sending in `services/email_service.py`
- [ ] Admin dashboard (`dashboard/index.html`)
- [ ] Persistent volume for the database