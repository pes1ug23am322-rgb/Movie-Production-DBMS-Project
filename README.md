 Movie / Theatre Production Management System  
DBMS Mini Project using Flask + MySQL

This is a simple web-based system developed as part of our **3rd Year B.Tech DBMS Mini Project**. It manages different aspects of movie/theatre production including users, productions, crew, casting, budget, awards, and reviews.
 Features
- Add & manage users  
- Add & view productions  
- Crew and casting management  
- Budget tracking (estimated & actual)  
- Awards management  
- User reviews with ratings  
- Reports: Average ratings & Budget variance  

Technologies Used
- Python Flask  
- MySQL  
- SQLAlchemy  
- HTML, Bootstrap  
- Jinja2 Templates  

 How to Run
1. Install dependencies  
   pip install -r requirements.txt

2. Create the database  
   CREATE DATABASE film_db;

3. Update MySQL credentials in config.py if needed

4. Run the Flask app  
   python app.py

5. Open in browser  
   http://127.0.0.1:5000/

Project Structure
film_project_student_mysql/
│
├── app.py
├── models.py
├── config.py
│
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── users.html
│   ├── productions.html
│   ├── crew.html
│   ├── casting.html
│   ├── budget.html
│   ├── awards.html
│   ├── reviews.html
│   └── reports.html
│
├── static/
│   └── css/
│
└── sql/
    └── mysql_schema.sql

 Team Members
SUHAS HARSOOR: Backend Development + Database  
VISHNU MISHRA: Frontend Development + Documentation  

Purpose
To demonstrate DBMS concepts such as tables, primary & foreign keys, relationships, constraints, triggers, stored procedure, stored function, and SQL queries in a real-world themed mini project.


