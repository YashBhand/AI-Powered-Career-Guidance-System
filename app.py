
from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)

import sqlite3
import os

from model.train_model import recommend_careers

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# --------------------------------
# 1. Flask application setup
# --------------------------------

app = Flask(__name__)

app.secret_key = "career_guidance_secret_key"

# Database location
DATABASE = os.path.join("database", "career_guidance.db")


# --------------------------------
# 2. Database connection
# --------------------------------

def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# --------------------------------
# 3. Create database tables
# --------------------------------

def create_database():

    os.makedirs("database", exist_ok=True)

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            education_level TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            education_level TEXT,
            subject TEXT,
            interest TEXT,
            skill TEXT,
            FOREIGN KEY (student_id)
            REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


# --------------------------------
# 4. Homepage
# --------------------------------

@app.route('/')
def home():

    return render_template('index.html')


# --------------------------------
# 5. Student registration
# --------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    message = ""

    if request.method == 'POST':

        name = request.form.get('full_name', '').strip()

        email = request.form.get('email', '').strip().lower()

        education = request.form.get(
            'education_level', ''
        ).strip()

        password = request.form.get('password', '')

        if not name or not email or not education or not password:

            message = "Please fill in all fields."

        elif len(password) < 8:

            message = "Password must contain at least 8 characters."

        elif education not in ["10th", "12th", "College"]:

            message = "Please select a valid education level."

        else:

            conn = get_db_connection()

            try:

                hashed_password = generate_password_hash(password)

                conn.execute("""
                    INSERT INTO students
                    (full_name, email, education_level, password)
                    VALUES (?, ?, ?, ?)
                """, (
                    name,
                    email,
                    education,
                    hashed_password
                ))

                conn.commit()

                conn.close()

                return redirect(url_for('login'))

            except sqlite3.IntegrityError:

                conn.close()

                message = "This email is already registered."

            except sqlite3.Error:

                conn.close()

                message = "Registration failed. Please try again."

    return render_template(
        'register.html',
        message=message
    )


# --------------------------------
# 6. Student login
# --------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    message = ""

    if request.method == 'POST':

        email = request.form.get('email', '').strip().lower()

        password = request.form.get('password', '')

        conn = get_db_connection()

        student = conn.execute(
            "SELECT * FROM students WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if student and check_password_hash(
            student['password'],
            password
        ):

            session.clear()

            session['student_id'] = student['id']

            session['student_name'] = student['full_name']

            return redirect(url_for('dashboard'))

        else:

            message = "Invalid email or password."

    return render_template(
        'login.html',
        message=message
    )


# --------------------------------
# 7. Student dashboard
# --------------------------------

@app.route('/dashboard')
def dashboard():

    if 'student_id' not in session:

        return redirect(url_for('login'))

    return render_template(
        'dashboard.html',
        name=session['student_name']
    )


# --------------------------------
# 8. Career assessment
# --------------------------------

@app.route('/assessment', methods=['GET', 'POST'])
def assessment():

    # Check student login
    if 'student_id' not in session:

        return redirect(url_for('login'))

    if request.method == 'POST':

        # Get student answers
        education = request.form.get(
            'education_level', ''
        ).strip()

        subject = request.form.get(
            'subject', ''
        ).strip()

        interest = request.form.get(
            'interest', ''
        ).strip()

        skill = request.form.get(
            'skill', ''
        ).strip()

        # Validate answers
        if not all([education, subject, interest, skill]):

            return render_template(
                'assessment.html',
                message="Please complete all assessment fields."
            )

        if education not in ["10th", "12th", "College"]:

            return render_template(
                'assessment.html',
                message="Please select a valid education level."
            )

        # Generate career recommendations
        recommendations = recommend_careers(
            education,
            subject,
            interest,
            skill
        )

        # Save assessment answers
        conn = get_db_connection()

        conn.execute("""
            INSERT INTO assessments
            (student_id, education_level, subject, interest, skill)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session['student_id'],
            education,
            subject,
            interest,
            skill
        ))

        conn.commit()
        conn.close()

        # Check recommendations
        if recommendations.empty:

            return render_template(
                'result.html',
                recommendations=[],
                message="No matching careers found. Please try another assessment."
            )

        # Convert recommendations into dictionary
        career_results = recommendations.to_dict(
            orient='records'
        )

        # Display results
        return render_template(
            'result.html',
            recommendations=career_results,
            message=""
        )

    return render_template('assessment.html')


# --------------------------------
# 9. Student logout
# --------------------------------

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))


# --------------------------------
# 10. Run Flask application
# --------------------------------

if __name__ == '__main__':

    create_database()

    app.run(debug=True)
