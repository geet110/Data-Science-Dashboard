"""
app.py  -  Student Performance & Academic Analytics Dashboard
-------------------------------------------------------------
This file only builds the web page (Streamlit).
 - analysis.py  -> Pandas calculations
 - charts.py    -> Matplotlib / Seaborn charts
Run with:  streamlit run app.py
"""
import matplotlib.pyplot as plt
import streamlit as st

import analysis as an
import charts as ch
from generate_data import SUBJECTS

# ------------------------------------------------------------ page setup
st.set_page_config(page_title="Student Performance Dashboard", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1250px;}
.hero {background: linear-gradient(120deg, #4F46E5 0%, #7C3AED 55%, #06B6D4 100%);
       padding: 26px 32px; border-radius: 18px; color: white; margin-bottom: 22px;
       box-shadow: 0 10px 25px rgba(79,70,229,.25);}
.hero h1 {margin: 0; font-size: 2rem; color: white;}
.hero p {margin: 6px 0 0 0; opacity: .9; font-size: 1rem;}
.kpi {background: white; border-radius: 16px; padding: 18px 20px;
      box-shadow: 0 2px 12px rgba(15,23,42,.07); border-left: 6px solid var(--c);}
.kpi .label {color: #64748B; font-size: .85rem; font-weight: 600; text-transform: uppercase; letter-spacing: .04em;}
.kpi .value {color: #0F172A; font-size: 2rem; font-weight: 800; line-height: 1.3;}
.insight {background: #EEF2FF; border-radius: 12px; padding: 14px 20px; margin: 18px 0 6px 0; color: #1E293B;}
h3 {color: #1E293B;}
</style>
""", unsafe_allow_html=True)


def show(fig):
    """Display a Matplotlib figure, then free its memory."""
    st.pyplot(fig)
    plt.close(fig)


def kpi_card(label, value, color):
    return f'<div class="kpi" style="--c:{color}"><div class="label">{label}</div><div class="value">{value}</div></div>'


# ------------------------------------------------------------- load data
@st.cache_data
def get_data():
    return an.load_data()


raw = get_data()

# --------------------------------------------------------------- sidebar
st.sidebar.title("🎛️ Filters")

subjects = st.sidebar.multiselect("📚 Subjects", SUBJECTS, default=SUBJECTS,
                                  help="Marks, grades and pass/fail are calculated using only these subjects.")
years = st.sidebar.multiselect("🏫 Year", sorted(raw["Year"].unique()),
                               default=sorted(raw["Year"].unique()))
grades = st.sidebar.multiselect("🎓 Grade", an.GRADE_ORDER, default=an.GRADE_ORDER)
att_low = int(raw["Attendance"].min())
attendance_range = st.sidebar.slider("🗓️ Attendance (%)", att_low, 100, (att_low, 100))

st.sidebar.markdown("---")
st.sidebar.caption(f"Pass rule: at least {an.PASS_MARK} marks in every selected subject.")

# ------------------------------------------------------------ the header
st.markdown("""
<div class="hero">
  <h1>🎓 Student Performance & Academic Analytics</h1>
  <p>BCA Department · Interactive dashboard built with Python, Pandas, Streamlit, Matplotlib & Seaborn</p>
</div>
""", unsafe_allow_html=True)

if not subjects:
    st.warning("Please select at least one subject in the sidebar.")
    st.stop()

# ---------------------------------------------- run the Pandas analysis
with_results = an.add_results(raw, subjects)
df = an.apply_filters(with_results, years, grades, attendance_range)

if df.empty:
    st.warning("No students match the current filters. Please widen your selection.")
    st.stop()

kpi = an.calculate_kpis(df)
summary = an.subject_summary(df, subjects)
grade_counts = an.grade_distribution(df)
top10 = an.top_students(df, 10)
bands = an.attendance_band_summary(df)
r = an.attendance_correlation(df)

# ------------------------------------------------------------- KPI cards
c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi_card("Total Students", f"{kpi['total_students']}", "#4F46E5"), unsafe_allow_html=True)
c2.markdown(kpi_card("Average Marks", f"{kpi['avg_marks']}", "#06B6D4"), unsafe_allow_html=True)
c3.markdown(kpi_card("Average Attendance", f"{kpi['avg_attendance']}%", "#F59E0B"), unsafe_allow_html=True)
c4.markdown(kpi_card("Pass Percentage", f"{kpi['pass_percentage']}%", "#10B981"), unsafe_allow_html=True)

# ---------------------------------------------------------- key insights
best = summary.loc[summary["Average"].idxmax()]
weak = summary.loc[summary["Average"].idxmin()]
st.markdown(
    f'<div class="insight">💡 <b>Key insights:</b> '
    f'Strongest subject is <b>{best["Subject"]}</b> ({best["Average"]} avg), '
    f'weakest is <b>{weak["Subject"]}</b> ({weak["Average"]} avg). '
    f'Top performer: <b>{top10.loc[0, "Name"]}</b> ({top10.loc[0, "Average"]}). '
    f'{an.describe_correlation(r)}</div>',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📚 Subjects", "🏆 Top 10", "🎓 Grades", "📈 Attendance", "🗂️ Data"])

with tab1:
    st.subheader("Subject-wise Performance")
    a, b = st.columns(2)
    with a:
        show(ch.subject_average_chart(summary))
    with b:
        show(ch.subject_boxplot(df, subjects))
    a, b = st.columns([1, 1])
    with a:
        show(ch.subject_heatmap(df, subjects))
    with b:
        st.markdown("##### Subject summary table")
        st.dataframe(summary, hide_index=True)

with tab2:
    st.subheader("Top 10 Students")
    a, b = st.columns([1, 1])
    with a:
        st.dataframe(top10, hide_index=True)
    with b:
        show(ch.top_students_chart(top10))

with tab3:
    st.subheader("Grade Distribution")
    a, b = st.columns([3, 2])
    with a:
        show(ch.grade_bar_chart(grade_counts))
    with b:
        show(ch.grade_donut_chart(grade_counts))
    st.caption("Grades from average marks: A+ ≥ 90, A ≥ 80, B ≥ 70, C ≥ 60, D ≥ 50, E ≥ 40, F < 40.")

with tab4:
    st.subheader("Attendance vs Academic Performance")
    st.info(an.describe_correlation(r))
    a, b = st.columns(2)
    with a:
        show(ch.attendance_scatter(df))
    with b:
        show(ch.attendance_band_chart(bands))
    st.dataframe(bands, hide_index=True)

with tab5:
    st.subheader("Filtered Student Data")
    st.caption(f"Showing {len(df)} of {len(raw)} students")
    show_cols = ["Student_ID", "Name", "Gender", "Year", "Attendance"] + subjects + \
                ["Total", "Average", "Grade", "Result"]
    st.dataframe(df[show_cols], hide_index=True)
    st.download_button("⬇️ Download filtered data as CSV",
                       df[show_cols].to_csv(index=False).encode("utf-8"),
                       file_name="filtered_students.csv", mime="text/csv")

st.markdown("---")
st.caption("Student Performance & Academic Analytics Dashboard · BCA Data Science Practical Project")
