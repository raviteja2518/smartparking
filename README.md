🚗 Smart Parking Allocation System
A web-based Parking Management System built with **Flask** + **SQLite** that allows controlled parking spot allocation, billing based on duration, and admin analytics.
📌 Features
- ✅ Login system for **authorized staff**
- 🚘 Allocate parking spot with **vehicle and user details**
- 🕒 Automatic billing based on time duration
  - First 30 minutes – Free
  - ₹2 for every 10 minutes after
- 💳 Bill generation on vehicle exit
- 📊 Admin dashboard to view **daily earnings**
- 🎨 Attractive UI using **Bootstrap**, **Animate.css**, and **Google Fonts*
## 🖥️ Tech Stack
- **Backend:** Python, Flask, SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap 5, Animate.css
- **Authentication:** Basic username-password login (for limited users)
## 📷 Screenshots
https://github.com/user-attachments/assets/dd86a69d-07d7-4e5e-a6c4-605ef52b6c92
https://github.com/user-attachments/assets/5982986e-3aa8-4c68-9089-4c64700724e4
https://github.com/user-attachments/assets/5cd5eaa7-1c4b-498e-9b8f-0df80bc10bfa

## 🛠️ Setup Instructions

1. Clone the repo:-
   git clone https://github.com/raviteja2518/smartparking.git
   cd smartparking


2. Create virtual environment & activate:-
   python -m venv venv
   venv\\Scripts\\activate


3. Install dependencies:-
   pip install -r requirements.txt


4. Delete old DB if exists:-
   del parking.db


5.Run the app:-
   flask run


Visit: http://127.0.0.1:5000


🔐 Login Credentials:-
Username: admin
Password: 123


You can change them in app.py or insert more users in User table.
🤝 Contributing



Let’s connect and collaborate! Feel free to reach out for tech discussions, project collaborations!
Linkedin:-https://www.linkedin.com/in/gangaravitejareddy-yaramareddy-33b538277/

