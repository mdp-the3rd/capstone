# Casting Agency API

This project is the **Casting Agency Capstone** for the Udacity Full Stack Nanodegree (FSND). It demonstrates a production-ready RESTful API with **Role-Based Access Control (RBAC)**, **Auth0 authentication**, **Flask**, **SQLAlchemy**, and **Heroku deployment**.

The Casting Agency models a company responsible for creating movies and managing actors. Different roles have different permissions for interacting with the system.

---

## Live Application

**Base URL:**  
https://capstone-michele-9d06663b5050.herokuapp.com

> All endpoints (except `/`) require authentication via Auth0.

---

## Motivation

This project demonstrates:
- Secure API design with RBAC
- Third-party authentication using Auth0
- Database migrations using Flask-Migrate
- Production deployment on Heroku

The goal is to simulate real-world backend engineering practices.

---

## Tech Stack

- Python 3.10 (Heroku)
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- Auth0 (OAuth2 + JWT)
- PostgreSQL (Heroku)
- Gunicorn

---

## Authentication & Authorization

Authentication is handled by **Auth0** using JSON Web Tokens (JWTs).

### Roles & Permissions

| Role | Permissions |
n|------|------------|
| Casting Assistant | `get:actors`, `get:movies` |
| Casting Director | All Casting Assistant permissions plus:<br>`post:actors`, `patch:actors`, `patch:movies`, `delete:actors` |
| Executive Producer | All permissions including:<br>`post:movies`, `delete:movies` |

Permissions are enforced using a custom `@requires_auth` decorator.

---

## API Endpoints

### Actors

| Method | Endpoint | Permission |
|------|--------|------------|
| GET | `/actors` | `get:actors` |
| POST | `/actors` | `post:actors` |
| PATCH | `/actors/<id>` | `patch:actors` |
| DELETE | `/actors/<id>` | `delete:actors` |

### Movies

| Method | Endpoint | Permission |
|------|--------|------------|
| GET | `/movies` | `get:movies` |
| POST | `/movies` | `post:movies` |
| PATCH | `/movies/<id>` | `patch:movies` |
| DELETE | `/movies/<id>` | `delete:movies` |

---

## Request & Response Examples

### GET /actors

**Request:**
```bash
curl https://capstone-michele-9d06663b5050.herokuapp.com/actors \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1pWTNDMWdYLS1IUVk1ZkVPY0tMRyJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZG5kLnVrLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OTY4YjgxMzBjZTg4MWE2MGY2OTUwMTQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTc2ODQ3MjcwNCwiZXhwIjoxNzY4NDc5OTA0LCJzY29wZSI6IiIsImF6cCI6IlRGM0hLRnBDa1ZWZUlFR0ZpR1JQMWtYcUdjYURrV2M1IiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.G3tydplM1KEbAUIfRW3QdQxQLI9t5FYfRffHmXCncUiMAj3eJ-xvXBvkuZOu3UwnUJyCuZyxka1VFjjBUCPyxyR1GZ83dg82j4VQO4FeNyqBatxVAXHif9dG6J_n0b-TNWCcWvqGjVCW1b7FTY65lD1hPzlj-fId9Lu5SHOOj926SFZpiXjX5fnVJgo_LV-CnLO9egtVWhTspXZPvRYk1OUokG7VIu5iYmlkZxJ5ULt898HacpWTWwl-69Nf2VQruSsCw1yHq4J32G4wOnaKEFzGWSrIpxNG7OLawK-jVWArpVw5HKwLRfhkCE6nv1T1DKfu8hYXLSlHFEZ1Ss2R6A "
```

**Response:**
```json
{
  "success": true,
  "actors": []
}
```

---

## Error Handling

Errors are returned as JSON in the following format:

```json
{
  "success": false,
  "error": 404
}
```

Handled error codes:
- 400 – Bad Request
- 401 – Unauthorized
- 403 – Forbidden
- 404 – Not Found
- 422 – Unprocessable Entity
- 500 – Internal Server Error

---

## Testing

Tests are written using Python’s `unittest` framework.

### To run tests locally:

```bash
python test_app.py
```

Tests include:
- Success and error cases for each endpoint
- RBAC enforcement tests (minimum two per role)

---

## ⚙️ Local Development Setup

### Clone the repository
```bash
git clone <repository-url>
cd heroku_sample
```

### Create and activate virtual environment
```bash
py -3.8 -m venv venv
source venv/Scripts/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set environment variables
```bash
export FLASK_APP=app.py
export DATABASE_URL=sqlite:///database.db
```

### Run migrations
```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

### Run the app
```bash
flask run
```

---

## ☁️ Deployment (Heroku)

### Required environment variables:

```bash
AUTH0_DOMAIN
API_AUDIENCE
DATABASE_URL  # Automatically set by Heroku
```

### Deployment steps:

```bash
git push heroku main
heroku run python3 -m flask db upgrade
```

---

## 🔑 Auth0 Token Setup (for Testing)

1. Log into Auth0 Dashboard
2. Assign a role (Casting Assistant, Director, or Producer) to a user
3. Generate an **Access Token** with:
   - Audience = API Identifier
4. Use the token in request headers:

```http
Authorization: Bearer <JWT>
```

---

## ✅ Project Status

✔ RBAC implemented
✔ Auth0 configured
✔ Database migrations applied
✔ Deployed on Heroku
✔ Tests passing

---

## 🏁 Author

**Michele**  
Udacity Full Stack Nanodegree Capstone Project

---

## 📌 Notes for Reviewers

- Tokens must be generated via Auth0 (not included in repo)
- App uses PostgreSQL in production and SQLite locally
- Python 3.10 is used on Heroku

---

Thank you for reviewing this project 🙌

