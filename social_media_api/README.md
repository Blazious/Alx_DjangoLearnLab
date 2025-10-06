# Alx_DjangoLearnLab / social_media_api

## Quick start
1. Clone the repo
2. Create & activate venv
3. Install dependencies:
   pip install -r requirements.txt
   # or
   pip install django djangorestframework pillow
4. Configure settings (SECRET_KEY, DEBUG, DB settings)
5. Run migrations:
   python manage.py makemigrations
   python manage.py migrate
6. Create superuser:
   python manage.py createsuperuser
7. Start dev server:
   python manage.py runserver

## Endpoints
- POST /api/accounts/register/  → register (returns token)
- POST /api/accounts/login/     → login (returns token)
- GET/PUT /api/accounts/profile/ → get or update authenticated user's profile

## Posts & Comments API

### Endpoints
- `GET /api/posts/` — list posts (supports `?search=`, `?page=`, `?page_size=`)
- `POST /api/posts/` — create a post (auth required)
- `GET /api/posts/{id}/` — retrieve post with nested comments
- `PUT /api/posts/{id}/` — update (author only)
- `DELETE /api/posts/{id}/` — delete (author only)

- `GET /api/comments/` — list comments (supports `?search=`)
- `POST /api/comments/` — create a comment (body: `{"post": <post_id>, "content": "..."}`)
- `GET /api/comments/{id}/` — retrieve comment
- `PUT /api/comments/{id}/` — update (author only)
- `DELETE /api/comments/{id}/` — delete (author only)

### Authentication
- Use `Authorization: Token <key>` header. Register / login endpoints are in `accounts` app.

### Examples
Create post:

## Notes
- The project uses a custom user model (`accounts.User`) — make sure this is set before initial migrations.
- Media (profile_picture) stored under `/media/` in development.
- Auth is DRF TokenAuth. Include `Authorization: Token <key>` header for protected endpoints.
