📚 Study Group Finder

A Django-based web application that helps students create, join, and manage study groups.
It allows members to schedule study sessions, track attendance, and collaborate effectively.

👨‍💻 Team Members

| Name           | Registration No
| -------------- | ---------------- 
| Muhammad Fahad | Sp-23-bse-010    
| Syed Touqeer Abbas | Sp23-bse-056      |



🧠Project Overview

Study Group Finder; simplifies collaboration among students by enabling them to:

* Create and join study groups.
* Schedule and manage group study sessions.
* RSVP for sessions (Attending, Maybe, or Cannot Attend).
* View group and member profiles.
* Access an integrated dashboard and personalized recommendations (optional future features).

🧰 Technology Stack

| Component                   | Technology                                  |
| --------------------------- | ------------------------------------------- |
| **Backend Framework**       | Django 5.2.7 (Python 3.11)                  |
| **Frontend**                | HTML5, CSS3, Bootstrap 5, FontAwesome Icons |
| **Database**                | SQLite3 (default)                           |
| **Template Engine**         | Django Template Language (DTL)              |
| **Styling & Forms**         | Django Crispy Forms + Crispy Bootstrap5     |
| **Version Control**         | Git & GitHub                                |
| **Development Environment** | VS Code                         |

⚙️ Project Setup Instructions

1. Clone the Repository

```bash
git clone https://github.com/yourusername/StudyGroupFinder.git
cd StudyGroupFinder

2. Create and Activate Virtual Environment

Windows:

```bash
python -m venv env
env\Scripts\activate
```

3. Install Required Packages

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, run:

```bash
pip install django==5.2.7 crispy-bootstrap5
pip install django-crispy-forms
```

Then generate it:

```bash
pip freeze > requirements.txt
```

---

🗄️ Database Setup Instructions**

1. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

2. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

3. Load Sample Data (Optional)

If you have a fixtures file:

```bash
python manage.py loaddata sample_data.json
```

---

▶️ Running the Application

Run the Django development server:

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

🔐 Test Login Credentials

| Role      | Username | Password |
| --------- | -------- | -------- |
| Student 1 | muhammad | jamat1234|
| Student 2 | ali      | al34@4567|
| Student 3 | SyedTouqeer445 | Tou123@6789|
| Admin     | muhammad | jamat1234|


✅ List of Completed Features

### 🔹 **Accounts App**

* User registration and login/logout.
* Profile management (view & edit).
* Profile pictures and personal info.

### 🔹 **Groups App**

* Create and manage study groups.
* Join/Leave group functionality.
* View group details and member lists.
* Permissions for group creator vs members.

### 🔹 **User Sessions App**

* Create and manage study sessions.
* RSVP (Attending / Maybe / Cannot Attend).
* Cancel and delete session options.
* Display attendees by category.
* Group session list and detail views.

🔹 Dashboard App

* Personalized dashboard after login.
* Quick navigation to groups and sessions.


⚠️ Known Limitations / Issues

* Notifications system not yet implemented.
* Analytics and gamification features are planned for future releases.
* No email verification during signup.
* Calendar view in progress — currently uses simple list-based scheduling.
* Limited error handling in some forms (minor UI enhancements pending).

---

🧩 Future Enhancements

* 📅 Calendar View for session schedules.
* 🔔 Notification & Reminder System (email or in-app).
* 📊 Analytics Dashboard for group activity insights.
* 🏆 Gamification features (badges, streaks, etc.).
* 🤖 Smart Recommendations using department and semester.
