# 🎓 Student Performance & Academic Analytics Dashboard

BCA Data Science practical project built with **Python, Pandas, Streamlit, Matplotlib and Seaborn**.

## Project structure

```
student_dashboard/
├── app.py            <- the dashboard page (Streamlit)  <- you RUN this
├── analysis.py       <- ALL Pandas analysis (KPIs, grades, top 10, attendance)
├── charts.py         <- Matplotlib + Seaborn charts
├── generate_data.py  <- creates the sample dataset of 300 students
├── requirements.txt  <- libraries to install
├── .streamlit/config.toml   <- light colour theme
└── data/students.csv        <- sample data (auto-created if missing)
```

## How to run on your laptop

### Step 1 - Install Python
Download Python 3.10 or newer from https://www.python.org/downloads/
**Windows:** tick **"Add Python to PATH"** during installation.
Check it worked: open a terminal and type `python --version`
(on Mac/Linux use `python3`).

### Step 2 - Open a terminal inside the project folder
- **Windows:** open the `student_dashboard` folder, click the address bar, type `cmd`, press Enter.
- **Mac/Linux:** open Terminal and run `cd path/to/student_dashboard`.

### Step 3 - (Recommended) create a virtual environment
Windows:
```
python -m venv venv
venv\Scripts\activate
```
Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### Step 4 - Install the libraries
```
pip install -r requirements.txt
```

### Step 5 - (Optional) generate the dataset
```
python generate_data.py
```
This creates `data/students.csv`. The dashboard does this automatically if the file is missing.

### Step 6 - Start the dashboard
```
streamlit run app.py
```
Your browser opens at **http://localhost:8501**. Press `Ctrl + C` in the terminal to stop it.

## Using the dashboard
Use the **sidebar filters** (Subjects, Year, Grade, Attendance). Everything - KPI cards,
charts and tables - updates instantly. Marks, grades and pass/fail are recalculated
using only the subjects you select. Explore the tabs: Subjects, Top 10, Grades,
Attendance, Data (with CSV download).

## Rules used in the analysis
| Item | Rule |
|---|---|
| Average | Mean of selected subject marks |
| Grade | A+ ≥ 90, A ≥ 80, B ≥ 70, C ≥ 60, D ≥ 50, E ≥ 40, F < 40 |
| Pass | At least 35 marks in **every** selected subject |
| Pass % | Passed students ÷ total students × 100 |

## Pandas concepts used (good for viva)
`read_csv`, `sum/mean(axis=1)`, `pd.cut` (grades & attendance bands), boolean filtering
with `isin` and `between`, `value_counts`, `reindex`, `groupby().agg()`, `melt`,
`sort_values`, `corr`, `DataFrame` creation, `reset_index`.

## Common problems
| Problem | Fix |
|---|---|
| `'streamlit' is not recognized` | Run `pip install -r requirements.txt`, or use `python -m streamlit run app.py` |
| `pip` not found | Use `python -m pip install -r requirements.txt` |
| Port already in use | `streamlit run app.py --server.port 8502` |
| Want different data | Edit `generate_data.py`, delete `data/students.csv`, run it again |
| Want to use your own CSV | Keep the same column names as `data/students.csv` |

## Note
The data is **synthetic** (generated with NumPy using a fixed seed, so you always get the same students).
Mention this in your report.
