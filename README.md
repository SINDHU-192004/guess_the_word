# Guess the Word – Django Web App

A full-stack Wordle-style 5-letter word guessing game built with Python Django. Includes player registration/login, daily play limits, guess feedback (green/orange/grey), history, and admin dashboards/reports.

---

## Author
- Name: SINDHU T
- University: REVA UNIVERSITY
- Role: Intern @ OpenText (Onboarding 2025)

---

## Project Summary
This project fulfills the “Guess the Word” specifications provided by OpenText for pre-onboarding assignment. It supports two user types:
- Player users: play the guessing game (max 3 games/day, 5 guesses per game)
- Admin users: manage words and view reports

At game start, a random 5-letter uppercase word is chosen. Each submitted guess shows per-letter feedback:
- Green: correct letter in correct position
- Orange: correct letter in wrong position
- Grey: letter not in target word

All words selected and guesses (with dates) are stored in the database. Admins can view day-wise and user-wise reports.

---

## Tech Stack
- Python 3.10+
- Django 4.2
- SQLite (development default)
- Bootstrap 5, Font Awesome

---

## Repository Structure
```
guess_the_word/
├─ manage.py
├─ requirements.txt
├─ guess_the_word_project/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ asgi.py
├─ game/
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ signals.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ templatetags/
│  │  ├─ __init__.py
│  │  └─ custom_filters.py
│  └─ management/
│     └─ commands/
│        └─ populate_words.py
├─ templates/
│  ├─ base.html
│  ├─ registration/
│  │  ├─ login.html
│  │  └─ register.html
│  └─ game/
│     ├─ home.html
│     ├─ dashboard.html
│     ├─ play.html
│     ├─ result.html
│     ├─ history.html
│     ├─ admin_dashboard.html
│     ├─ admin_reports.html
│     └─ manage_words.html
└─ static/
   └─ js/
      └─ app.js
```

---

## How to Run Locally (Windows PowerShell)
Run these from the project root: `c:/Users/91636/Desktop/guess_the_word`

1) Create a virtual environment and install dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2) Apply database migrations and create an admin user
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
Follow prompts to set username/email/password. This account will be an Admin (Django staff) and can access Admin features.

3) Load initial 20 words
```powershell
python manage.py populate_words
```
You should see a summary indicating words created or already existing.

4) Start the development server
```powershell
python manage.py runserver
```
Open http://127.0.0.1:8000/ in your browser.

---

## Using the Application
- Home (not logged in): links to Register and Login
- Register: username and password rules enforced
  - Username: at least 5 characters, must include both uppercase and lowercase letters
  - Password: at least 5 characters, must include letters, a number, and one of $, %, *, @
- Dashboard (logged in): shows stats and today’s usage; start a new game if under daily limit (max 3)
- Gameplay:
  - Enter a 5-letter uppercase word
  - You have 5 total guesses
  - After each guess, letters are colored: green/orange/grey
  - On success, you’ll see a congratulatory result; on failure after 5 guesses, a “better luck next time” result
- History: list of completed games with outcomes

### Admin Features
Admin menu appears when logged in as a staff/superuser.
- Admin Dashboard: quick stats
- Reports:
  - Daily report: date, number of users, total games, correct guesses, success rate
  - User report: date-wise counts of words tried and correct guesses
- Manage Words: add new 5-letter uppercase words; activate/deactivate words
- Django Admin (built-in): http://127.0.0.1:8000/admin/

---

## Where Each Requirement Is Implemented
- Two user types (Admin, Player):
  - `game/views.py:is_admin`, navbar uses `user.is_staff`
- Registration and login with custom validation:
  - `game/forms.py:CustomUserCreationForm`, templates under `templates/registration/`
- Initial 20 words in DB:
  - `game/management/commands/populate_words.py`
- Random word and daily limit (3 per user):
  - `game/models.py:Word.get_random_word`, `Game.can_user_play_today()`; `game/views.py:start_game`
- 5 guesses per game, uppercase input, show previous guesses:
  - `game/forms.py:GuessForm`, `templates/game/play.html`, `static/js/app.js`
- Feedback colors and logic:
  - `game/models.py:Guess.generate_feedback()`; styles in `templates/base.html`
- Win/Lose flow with messages and stop:
  - `game/views.py:play_game`, `game/views.py:game_result`, `templates/game/result.html`
- Save chosen words and guesses with dates:
  - `game/models.py:Game`, `game/models.py:Guess`
- Admin reports (daily, per-user):
  - `game/forms.py:AdminReportForm`, `game/views.py:admin_reports`, `templates/game/admin_reports.html`

---

## Testing Suggestions
- Register two users; play games to reach daily limit and verify the restriction
- Try valid/invalid usernames and passwords during registration
- Check guess feedback correctness for duplicates (e.g., target has a repeated letter)
- Verify reports for a specific day and for a specific user

---

## Attribution
This project was created for OpenText internship onboarding tasks (2025). 
