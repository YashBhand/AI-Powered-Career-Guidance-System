
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------
# 1. Load datasets
# --------------------------------

df = pd.read_csv("dataset/careers.csv")
courses_df = pd.read_csv("dataset/courses.csv")

# Remove extra spaces from career names
df["career"] = df["career"].astype(str).str.strip()
courses_df["career"] = courses_df["career"].astype(str).str.strip()

# Keep one course per career
courses_df = courses_df.drop_duplicates(
    subset="career",
    keep="first"
)


# --------------------------------
# 2. Career recommendation function
# --------------------------------

def recommend_careers(education, subject, interest, skill):

    # Filter careers according to education level
    eligible_careers = df[
        df["education"].astype(str).str.strip().str.lower()
        == education.strip().lower()
    ].copy()

    # Check whether careers are available
    if eligible_careers.empty:
        return pd.DataFrame()

    # Prepare student information
    student_data = (
        education + " " +
        subject + " " +
        interest + " " +
        skill
    )

    # Prepare career information
    career_data = (
        eligible_careers["education"].astype(str) + " " +
        eligible_careers["subject"].astype(str) + " " +
        eligible_careers["interest"].astype(str) + " " +
        eligible_careers["skill"].astype(str) + " " +
        eligible_careers["description"].astype(str)
    )

    # --------------------------------
    # 3. Convert text into numbers
    # --------------------------------

    vectorizer = TfidfVectorizer()

    career_vectors = vectorizer.fit_transform(career_data)

    student_vector = vectorizer.transform([student_data])

    # --------------------------------
    # 4. Calculate similarity
    # --------------------------------

    similarity = cosine_similarity(
        student_vector,
        career_vectors
    )

    # Add similarity score
    eligible_careers["score"] = similarity[0]

    # --------------------------------
    # 5. Select top 3 careers
    # --------------------------------

    recommendations = eligible_careers.sort_values(
        by="score",
        ascending=False
    ).head(3).copy()

    # --------------------------------
    # 6. Add course information
    # --------------------------------

    recommendations = recommendations.merge(
        courses_df,
        on="career",
        how="left"
    )

    # Fill missing course details
    recommendations = recommendations.fillna({
        "course_name": "Course information not added yet",
        "qualification": "Not available",
        "duration": "Not available",
        "skills": "Not available"
    })

    # Return final output
    return recommendations[
        [
            "career",
            "description",
            "score",
            "course_name",
            "qualification",
            "duration",
            "skills"
        ]
    ]


# --------------------------------
# 7. Display recommendations
# --------------------------------

def display_recommendations(education, subject, interest, skill):

    result = recommend_careers(
        education,
        subject,
        interest,
        skill
    )

    print("\n===== AI CAREER RECOMMENDATIONS =====")
    print("Education:", education)
    print("Subject:", subject)
    print("Interest:", interest)
    print("Skill:", skill)

    if result.empty:

        print("\nNo matching careers found.")

    else:

        for rank, (_, career) in enumerate(
            result.iterrows(), start=1
        ):

            print("\nRank:", rank)
            print("Career:", career["career"])
            print("Description:", career["description"])

            print(
                "Similarity Score:",
                round(career["score"] * 100, 1), "%"
            )

            print("Recommended Course:", career["course_name"])
            print("Qualification:", career["qualification"])
            print("Duration:", career["duration"])
            print("Required Skills:", career["skills"])

    print("\n====================================")


# --------------------------------
# 8. Test all education levels
# --------------------------------

if __name__ == "__main__":

    print("\n========== 10TH STUDENT ==========")

    display_recommendations(
        "10th",
        "Science",
        "Technology",
        "Problem Solving"
    )

    print("\n========== 12TH STUDENT ==========")

    display_recommendations(
        "12th",
        "Mathematics",
        "Technology",
        "Problem Solving"
    )

    print("\n========== COLLEGE STUDENT ==========")

    display_recommendations(
        "College",
        "Mathematics",
        "Technology",
        "Problem Solving"
    )
