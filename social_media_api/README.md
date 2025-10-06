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

### Follow / Unfollow

- POST /api/accounts/follow/{user_id}/  — Follow user (auth required)
- DELETE /api/accounts/follow/{user_id}/ — Unfollow user (auth required)
- GET /api/accounts/{user_id}/following/ — Get users {user_id} follows (auth required)
- GET /api/accounts/{user_id}/followers/ — Get users that follow {user_id} (auth required)

Headers: Authorization: Token <token>

Example: POST /api/accounts/follow/3/  (follows user with id 3)

### Feed

- GET /api/feed/ — Returns posts from users the current authenticated user follows. (auth required)
Supports pagination: `?page=`, `?page_size=`

## Likes
- POST /api/posts/{post_id}/like/   — like a post (auth required)
- DELETE /api/posts/{post_id}/like/ — unlike a post (auth required)

## Notifications
- GET /api/notifications/ — list notifications for authenticated user (paginated)
- POST /api/notifications/mark-all-read/ — mark all unread notifications as read

## Notes
- The project uses a custom user model (`accounts.User`) — make sure this is set before initial migrations.
- Media (profile_picture) stored under `/media/` in development.
- Auth is DRF TokenAuth. Include `Authorization: Token <key>` header for protected endpoints.
