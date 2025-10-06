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

## Notes
- The project uses a custom user model (`accounts.User`) — make sure this is set before initial migrations.
- Media (profile_picture) stored under `/media/` in development.
- Auth is DRF TokenAuth. Include `Authorization: Token <key>` header for protected endpoints.
