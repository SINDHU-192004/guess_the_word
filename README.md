# 🎮 **GUESS THE WORD** 

## 📌 **Project Overview**

**Guess the Word** is a **Django-based Wordle-style web application** developed as part of the **OpenText internship onboarding assignment**.  
The project implements both **Player** and **Admin** user roles, enforces **custom registration/login rules**, and provides a fun **5-letter guessing game** with feedback highlighting (**green/orange/grey**). Each **player** can play up to **3 games per day**, with **5 guesses per game**, while **admins** can configure words and generate detailed reports (**daily and user-wise**). 

The system ensures:
- **Secure registration** (username rules + strong password policy)  
- **Pre-loaded database** with **20 five-letter uppercase words**  
- **Random word selection** for each game session  
- **Interactive gameplay** with instant feedback on guesses  
- **Storage of all attempts and results** in the database  
- **Admin dashboards** with **reports on usage and success rates**  

This makes it both an **engaging game for players** and a **data-driven tool for admins**.

---

## 📸 **Screenshots**

### **Dashboard**
![1](https://github.com/user-attachments/assets/0b542083-cc52-4719-af31-49b0855ed7e7)

### **Login Page**
![2](https://github.com/user-attachments/assets/1cce3faa-ebe8-461c-bfb3-fc1580e8f0e2)

### **Registration Page**
![3](https://github.com/user-attachments/assets/17eb7869-1f09-40d7-bc4d-9fa501517f7e)

![4](https://github.com/user-attachments/assets/fb37a484-d223-4571-9d08-11d44cea575d)

### **Play the Game**
![5](https://github.com/user-attachments/assets/017635ab-e11d-4867-bc5f-6c43edf710e2)

### **Guess**
![6](https://github.com/user-attachments/assets/f2acc6ed-fe4a-46cd-8ffa-2712bf96beef)

![7](https://github.com/user-attachments/assets/bda8e12f-bc24-4559-a61d-4d908917044d)

![8](https://github.com/user-attachments/assets/fe3f7aac-d497-4146-9ec5-fd2264c89d59)

### **Game History**
![9](https://github.com/user-attachments/assets/5289f6c6-c455-450f-b78b-97e2dbc20efe)

![10](https://github.com/user-attachments/assets/fd5ed688-7cea-4283-ada3-18d4ae873d1d)

### **Admin**
![11](https://github.com/user-attachments/assets/1d26f0f5-ceca-4b8e-acd5-8ead52bad477)

### **Daily Report**
![12](https://github.com/user-attachments/assets/c3438150-023f-42bf-811e-108e48a0a197)

### **User Report**
![13](https://github.com/user-attachments/assets/0aa0d3e4-fff3-4d26-9696-6d882476c29b)

### **Manage Words**
![14](https://github.com/user-attachments/assets/09f9f621-e813-4e12-be6d-1c4db6408b67)

---

## 🎮 **Features**

✅ **Two user types** (**Admin**, **Player**)  
✅ **Custom registration & login validation**  
✅ **Daily play limit**: **3 games per user**  
✅ **5 guesses per game**, **uppercase validation**  
✅ **Per-letter feedback** (**green/orange/grey**)  
✅ **Win/Lose flow** with **result messages**  
✅ **Guess history** and **outcomes stored**  
✅ **Admin reports** (**daily** and **per-user**)  
✅ **Manage words** (**activate/deactivate**)  
  
---

## 📖 **Project Summary**

This project fulfills the **“Guess the Word” specifications** provided by **OpenText** for **pre-onboarding assignment**.  

The app supports **two user types**:
- **Player users:** play the **guessing game** (**max 3 games/day**, **5 guesses per game**)  
- **Admin users:** **manage words** and **view reports**  

### 🎯 **Gameplay**
At game start, a **random 5-letter uppercase word** is chosen. Each submitted **guess** shows **per-letter feedback**:

🟩 **Green → correct letter in correct position**  
🟧 **Orange → correct letter in wrong position**  
⬛ **Grey → letter not in target word**  

All **words** and **guesses** (with **timestamps**) are **stored in the database**.  
**Admins** can view **day-wise** and **user-wise reports**.

---

## 🛠 **Tech Stack**
- **Python 3.10+**  
- **Django 4.2**  
- **SQLite** (default dev DB)  
- **Bootstrap 5 + Font Awesome**  

---

## 🚀 **How to Run Locally (Windows PowerShell)**

From **project root**: `c:/Users/91636/Desktop/guess_the_word`

### 1️⃣ **Create a virtual environment and install dependencies**
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

---

## 👩‍💻 Author
**SINDHU T**

---

## 📜 Attribution

This project was developed as part of the OpenText Internship Onboarding Program (2025).
It was created to fulfill the onboarding requirement of demonstrating proficiency in Python and Java, as outlined in the training modules provided to interns.









