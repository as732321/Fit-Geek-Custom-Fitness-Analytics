import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Fitness Analytics MVP", layout="wide", page_icon="🏋️‍♂️")

st.title("**Nerd Fit:** Generate Custom Fitness Analytics")
st.markdown("""
This app transforms messy, human-readable Excel workout logs into actionable data insights. 
It calculates **Estimated 1-Rep Max (1RM)**, **Total Volume**, and tracks **Progressive Overload**.
""")

# --- ETL ENGINE (Extract, Transform, Load) ---
def process_data(file):
    all_sheets = pd.read_excel(file, sheet_name=None)
    combined_list = []

    for sheet_name, df in all_sheets.items():
        # 1. Clean Column Names
        df.columns = [str(c).strip().capitalize() for c in df.columns]
        
        # 2. Extract Week Number (e.g., "Week 2" -> 2)
        week_match = re.search(r'(\d+)', sheet_name)
        week_num = int(week_match.group(1)) if week_match else 1
        
        # 3. Forward Fill Hierarchy
        if 'Day' in df.columns: df['Day'] = df['Day'].ffill()
        if 'Exercise' in df.columns: df['Exercise'] = df['Exercise'].ffill()

        # 4. Numeric Cleaning & Unit Stripping
        def extract_number(value):
            val_str = str(value).lower().strip()
            if 'bw' in val_str: return 0.0
            match = re.search(r"(\d+\.?\d*)", val_str)
            return float(match.group(1)) if match else np.nan

        if 'Weight' in df.columns: df['Weight'] = df['Weight'].apply(extract_number)
        if 'Reps' in df.columns: df['Reps'] = df['Reps'].apply(extract_number)
        
        # Rename 'Set' to 'Sets' if it exists
        if 'Set' in df.columns:
            df = df.rename(columns={'Set': 'Sets'})
            df['Sets'] = pd.to_numeric(df['Sets'], errors='coerce')

        # 5. Split Day Info & Calculate Cumulative Day
        def split_day_info(day_string):
            day_str = str(day_string)
            muscle_group = re.sub(r'\(Day\s*\d+\)', '', day_str).strip()
            day_match = re.search(r'\(Day\s*(\d+)\)', day_str)
            day_in_week = int(day_match.group(1)) if day_match else 1
            cumulative_day = ((week_num - 1) * 6) + day_in_week
            return muscle_group, cumulative_day

        if 'Day' in df.columns:
            df[['Workout', 'Day_Number']] = df['Day'].apply(lambda x: pd.Series(split_day_info(x)))
            df['Day'] = df['Day_Number']

        # 6. Advanced Metrics: 1RM & Volume
        # Brzycki Formula: Weight / (1.0278 - (0.0278 * Reps))
        df['Est_1RM'] = np.where(df['Reps'] > 1, 
                                 df['Weight'] / (1.0278 - (0.0278 * df['Reps'])), 
                                 df['Weight'])
        df['Volume'] = df['Weight'] * df['Reps']

        # 7. Final Clean up
        df = df.dropna(subset=['Sets', 'Weight', 'Reps'])
        combined_list.append(df)

    return pd.concat(combined_list, ignore_index=True)

# --- APP INTERFACE ---
uploaded_file = st.sidebar.file_uploader("Upload your Workout Log (Excel)", type="xlsx", key="main_loader")

if uploaded_file:
    df = process_data(uploaded_file)
    
    # --- KPI METRICS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sessions", df['Day'].nunique())
    with col2:
        st.metric("Total Volume Lifted", f"{int(df['Volume'].sum()):,} lbs")
    with col3:
        st.metric("Peak Est. 1RM", f"{round(df['Est_1RM'].max(), 1)} lbs")

    # --- VISUALIZATION ---
    st.subheader("Progressive Overload Trends")
    exercise_list = sorted(df['Exercise'].unique())
    selected_ex = st.selectbox("Select Exercise", exercise_list)
    
    chart_df = df[df['Exercise'] == selected_ex].groupby('Day')['Est_1RM'].max().reset_index()
    
    fig = px.line(chart_df, x='Day', y='Est_1RM', 
                  title=f"Estimated 1RM Progression: {selected_ex}",
                  labels={'Est_1RM': '1-Rep Max (lbs)', 'Day': 'Cumulative Day'},
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # --- DATA PREVIEW ---
    with st.expander("View Cleaned Dataset"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("👋 Welcome! Please upload the Excel template to see your fitness insights.")