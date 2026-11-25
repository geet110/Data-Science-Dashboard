"""
generate_data.py
----------------
Creates a realistic sample dataset of 300 BCA students and saves it
as  data/students.csv

Run it with:   python generate_data.py
(The dashboard also runs this automatically if the CSV is missing.)
"""
from pathlib import Path

import numpy as np
import pandas as pd

SUBJECTS = ["Python", "Data Structures", "DBMS", "Mathematics", "Statistics", "Web Tech"]

# Some subjects are naturally a little harder / easier than others
SUBJECT_DIFFICULTY = {
    "Python": 0, "Data Structures": -4, "DBMS": 2,
    "Mathematics": -6, "Statistics": -3, "Web Tech": 4,
}

MALE_NAMES = ["Aarav", "Rohan", "Vikram", "Arjun", "Karan", "Rahul", "Aditya", "Manish",
              "Sachin", "Deepak", "Nikhil", "Yash", "Harsh", "Ankit", "Pranav", "Mohit",
              "Sahil", "Gaurav", "Tarun", "Vivek"]
FEMALE_NAMES = ["Ananya", "Priya", "Sneha", "Kavya", "Neha", "Pooja", "Riya", "Isha",
                "Simran", "Divya", "Meera", "Aditi", "Shruti", "Kritika", "Nisha",
                "Tanvi", "Anjali", "Muskan", "Komal", "Sakshi"]
LAST_NAMES = ["Sharma", "Verma", "Gupta", "Yadav", "Singh", "Meena", "Jain", "Agarwal",
              "Chauhan", "Rathore", "Saini", "Joshi", "Mishra", "Khandelwal", "Bansal",
              "Choudhary", "Pareek", "Goyal", "Mathur", "Tiwari"]

DATA_PATH = Path(__file__).parent / "data" / "students.csv"


def generate_students(n=300, seed=42):
    """Return a DataFrame with n students. The seed makes results repeatable."""
    rng = np.random.default_rng(seed)

    # --- unique names -------------------------------------------------
    names, used = [], set()
    while len(names) < n:
        gender = rng.choice(["Male", "Female"])
        first = rng.choice(MALE_NAMES if gender == "Male" else FEMALE_NAMES)
        full = f"{first} {rng.choice(LAST_NAMES)}"
        if full not in used:
            used.add(full)
            names.append((full, gender))

    df = pd.DataFrame({
        "Student_ID": [f"BCA{1001 + i}" for i in range(n)],
        "Name": [x[0] for x in names],
        "Gender": [x[1] for x in names],
        "Year": rng.choice(["Year 1", "Year 2", "Year 3"], size=n),
    })

    # --- attendance (%) ----------------------------------------------
    attendance = np.clip(rng.normal(78, 12, n), 40, 100).round(1)
    df["Attendance"] = attendance

    # --- marks: depend on student ability AND attendance -------------
    ability = rng.normal(0, 1, n)                       # natural ability
    strength = 0.85 * ability + 0.55 * (attendance - 78) / 12
    for subject in SUBJECTS:
        marks = 66 + SUBJECT_DIFFICULTY[subject] + 12 * strength + rng.normal(0, 9, n)
        df[subject] = np.clip(marks, 10, 100).round(0).astype(int)

    return df


def create_csv(path=DATA_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_students()
    df.to_csv(path, index=False)
    return df


if __name__ == "__main__":
    data = create_csv()
    print(f"Created {DATA_PATH} with {len(data)} students.\n")
    print(data.head())
