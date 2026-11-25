"""
analysis.py
-----------
ALL the Pandas data analysis lives here (no Streamlit, no charts).
Every function takes a DataFrame and returns a DataFrame / number / dict,
so each one is easy to read, test and explain in your viva.
"""
import pandas as pd

from generate_data import DATA_PATH, SUBJECTS, create_csv

PASS_MARK = 35                                   # minimum marks needed in each subject
GRADE_ORDER = ["A+", "A", "B", "C", "D", "E", "F"]


# ---------------------------------------------------------------- loading
def load_data(path=DATA_PATH):
    """Read the CSV into a DataFrame (creates it first if it does not exist)."""
    if not path.exists():
        create_csv(path)
    return pd.read_csv(path)


# ------------------------------------------------- derived columns (Pandas)
def add_results(df, subjects):
    """Add Total, Average, Grade and Result columns for the chosen subjects."""
    out = df.copy()
    out["Total"] = out[subjects].sum(axis=1)
    out["Average"] = out[subjects].mean(axis=1).round(2)

    # pd.cut sorts each average into a grade "bucket"
    out["Grade"] = pd.cut(
        out["Average"],
        bins=[0, 40, 50, 60, 70, 80, 90, 101],
        labels=["F", "E", "D", "C", "B", "A", "A+"],
        right=False,
    ).astype(str)

    # A student passes only if they score >= PASS_MARK in EVERY chosen subject
    passed = (out[subjects] >= PASS_MARK).all(axis=1)
    out["Result"] = passed.map({True: "Pass", False: "Fail"})
    return out


# ---------------------------------------------------------------- filtering
def apply_filters(df, years, grades, attendance_range):
    """Keep only the rows that match the sidebar filters."""
    low, high = attendance_range
    mask = (
        df["Year"].isin(years)
        & df["Grade"].isin(grades)
        & df["Attendance"].between(low, high)
    )
    return df[mask]


# --------------------------------------------------------------------- KPIs
def calculate_kpis(df):
    """The four headline numbers shown at the top of the dashboard."""
    return {
        "total_students": len(df),
        "avg_marks": float(round(df["Average"].mean(), 1)),
        "avg_attendance": float(round(df["Attendance"].mean(), 1)),
        "pass_percentage": float(round((df["Result"] == "Pass").mean() * 100, 1)),
    }


# ------------------------------------------------------------- subject-wise
def subject_summary(df, subjects):
    """Average / highest / lowest marks and pass % for every subject."""
    summary = pd.DataFrame({
        "Average": df[subjects].mean(),
        "Highest": df[subjects].max(),
        "Lowest": df[subjects].min(),
        "Pass %": (df[subjects] >= PASS_MARK).mean() * 100,
    }).round(1)
    return summary.rename_axis("Subject").reset_index()


# -------------------------------------------------------------- top students
def top_students(df, n=10):
    """Top n students by average marks (attendance breaks ties)."""
    top = df.sort_values(["Average", "Attendance"], ascending=False).head(n)
    top = top[["Student_ID", "Name", "Year", "Total", "Average", "Grade", "Attendance"]]
    top = top.reset_index(drop=True)
    top.insert(0, "Rank", top.index + 1)
    return top


# -------------------------------------------------------------------- grades
def grade_distribution(df):
    """Number of students in each grade (grades with 0 students are kept)."""
    counts = df["Grade"].value_counts().reindex(GRADE_ORDER, fill_value=0)
    return counts.rename_axis("Grade").reset_index(name="Students")


# --------------------------------------------------------------- attendance
def attendance_band_summary(df):
    """Average marks for each attendance band (e.g. 60-70%)."""
    bands = pd.cut(
        df["Attendance"],
        bins=[0, 60, 70, 80, 90, 101],
        labels=["Below 60", "60-70", "70-80", "80-90", "90-100"],
        right=False,
    )
    out = df.groupby(bands, observed=True).agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average", "mean"),
    ).round(1)
    return out.rename_axis("Attendance Band").reset_index()


def attendance_correlation(df):
    """Correlation (-1 to +1) between attendance and average marks."""
    if len(df) < 3:
        return float("nan")
    return round(df["Attendance"].corr(df["Average"]), 2)


def describe_correlation(r):
    """Turn the correlation number into a plain-English sentence."""
    if pd.isna(r):
        return "Not enough data to measure the link between attendance and marks."
    strength = "strong" if abs(r) >= 0.6 else "moderate" if abs(r) >= 0.3 else "weak"
    direction = "positive" if r >= 0 else "negative"
    return f"Attendance and marks have a {strength} {direction} relationship (r = {r})."
