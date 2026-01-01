# 🏋️‍♂️ Fit Geek 1.0 

**Turn messy Excel workout logs into actionable strength training insights.**

Fit Geek is a Python-based data pipeline and dashboard that solves a common problem for lifters: **Data Fragmentation**. It takes human-readable (hierarchical) Excel logs, cleans and normalizes the data, and visualizes progress over time using the Brzycki 1-Rep Max formula.

---

## 🚀 Features

* **Automated ETL Pipeline**: Ingests multi-sheet Excel files (one sheet per week), handles merged cells, and standardizes column names.
* **Intelligent Data Cleaning**:
    * **Unit Stripping**: Automatically converts text like "135 lbs" or "20kg" into pure floats (`135.0`).
    * **Forward Filling**: Fills gaps in hierarchical logs (e.g., where "Day" or "Exercise" is only written once per block).
    * **Time Normalization**: Converts "Week 2, Day 1" into a continuous `Cumulative_Day` integer for linear time-series plotting.
* **Advanced Metrics**:
    * **Estimated 1RM**: Calculates theoretical max strength using the Brzycki formula.
    * **Volume Load**: Tracks total tonnage lifted per session.
* **Interactive Dashboard**: Powered by **Streamlit** and **Plotly** for dynamic filtering and zooming.

---

## 📋 How to Use the Excel Template

To use this dashboard, you must track your workouts using the provided `Workout_Log_Template.xlsx`.

### 1. Download the Template
[Click here to download the template](Workout_Log_Template.xlsx) (Ensure this file is in your repo).

### 2. Logging Rules
* **One Sheet per Week**: Name your tabs "Week 1", "Week 2", etc.
* **The "Day" Column**: Use the format `Muscle Group (Day X)`.
    * *Example:* `Chest + Back (Day 1)`
* **The "Weight" Column**: You can type units! The app handles them automatically.
    * *Valid entries:* `135`, `135 lbs`, `60 kg`, `bw` (Bodyweight).
* **Structure**: You don't need to repeat the Day or Exercise name for every set. The app will "Forward Fill" the data for you.

**Example Input:**
| Day | Exercise | Set | Reps | Weight |
| :--- | :--- | :--- | :--- | :--- |
| Chest (Day 1) | Bench Press | 1 | 10 | 135 lbs |
| | | 2 | 8 | 145 lbs |
| | | 3 | 5 | 155 lbs |

---

## 🛠️ Installation & Setup

Prerequisites: Python 3.8+

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/fitness-analytics-pro.git](https://github.com/YOUR_USERNAME/fitness-analytics-pro.git)
    cd fitness-analytics-pro
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```

4.  **Upload Data**
    * The app will open in your browser at `http://localhost:8501`.
    * Drag and drop your filled-out `Workout_Log_Template.xlsx` into the sidebar.

---

## 💻 Tech Stack

* **Core Logic**: Python
* **Data Manipulation**: Pandas, NumPy (Vectorized operations)
* **Interface**: Streamlit
* **Visualization**: Plotly Express
* **File Handling**: OpenPyXL, Regex (String parsing)

---

## 🔮 Future Roadmap

* **Apple Health Integration**: Syncing heart rate data from Apple Watch XML exports (`export.xml`).
* **Machine Learning**: Implementing a classifier to detect "High Exertion" sets by correlating Heart Rate Peaks with Work Sets.
* **Exertion Scoring**: Calculating TRIMP (Training Impulse) scores based on HR recovery curves.

---

*Created by Avery Stanford - linkedin.com/in/avery-stanford*
