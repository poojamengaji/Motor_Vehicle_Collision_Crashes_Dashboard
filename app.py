import streamlit as st
from utils import *

# Load data
df = load_data()
st.session_state.clear()
create_dashboard_screen()
menu = st.session_state.menu

if menu == "DASHBOARD":
    st.subheader("📊 DASHBOARD OVERVIEW")
    create_dashboard_tab(df)

elif menu == "KPI":
    st.subheader("📈 KEY PERFORMANCE INDICATORS")
elif menu == "TIME":
    st.subheader("TIME ANALYSIS")
elif menu == "LOCATION":
    st.subheader("LOCATION ANALYSIS")
elif menu == "CONTRIBUTING FACTORS":
    st.subheader("CONTRIBUTING FACTORS")
    create_contributing_factors_tab(df)
elif menu == "INJURIES":
    st.subheader("INJURIES")
    create_injuries_tab()
elif menu == "PREDICTIONS":
    st.subheader("PREDICTIONS")
    create_predictions_tab()