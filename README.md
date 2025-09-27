# 🎮 Guess the Word – Django Web App

A full-stack **Wordle-style 5-letter word guessing game** built with Python Django.  
Includes player registration/login, daily play limits, guess feedback (green/orange/grey), history, and admin dashboards/reports.

---

## 👩‍💻 Author
- **Name:** SINDHU T  
- **University:** REVA UNIVERSITY  
- **Role:** Intern @ OpenText (Onboarding 2025)  

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

1️⃣ Create a virtual environment and install dependencies  
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

2️⃣ Apply database migrations and create an admin user

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


3️⃣ Load initial 20 words

python manage.py populate_words


4️⃣ Run development server

python manage.py runserver


Open 👉 http://127.0.0.1:8000/


## Screenshots

![1](https://github.com/user-attachments/assets/a55014f3-c5b8-4b2a-b799-7f29c8eed9b1)

![2](https://github.com/user-attachments/assets/5f216b0f-4571-4932-9267-ac5915238de4)

![3](https://github.com/user-attachments/assets/5aab6ce8-f898-4f89-b307-cf03d3f6d191)

![4](https://github.com/user-attachments/assets/396ae961-848b-451c-ac73-7d7381f7efc0)

![5](https://github.com/user-attachments/assets/0edcb523-5e0c-4c40-8cf3-55d392f86a11)

![6](https://github.com/user-attachments/assets/0f1dc086-1cf5-4825-abb4-887b2307323e)

![7](https://github.com/user-attachments/assets/e5339861-0865-484d-9ce0-1329df54c665)

![8](https://github.com/user-attachments/assets/55c1416d-9a66-44b3-a48e-0ccaed50b904)

![9](https://github.com/user-attachments/assets/0b78a0cd-9c1a-4c6e-8c2a-95c042601057)

![10](https://github.com/user-attachments/assets/f3707174-fc3f-45fe-bcd3-e96dca3e56bd)

![11](https://github.com/user-attachments/assets/91faecae-86e9-4553-8e0c-63f5b834da60)

![12](https://github.com/user-attachments/assets/f4a8ecf4-12e6-4437-830e-13cc556074f6)

![13](https://github.com/user-attachments/assets/fbb42557-8751-47db-be5e-d4899f583627)

![14](https://github.com/user-attachments/assets/89b0765e-c7a2-47e1-bbc1-e9d3f6749cd4)

## 🎮 Features

✅ Two user types (Admin, Player)

✅ Custom registration & login validation

✅ Daily play limit: 3 games per user

✅ 5 guesses per game, uppercase validation

✅ Per-letter feedback (green/orange/grey)

✅ Win/Lose flow with result messages

✅ Guess history and outcomes stored

✅ Admin reports (daily and per-user)

✅ Manage words (activate/deactivate)

## 📜 Attribution

This project was created for OpenText internship onboarding tasks (2025).










