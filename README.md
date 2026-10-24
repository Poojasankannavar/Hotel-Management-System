# 🏨 Hotel Management System

A hotel and restaurant management web application built using **Python and Django**. The system combines restaurant operations, hotel room management, guest bookings, billing, inventory, staff management, and business reporting in one application.

<p align="center">
  <a href="https://hotel-management-system-tcl6.onrender.com/">
    <img src="https://img.shields.io/badge/Live%20Demo-Visit%20Application-2EA44F?style=for-the-badge&logo=render&logoColor=white" alt="Live Demo">
  </a>
  <a href="https://github.com/Poojasankannavar/Hotel-Management-System">
    <img src="https://img.shields.io/badge/GitHub-View%20Repository-181717?style=for-the-badge&logo=github" alt="GitHub Repository">
  </a>
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="Database">
</p>

## 🚀 Live Demo

**Try the application:** [Hotel Management System](https://hotel-management-system-tcl6.onrender.com/)

> Note: The link is provided as the live demo URL. Its current availability and functionality have not been independently verified.

## 📌 Project Overview

The Hotel Management System is a Django-based web application designed to manage hotel and restaurant activities through separate administrator, staff, and booking-related interfaces.

It brings restaurant services, room bookings, billing, inventory, employee records, and business reports together in a single system.

## ✨ Features

### 🍽️ Restaurant Management
- Menu and food item management.
- Stock and inventory management.
- Restaurant table management and orders.
- Parcel orders.
- Bill generation, settlement, and printing.
- Pending bill tracking.

### 🏨 Hotel Management
- Room listings and room inventory.
- Guest booking management.
- Room-related records and operations.

### 📊 Business and Financial Management
- Purchase records.
- Expense tracking.
- Staff salary management.
- Sales and profit reports.
- Daily business reports.
- Pending bill records.

### 🔐 User Management
- Separate administrator and staff interfaces.
- Registration and login pages for relevant user roles.
- Booking-related user access.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Backend framework | Django 5.2 |
| Frontend | HTML, Django Templates, CSS, JavaScript |
| Default database | SQLite |
| Deployment database support | Database URL configuration, including PostgreSQL and MySQL drivers |
| Database packages | `psycopg`, `PyMySQL` |
| Production server | Gunicorn |
| Static file serving | WhiteNoise |
| Deployment platform | Render |
| Version control | Git and GitHub |

## 📂 Project Structure

The main Django application is located in `food/food_app`.

```text
Hotel-Management-System/
├── food/
│   ├── food_app/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── templates/
│   │   └── static/
│   ├── manage.py
│   └── ...
├── render.yaml
├── requirements.txt
└── README.md
```

*This is an illustrative structure based on the described project. The exact files and directories may differ in the repository.*

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.x compatible with the project's dependencies.
- pip.
- Git.
- A code editor such as VS Code or PyCharm.

### 1. Clone the Repository

```bash
git clone https://github.com/Poojasankannavar/Hotel-Management-System.git
cd Hotel-Management-System
```

Navigate to the directory containing `manage.py` if it is inside the `food/` folder:

```bash
cd food
```

### 2. Create and Activate a Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

If `requirements.txt` is in the current directory:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the requirements file is in the parent directory, use its relative path instead.

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create an Administrator Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create the account if Django's built-in administration is configured for your project.

## ▶️ Running the Application

Start the local development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## 🚀 Deployment

The project includes Render deployment configuration through `render.yaml`.

Typical deployment steps include:

1. Push the latest project changes to GitHub.
2. Connect the repository to Render.
3. Configure environment variables and the database as required.
4. Install dependencies using the project's requirements file.
5. Run database migrations during deployment.
6. Configure the production start command to use Gunicorn.
7. Configure static file handling with WhiteNoise.
8. Test login, bookings, orders, billing, and reporting after deployment.

**Live application:** [https://hotel-management-system-tcl6.onrender.com](https://hotel-management-system-tcl6.onrender.com)

## 🔮 Future Improvements

- Add online room reservation and booking confirmation.
- Integrate payment gateway support.
- Add email or SMS booking notifications.
- Improve dashboard analytics and visual reports.
- Introduce role-based permissions for administrators and staff.
- Add automated tests for bookings, orders, and billing.
- Improve mobile responsiveness and accessibility.
- Strengthen form validation and application security.

## 👩‍💻 Author

**Pooja Sankannavar**

MCA Student | Full-Stack Developer | Software Development and AI Enthusiast

- **GitHub:** [@Poojasankannavar](https://github.com/Poojasankannavar)
- **LinkedIn:** [Pooja Sankannavar](https://www.linkedin.com/in/pooja-sankannavar-8751a0318/)
- **Repository:** [Hotel Management System](https://github.com/Poojasankannavar/Hotel-Management-System)
- **Live Demo:** [Open Application](https://hotel-management-system-tcl6.onrender.com/)

---

⭐ If you find this project useful, consider giving the repository a star!

*Developed as an academic project to explore full-stack web development, database management, and hotel and restaurant operations using Django.*
