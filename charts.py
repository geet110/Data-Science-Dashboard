"""
charts.py
---------
All Matplotlib + Seaborn charts. Every function receives data (already
prepared by analysis.py) and returns a Matplotlib figure.
"""
import matplotlib

matplotlib.use("Agg")                      # draw without opening a window
import matplotlib.pyplot as plt
import seaborn as sns

from analysis import GRADE_ORDER, PASS_MARK

PRIMARY, GREEN, RED, AMBER, SLATE = "#4F46E5", "#10B981", "#EF4444", "#F59E0B", "#64748B"
GRADE_COLORS = {"A+": "#10B981", "A": "#34D399", "B": "#06B6D4", "C": "#6366F1",
                "D": "#F59E0B", "E": "#FB923C", "F": "#EF4444"}

sns.set_theme(style="whitegrid", rc={
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 13,
    "axes.labelcolor": "#334155", "grid.color": "#E2E8F0",
    "figure.facecolor": "white", "axes.facecolor": "white",
})


def _label_bars(ax, fmt="%.1f"):
    for container in ax.containers:
        ax.bar_label(container, fmt=fmt, padding=3, fontsize=9, color="#334155")


def message_figure(text):
    """A blank figure with a message (used when there is not enough data)."""
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.text(0.5, 0.5, text, ha="center", va="center", color=SLATE, fontsize=11)
    ax.axis("off")
    return fig


# ---------------------------------------------------------------- subjects
def subject_average_chart(summary):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    sns.barplot(data=summary, x="Subject", y="Average", hue="Subject",
                palette=sns.color_palette("crest", len(summary)), legend=False, ax=ax)
    _label_bars(ax)
    ax.set_ylim(0, 100)
    ax.set_title("Average Marks by Subject")
    ax.set_xlabel("")
    ax.set_ylabel("Average marks")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    return fig


def subject_boxplot(df, subjects):
    long = df.melt(value_vars=subjects, var_name="Subject", value_name="Marks")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    sns.boxplot(data=long, x="Subject", y="Marks", hue="Subject",
                palette=sns.color_palette("crest", len(subjects)), legend=False, ax=ax)
    ax.axhline(PASS_MARK, color=RED, ls="--", lw=1.2, label=f"Pass mark ({PASS_MARK})")
    ax.legend(loc="lower right", frameon=False)
    ax.set_title("Spread of Marks (Box Plot)")
    ax.set_xlabel("")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    return fig


def subject_heatmap(df, subjects):
    if len(subjects) < 2:
        return message_figure("Select at least 2 subjects to see correlations")
    fig, ax = plt.subplots(figsize=(7, 4.6))
    sns.heatmap(df[subjects].corr(), annot=True, fmt=".2f", cmap="Blues",
                linewidths=1, cbar=False, ax=ax)
    ax.set_title("How Subjects Relate to Each Other (Correlation)")
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    return fig


# ------------------------------------------------------------ top students
def top_students_chart(top):
    fig, ax = plt.subplots(figsize=(7, 4.6))
    sns.barplot(data=top, y="Name", x="Average", color=PRIMARY, ax=ax)
    _label_bars(ax)
    low = max(0, top["Average"].min() - 10)
    ax.set_xlim(low, 100)
    ax.set_title("Top 10 Students by Average Marks")
    ax.set_xlabel("Average marks")
    ax.set_ylabel("")
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------ grades
def grade_bar_chart(grades):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    sns.barplot(data=grades, x="Grade", y="Students", hue="Grade",
                palette=GRADE_COLORS, order=GRADE_ORDER, hue_order=GRADE_ORDER,
                legend=False, ax=ax)
    _label_bars(ax, fmt="%d")
    ax.set_title("Grade Distribution")
    ax.set_xlabel("Grade")
    ax.set_ylabel("Number of students")
    fig.tight_layout()
    return fig


def grade_donut_chart(grades):
    data = grades[grades["Students"] > 0]
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    ax.pie(data["Students"], labels=data["Grade"], autopct=lambda p: f"{p:.0f}%" if p >= 5 else "", startangle=90,
           colors=[GRADE_COLORS[g] for g in data["Grade"]], pctdistance=0.8,
           wedgeprops={"width": 0.42, "edgecolor": "white"}, textprops={"fontsize": 9})
    ax.set_title("Grade Share")
    fig.tight_layout()
    return fig


# -------------------------------------------------------------- attendance
def attendance_scatter(df):
    if len(df) < 3 or df["Attendance"].nunique() < 2:
        return message_figure("Not enough students for this chart")
    fig, ax = plt.subplots(figsize=(7, 4.6))
    sns.scatterplot(data=df, x="Attendance", y="Average", hue="Result",
                    hue_order=["Pass", "Fail"], palette={"Pass": GREEN, "Fail": RED},
                    s=45, alpha=0.75, edgecolor="white", ax=ax)
    sns.regplot(data=df, x="Attendance", y="Average", scatter=False,
                color=PRIMARY, line_kws={"lw": 2.2}, ax=ax)
    ax.set_title("Attendance vs Average Marks")
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Average marks")
    ax.legend(title="", frameon=False, loc="lower right")
    fig.tight_layout()
    return fig


def attendance_band_chart(bands):
    fig, ax = plt.subplots(figsize=(7, 4.6))
    sns.barplot(data=bands, x="Attendance Band", y="Avg_Marks", hue="Attendance Band",
                palette=sns.color_palette("flare", len(bands)), dodge=False, legend=False, ax=ax)
    _label_bars(ax)
    ax.set_ylim(0, 100)
    ax.set_title("Average Marks by Attendance Band")
    ax.set_xlabel("Attendance band (%)")
    ax.set_ylabel("Average marks")
    fig.tight_layout()
    return fig
