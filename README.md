# 🎮 Guess the Word – Django Web App

## 📌 Project Overview

**Guess the Word** is a Django-based Wordle-style web application developed as part of the OpenText internship onboarding assignment.  
The project implements both **Player** and **Admin** user roles, enforces custom registration/login rules, and provides a fun 5-letter guessing game with feedback highlighting (green/orange/grey). Each player can play up to **3 games per day**, with **5 guesses per game**, while admins can configure words and generate detailed reports (daily and user-wise). 

The system ensures:
- Secure registration (username rules + strong password policy)  
- Pre-loaded database with 20 five-letter uppercase words  
- Random word selection for each game session  
- Interactive gameplay with instant feedback on guesses  
- Storage of all attempts and results in the database  
- Admin dashboards with reports on usage and success rates  

This makes it both an **engaging game for players** and a **data-driven tool for admins**.

"C:\Users\91636\Desktop\guess_the_word\screenshots\1.jpg"

![2](https://github.com/user-attachments/assets/1cce3faa-ebe8-461c-bfb3-fc1580e8f0e2)


### 🎮 Features

✅ Two user types (Admin, Player)

✅ Custom registration & login validation

✅ Daily play limit: 3 games per user

✅ 5 guesses per game, uppercase validation

✅ Per-letter feedback (green/orange/grey)

✅ Win/Lose flow with result messages

✅ Guess history and outcomes stored

✅ Admin reports (daily and per-user)

✅ Manage words (activate/deactivate)

---

## 📖 Project Summary
This project fulfills the **“Guess the Word”** specifications provided by **OpenText** for pre-onboarding assignment.  

The app supports two user types:
- **Player users:** play the guessing game (max 3 games/day, 5 guesses per game)
- **Admin users:** manage words and view reports

### 🎯 Gameplay
At game start, a random 5-letter uppercase word is chosen. Each submitted guess shows per-letter feedback:
- 🟩 Green → correct letter in correct position  
- 🟧 Orange → correct letter in wrong position  
- ⬛ Grey → letter not in target word  

All words and guesses (with timestamps) are stored in the database. Admins can view **day-wise** and **user-wise reports**.

---

## 🛠 Tech Stack
- Python **3.10+**
- Django **4.2**
- SQLite (default dev DB)
- Bootstrap 5 + Font Awesome

---

## 🚀 How to Run Locally (Windows PowerShell)

From project root: `c:/Users/91636/Desktop/guess_the_word`

### 1️⃣ Create a virtual environment and install dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2️⃣ Apply database migrations and create an admin user
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3️⃣ Load initial 20 words
```powershell
python manage.py populate_words
```

### 4️⃣ Run development server
```powershell
python manage.py runserver
```

Open 👉 [http://127.0.0.1:8000/]


## 👩‍💻 Author
- **Name:** SINDHU T  
- **University:** REVA UNIVERSITY  
- **Role:** Intern @ OpenText (Onboarding 2025)  
---

## 📜 Attribution

This project was created for OpenText internship onboarding tasks (2025).










