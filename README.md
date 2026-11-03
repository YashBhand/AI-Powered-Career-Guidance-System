# 🎓 AI-Powered Personalized Career Guidance and Recommendation System

An AI-powered web application that helps students explore suitable career paths based on their education level, favourite subjects, interests, and skills.

## 📌 About the Project

Choosing the right career can be difficult for students. This project provides personalized career recommendations using Machine Learning and Natural Language Processing techniques.

The system accepts student information and recommends the top three matching career options along with relevant courses, qualifications, durations, and required skills.

It supports students from:
- 10th Standard
- 12th Standard
- College Level

## ✨ Features

- Student Registration and Login
- Secure Password Hashing
- Student Dashboard
- Career Assessment Form
- AI-Based Career Recommendations
- Top 3 Career Suggestions
- AI Match Score
- Recommended Courses and Qualifications
- SQLite Database Integration
- User-Friendly Web Interface

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Flask | Web Framework |
| Pandas | Dataset Handling |
| NumPy | Numerical Operations |
| Scikit-learn | Machine Learning |
| TF-IDF | Text Feature Extraction |
| Cosine Similarity | Career Matching |
| SQLite | Database |
| HTML | Web Page Structure |
| CSS | Web Page Styling |
| Bootstrap | Responsive UI |

## 🤖 Machine Learning Algorithm

This project uses:

**1. TF-IDF (Term Frequency-Inverse Document Frequency)**

Converts student information and career descriptions into numerical features.

**2. Cosine Similarity**

Measures the similarity between student preferences and available career information.

The system ranks careers according to their similarity scores and displays the top three recommendations.

*Note: The match score represents text similarity, not the probability of career success or guaranteed admission eligibility.*

## 📂 Project Structure

```text
AI_Career_Guidance/
│
├── app.py
├── requirements.txt
│
├── dataset/
│   ├── careers.csv
│   └── courses.csv
│
├── model/
│   └── train_model.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── assessment.html
│   └── result.html
│
├── static/
│   └── css/
│       └── style.css
│
├── database/
│
└── README.md
```

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YashBhand/AI-Powered-Career-Guidance-System.git
```

### Step 2: Open the Project Folder

```bash
cd AI-Powered-Career-Guidance-System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows CMD:

```bash
venv\Scripts\activate.bat
```

### Step 5: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python app.py
```

### Step 7: Open in Browser

Visit:

```text
http://127.0.0.1:5000/
```

Register an account, log in, and complete the career assessment.

## 📊 How It Works

1. Student registers and logs in.
2. Student selects education level, favourite subject, interest, and skill.
3. The system processes the student's information.
4. TF-IDF converts text into numerical vectors.
5. Cosine Similarity calculates matching scores.
6. The system displays the top three career recommendations.
7. Students can view suggested courses and related information.

## 🚀 Future Enhancements

- Expand the career and course datasets.
- Improve recommendations using more student profiles.
- Add career explanations and eligibility checking.
- Include aptitude and personality assessments.
- Add more career categories.
- Deploy the application online.

## 👨‍💻 Author

**Yash Bhand**

GitHub: [YashBhand](https://github.com/YashBhand)

---

⭐ If you find this project useful, consider giving the repository a star!