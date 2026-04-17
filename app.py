import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
from utils import load_data

# Load data
df = load_data()

# ---------- Page Config ----------
st.set_page_config(
    page_title="Motor Vehicle Collision Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ---------- Sidebar Menu ----------
if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"

menu_selection = st.sidebar.radio(
    "Select Menu",
    ["Dashboard", "KPI", "Time","Location","Contributing Factors","Injuries","Predictions"]
)
st.session_state.menu = menu_selection

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .title-text {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Create two columns: logo and title
col1, col2 = st.columns([1, 6])  # adjust ratio to make logo smaller
with col1:
    st.image("data/car-crash-icon.png", width=120)  # Logo size

with col2:
    st.markdown("""
        <div style="
            font-size: 2.5rem; 
            font-weight: bold; 
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            margin-top: 10px;
        ">
            Motor Vehicle Collision & Crashes
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 Dashboard Overview")


# ---------- Top Metrics ----------
col1, col2, col3 = st.columns(3)

with col1:
    # Handle empty or missing dates
   # if pd.notnull(df['CRASH DATE']).any():
        start_date_year = df['YEAR'].min()
        end_date_year = df['YEAR'].max()
        period_years = end_date_year - start_date_year + 1
        st.metric(
            "📊 Data Period",
            f"{start_date_year} - {end_date_year}",
            f"{period_years} Years"
        )
    # else:
    #     st.metric("⏱️ Data Period", "N/A", "No valid dates")

with col2:
    st.metric("📍 Coverage Area", f"{df['BOROUGH'].nunique()} Boroughs", "NYC Wide")

with col3:
    st.metric("📈 Dataset Size", f"{len(df):,}", "Records")

col1, col2, col3 = st.columns(3)
col1.metric("Total Crashes", f"{len(df):,}")
col2.metric("Total Injuries", f"{int(df['NUMBER OF PERSONS INJURED'].sum()):,}")
col3.metric("Total Deaths", f"{int(df['NUMBER OF PERSONS KILLED'].sum()):,}")

# ---------- Menu Content ----------
menu = st.session_state.menu

if menu == "Dashboard":
    st.markdown("---")
    crashes_by_date = df.groupby('CRASH DATE').size()   # need to verify
    tab1, tab2 = st.tabs(["Crashes Over Time", "Injuries & Deaths Over Time"])
    with tab1:     # need to verify
        st.line_chart(crashes_by_date)
    with tab2:              # need to verify
        st.subheader("Correlation Heatmap")
        corr = df[['NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED']].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, ax=ax)                
        st.pyplot(fig)

elif menu == "KPI":
    st.subheader("📈 Key Performance Indicators")
    # Add KPI charts or metrics here
    st.write("KPI metrics will go here.")

elif menu == "Time":
    st.subheader("Time Analysis")
    # Add time series analysis here
    st.write("Time-based charts and analysis will go here.")
elif menu == "Location":
    st.subheader("Location Analysis")
    # Add time series analysis here
    st.write("Location-based charts and analysis will go here.")
elif menu == "Contributing Factors":
    st.subheader("Contributing Factors")
    # Add time series analysis here
    st.write("Contributing Factors charts and analysis will go here.")
elif menu == "Injuries":
    st.subheader("Injuries")
    # Add time series analysis here
    st.write("Injuries analysis charts and analysis will go here.")
elif menu == "Predictions":
    st.subheader("Predictions")
    # Add time series analysis here
    st.write("Time-based charts and analysis will go here.")
    