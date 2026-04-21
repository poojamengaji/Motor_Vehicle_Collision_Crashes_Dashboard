import pandas as pd
import streamlit as st
import plotly.express as px

# ---------- Data Loading ----------
@st.cache_data
def load_data():
    """Load and cache the dataset to prevent reloading on every interaction"""
    # Adjust path if necessary
    df = pd.read_csv("data/Cleaned_Motor_Vehicle_Collisions_Crashes.csv")
    return df

# ---------- UI & Styling ----------
def apply_custom_css():
    st.markdown("""
        <style>
        .main { padding-top: 1rem; }
        .stMetric {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }
        .insight-box {
            padding: 20px;
            border-left: 5px solid #764ba2;
            background-color: #f9f9f9;
            margin: 10px 0;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

def create_header():
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("data/car-crash-icon.png", width=100)
    with col2:
        st.markdown("""
            <h1 style='background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top:10px;'>
            Motor Vehicle Collision Crashes</h1>
        """, unsafe_allow_html=True)
    st.markdown("---")

def main():
    """Initializes the Page Config, Header, and Sidebar Navigation"""
    st.set_page_config(page_title="NYC Collision Analytics", layout="wide", initial_sidebar_state="expanded")
    apply_custom_css()
    create_header()

    menu_options = ["DASHBOARD", "KPI", "TIME", "LOCATION", "CONTRIBUTING FACTORS", "INJURIES", "PREDICTIONS"]
    
    # THE FIX: Simply use key="menu". 
    # Streamlit will automatically create st.session_state.menu and update it instantly.
    st.sidebar.radio(
        "NAVIGATION MENU",
        menu_options,
        key="menu" 
    )

# ---------- Helper Functions ----------
def render_image_with_insight(path, title, insight):
    """Helper to display images with a spinner and styled text"""
    with st.spinner(f"Loading {title}..."):
        st.subheader(title)
        st.image(path, use_container_width=True)
        st.markdown(f"<div class='insight-box'><b>Insight:</b><br>{insight}</div>", unsafe_allow_html=True)

# ---------- Tab Components ----------
def create_dashboard_tab(df):
    with st.spinner("Loading Overview..."):
        m1, m2, m3 = st.columns(3)
        start, end = df['YEAR'].min(), df['YEAR'].max()
        m1.metric("📊 Data Period", f"{start} - {end}", f"{end-start+1} Years")
        m2.metric("📍 Coverage", f"{df['BOROUGH'].nunique()} Boroughs", "NYC Wide")
        m3.metric("📈 Dataset Size", f"{len(df):,}", "Records")

        t1, t2, t3 = st.columns(3)
        t1.metric("Total Crashes", f"{len(df):,}")
        t2.metric("Total Injuries", f"{int(df['NUMBER OF PERSONS INJURED'].sum()):,}")
        t3.metric("Total Deaths", f"{int(df['NUMBER OF PERSONS KILLED'].sum()):,}")

def create_contributing_factors_tab(df):
    t1, t2, t3, t4 = st.tabs(["TOP FACTORS", "VEHICLE TYPES", "DISTRIBUTION PLOT", "SUMMARIZED DATA"])
    
    with t1:
        render_image_with_insight("plots/TopFactorsByBorough.png", "Top Factors by Borough", 
            "The stacked bar chart illustrating 'Top Factors by Borough' reveals that Brooklyn and Queens are the primary hotspots for traffic incidents among named boroughs, while a significant volume of data is categorized under an 'Unknown' location. Across all regions, 'Driver Inattention/Distraction' (orange) and 'Unspecified' (light blue) consistently emerge as the most frequent contributing factors, mirroring the trends seen in the overall share data. While Staten Island shows the lowest total incident count, the proportional makeup of factors remains relatively stable across the five boroughs, with 'Following Too Closely' and 'Failure to Yield Right-of-Way' maintaining their positions as the most common specific moving violations. Interestingly, the 'Unknown' category displays a disproportionately high amount of specific violations like 'Following Too Closely,' suggesting that more detailed reporting often occurs even when the exact geographic borough is not recorded.")
    
    with t2:
        render_image_with_insight("plots/FactorVehicleTypeHeatMap.png", "Crash Frequency by Factor and Vehicle Type", 
            "Based on the provided heatmap displaying 'Crash Frequency by Factor and Vehicle Type,' standard passenger vehicles are responsible for the overwhelming majority of recorded incidents. The visual data is heavily anchored by intense dark blue 'hotspots' at the intersections of Sedans and Station Wagon/Sport Utility Vehicles with the top contributing factors: 'Driver Inattention/Distraction' and 'Unspecified.' These specific combinations represent the absolute highest crash frequencies in the dataset, easily dwarfing all other categories. In stark contrast, vehicles like Box Trucks, Pick-up Trucks, and Taxis exhibit exceptionally low crash frequencies across the board, appearing almost white on the color scale. While secondary factors like 'Following Too Closely' and 'Failure to Yield Right-of-Way' show moderate incidence levels, they are again almost exclusively tied to Sedans and SUVs, highlighting that everyday passenger vehicles and distracted driving are the primary drivers of the overall accident volume.")
    
    with t3:
        render_image_with_insight("plots/FactorDonut.png", "Share of Top Contributing Factors", 
            "Based on the provided donut chart detailing the 'Share of Top Contributing Factors,' the distribution is heavily dominated by just two primary categories: 'Driver Inattention/Distraction' (34.5%) and 'Unspecified' (32.9%). Together, these two factors account for more than two-thirds of all incidents represented in this top group, highlighting distracted driving as the leading known cause, while also revealing a significant gap in specific data collection due to the high volume of unspecified records. The remaining specific moving violations make up a much smaller fraction of the total share; 'Following Too Closely' (11.3%) and 'Failure to Yield Right-of-Way' (9.6%) represent roughly a fifth combined, leaving minor specific infractions like 'Passing or Lane Usage Improper' (6.1%) and 'Backing Unsafely' (5.6%) as the smallest contributors among the major factors.")
        
    with t4:
        with st.spinner("Loading Data Table..."):
            st.subheader("Contributing Factor Data")
            factor_summary = df.groupby('CONTRIBUTING FACTOR').agg(
                Total_Collisions=('COLLISION_ID', 'count'),
                Total_Injuries=('NUMBER OF PERSONS INJURED', 'sum'),
                Avg_Injuries_Per_Collision=('NUMBER OF PERSONS INJURED', 'mean')
            ).reset_index().sort_values(by='Total_Collisions', ascending=False)
            st.dataframe(factor_summary, use_container_width=True)

def create_injuries_tab():
    t1, t2, t3 = st.tabs(["INJURY DISTRIBUTION BY BOROUGH", "TOTAL INJURIES BY HOUR", "INJURED VS KILLED"])
    
    with t1:
        render_image_with_insight("plots/InjuryDistributionbyBorough.png", "Injury Distribution by Borough", 
            "Based on the provided boxplot detailing 'Injury Distribution by Borough,' the typical traffic incident results in very few injuries across all geographic areas, as shown by the medians and interquartile ranges compressed tightly at or near zero. However, the severity of outlier events varies significantly by location. The 'Unknown' location category contains the single most devastating incident recorded (40 injuries) along with a dense cluster of high-casualty events. Among the identified boroughs, Queens and the Bronx experience the most extreme outliers, with single crashes causing upwards of 30 injuries. Conversely, Manhattan stands out with the tightest overall distribution and the lowest maximum injury threshold (peaking below 20). This suggests that while accidents in Manhattan may be frequent, the borough's denser traffic patterns and slower average speeds likely mitigate the risk of the severe, high-impact collisions seen in areas with more open roadways or highways.")
    
    with t2:
        render_image_with_insight("plots/TotalInjuriesbyHour.png", "Total Injuries by Hour", 
            "The line chart of 'Total Injuries by Hour' demonstrates a clear bimodal distribution that closely tracks typical daily commuting patterns. Injuries reach their absolute lowest point during the early morning hours (3:00 AM to 5:00 AM) before experiencing a sharp rise that peaks around 8:00 AM, coinciding with the morning rush hour. Following a minor mid-morning dip, there is a sustained and significant climb throughout the afternoon, culminating in a daily maximum at 5:00 PM (17:00). This evening peak is notably higher and broader than the morning surge, suggesting that the combination of increased traffic volume, driver fatigue, and diminishing daylight during the evening commute creates the highest-risk window for injuries. After 6:00 PM, injury counts steadily decline as traffic volume tapers off into the night.")
    
    with t3:
        render_image_with_insight("plots/Injury_vs_Killed_By_Borough.png", "Injured vs Killed", 
            "Based on the scatter plot grid comparing 'Persons Killed' versus 'Persons Injured' across the boroughs, there is no direct correlation between the volume of injuries and the number of fatalities in a single incident; in fact, extreme events tend to be exclusively one or the other. The vast majority of crashes cluster tightly near zero for both metrics. However, looking at the outliers reveals that the events causing the highest number of injuries (such as those approaching 30 to 40 in the Bronx, Queens, and the 'Unknown' category) remarkably resulted in zero deaths. Conversely, the single most lethal incident—a stark outlier in Manhattan recording 8 fatalities—involved zero non-fatal injuries. This visual pattern suggests two distinct types of severe accidents: concentrated, catastrophic impacts that are immediately lethal to a small group (such as pedestrians or a single vehicle's occupants), and broader, multi-vehicle or mass-transit collisions that cause widespread but ultimately survivable injuries.")

def create_predictions_tab():
    t1, t2, t3 = st.tabs(["LINEAR", "LOGISTIC", "DECISION TREE"])
    
    with t1:
        # Need to work on this
        render_image_with_insight("plots/TopCoefficients.png", "Linear Model Coefficients", 
            "This plot shows the most important features influencing predictions in the linear model.")
    
    with t2:
        sub1, sub2 = st.tabs(["TOP COEFFICIENTS", "PREDICTED PROBABILITY"])
        with sub1:
            render_image_with_insight("plots/TopCoefficients.png", "Logistic Coefficients", 
                "Based on the horizontal bar chart displaying model coefficients, 'Failure to Yield Right-of-Way' stands out as the strongest predictor for increasing the probability of an injury, possessing a coefficient value nearly double that of several other major infractions. While earlier frequency charts indicated that 'Driver Inattention/Distraction' caused the highest raw volume of accidents, this predictive model suggests that 'Failure to Yield' is significantly more likely to actually result in physical harm when a crash does occur. Common moving violations like 'Driver Inattention/Distraction' and 'Following Too Closely' still prominently raise the likelihood of injury, but to a lesser degree. Notably, spatial and temporal features—such as the incident occurring in Brooklyn or on a Sunday—have a positive, yet extremely marginal, influence on injury probability when compared to the severe impact of direct, behavioral driving errors.")
        with sub2:
            render_image_with_insight("plots/PredictedProbability.png", "Predicted Probability Distribution", 
                "The 'Predicted Probability of Injury' histogram provides a high-level view of your model's confidence across the entire dataset. The distribution is unimodal and slightly right-skewed, with the vast majority of predicted probabilities concentrated between 0.20 and 0.35. This indicates that for most traffic incidents in this dataset, the model estimates a 20% to 35% chance of an injury occurring. While there is a secondary 'hump' or shoulder around the 0.45 mark, very few incidents are assigned a high-certainty probability (above 0.60). This suggests that while certain factors (like 'Failure to Yield') significantly increase risk, the presence of an injury in a collision is still subject to a high degree of randomness or depends on variables not fully captured by the current feature set.")
    with t3:
        render_image_with_insight("plots/DecisionTree_minimal.png", "Decision Tree Visual", 
            "Decision Tree visualization utilizing borough-level data to map out injury outcomes.")



def create_kpi_tab(df):
    total_crashes = df.shape[0]
    total_injuries = df['NUMBER OF PERSONS INJURED'].sum()
    total_fatalities = df['NUMBER OF PERSONS KILLED'].sum()

    injury_rate = total_injuries / total_crashes
    fatality_rate = total_fatalities / total_crashes
    peak_hour = df['HOUR'].value_counts().idxmax()
    peak_day = df['DAY_OF_WEEK'].value_counts().idxmax()
    peak_year = df['YEAR'].value_counts().idxmax()
    severity_score = (total_injuries + (total_fatalities * 5)) / total_crashes

    valid_df = df[df['BOROUGH'] != 'Unknown']
    high_risk_borough = (
        valid_df.groupby('BOROUGH')['NUMBER OF PERSONS INJURED'].sum() /
        valid_df['BOROUGH'].value_counts()
    ).idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7 = st.columns(3)

    col1.metric("Injury Rate", f"{injury_rate * 100:.2f}%")
    col2.metric("Death Rate", f"{fatality_rate * 100:.2f}%")
    col3.metric("Peak Hour", f"{peak_hour}:00")
    col4.metric("Peak Day", peak_day)

    col5.metric("Peak Year", peak_year)
    col6.metric("Severity Score", f"{severity_score * 100:.2f}%")
    col7.metric("High-Risk Borough", high_risk_borough)

    st.subheader("📊 KPI Insights")

    st.markdown("### Injury Rate")
    st.write(
        "The injury rate is 37.18%, meaning a large portion of crashes result in injuries. This shows that injuries are a common outcome in crash events."
    )

    st.markdown("### Death Rate")
    st.write(
        "The death rate is 0.18%, which is very low compared to the injury rate. This indicates that while crashes often lead to injuries, fatal outcomes are rare."
    )

    st.markdown("### Peak Crash Time and Day")
    st.write(
        "Crashes are highest around 16:00 (4 PM) and on Fridays. "
        "This is due to busy traffic times, especially when people are commuting or heading into the weekend, showing that crashes are more frequent at the end of the week compared to other days."
    )

    st.markdown("### Severity Score")
    st.write(
        "The severity score 38.08% gives a general idea of how serious the crashes are overall. "
        "This means many crashes result in injuries or are somewhat serious."
    )

    st.markdown("### High-Risk Borough")
    st.write(
        "The high-risk borough is Brooklyn,because crashes there tend to result in more injuries on average. "
        "It is not just about how many crashes happen, but how serious they are."
    )



def create_time_tab(df):
    tabs = st.tabs(["CRASHES BY YEAR", "CRASHES BY MONTH", "CRASHES BY HOUR", "INJURY HEATMAP"])

    year_counts = (
        df[df["YEAR"] >= 2017]
        .groupby("YEAR")
        .size()
        .reset_index(name="Crash Count")
        .sort_values("YEAR")
    )

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    month_counts = df.groupby("MONTH").size().reset_index(name="Crash Count")
    month_counts["MONTH"] = pd.Categorical(month_counts["MONTH"], categories=month_order, ordered=True)
    month_counts = month_counts.sort_values("MONTH")

    hour_counts = df.groupby("HOUR").size().reset_index(name="Crash Count").sort_values("HOUR")

    # --- YEAR ---
    with tabs[0]:
        fig = px.line(year_counts, x="YEAR", y="Crash Count", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"<div class='insight-box'><b>Insight:</b><br>Crash counts increased sharply between 2017 and 2018, reaching their highest levels in 2018 and 2019. "
        "Following this peak, there is a clear downward trend starting in 2020, with crashes decreasing each year afterward. "
        "This decline is notable and suggests a shift in driving patterns or external factors affecting road activity. "
        "The overall pattern indicates that crash frequency was highest in the late 2010s and has been steadily improving in recent years.</div>", unsafe_allow_html=True)

    # --- MONTH ---
    with tabs[1]:
        fig = px.bar(month_counts, x="MONTH", y="Crash Count")

        fig.update_traces(
            text=month_counts["Crash Count"].apply(lambda x: f"{x/1000:.1f}K"),
            textposition="outside",
            cliponaxis=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"<div class='insight-box'><b>Insight:</b><br>Crash activity is fairly consistent throughout the year, but there is a clear seasonal pattern. "
        "Crashes are slightly lower in the early months of the year, especially in February and April, and begin to increase as the weather gets warmer. "
        "The highest number of crashes occurs during the summer months, particularly around June and July, when travel activity is higher and more people are on the roads. "
        "Crash levels remain relatively high into early fall, such as in September and October, before gradually decreasing toward the end of the year. "
        "This trend suggests that increased travel, outdoor activity, and higher traffic volume during warmer months contribute to more accidents, while colder months may see fewer crashes due to reduced travel and more cautious driving conditions.</div>", unsafe_allow_html=True)

    # --- HOUR ---
    with tabs[2]:
        fig = px.line(hour_counts, x="HOUR", y="Crash Count", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"<div class='insight-box'><b>Insight:</b><br>Crash frequency is lowest during the early morning hours, especially between midnight and 5 AM, when there is very little traffic on the roads. "
        "As the day begins, crashes start to increase, with a noticeable rise during morning hours as more people begin commuting. "
        "The number of crashes continues to grow throughout the day and reaches its highest levels during the afternoon and early evening hours, around typical rush hours. "
        "After this peak, crash frequency gradually declines into the night as traffic decreases. "
        "This pattern suggests that crash occurrences are strongly related to traffic volume, with more vehicles on the road leading to a higher chance of accidents.</div>", unsafe_allow_html=True)

    # --- INJURY HEATMAP ---
    with tabs[3]:
        st.image("plots/InjuryRateHeatmap.png", use_container_width=True)

        st.markdown(f"<div class='insight-box'><b>Insight:</b><br>This heatmap shows how injury rates change across different boroughs and times of the day, and there are some clear patterns. Injury rates generally increase in the late afternoon and evening, especially between 5 PM and 9 PM, which likely matches peak traffic hours.  Brooklyn stands out with the highest injury rates, reaching around 36%, followed by the Bronx and Queens, while Manhattan tends to have lower rates throughout the day. Staten Island shows more stable and slightly lower injury rates compared to other boroughs.  Overall, this visualization shows that both the location and time of day affect how serious crashes are, not just how often they happen.</div>", unsafe_allow_html=True)



def create_location_tab(df):

    color_map = {
        "BROOKLYN": "#4C6EF5",
        "QUEENS": "#E8590C",
        "MANHATTAN": "#12B886",
        "BRONX": "#845EF7",
        "STATEN ISLAND": "#F59F00"
    }

    tabs = st.tabs(["CRASHES BY BOROUGH", "CRASH MAP", "SEVERITY BY BOROUGH"])

    # --- TAB 1: BOROUGH CHART ---
    with tabs[0]:
        borough_counts = (
            df[df["BOROUGH"] != "Unknown"]
            .groupby("BOROUGH")
            .size()
            .reset_index(name="Crash Count")
            .sort_values("Crash Count", ascending=False)
        )

        fig = px.bar(
            borough_counts,
            x="BOROUGH",
            y="Crash Count",
            color="BOROUGH",
            color_discrete_map=color_map,
            text="Crash Count"
        )

        fig.update_traces(texttemplate="%{text:,}", textposition="outside")

        fig.update_layout(
            xaxis_title="Borough",
            yaxis_title="Number of Crashes",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"<div class='insight-box'><b>Insight:</b><br>Brooklyn has the highest number of crashes, followed by Queens. Manhattan has the next highest number of crashes, followed by the Bronx, while Staten Island has the lowest number of crashes. This pattern shows that crashes are not evenly distributed across the city. Boroughs with larger populations and more road activity tend to have more accidents. For example, Brooklyn and Queens are the largest boroughs and have more vehicles on the road, which increases the chances of collisions. Manhattan also has a high number of crashes, which may be due to its dense traffic and busy streets, even though it is smaller in size. On the other hand, Staten Island has fewer crashes, which suggests lower traffic volume and less congestion compared to other boroughs.</div>", unsafe_allow_html=True)


    # --- TAB 2: MAP ---
    with tabs[1]:
        map_df = df[
            (df["LATITUDE"].between(40, 41)) &
            (df["LONGITUDE"].between(-75, -73))
        ][["LATITUDE", "LONGITUDE", "BOROUGH"]].copy()

        map_df = map_df.sample(min(10000, len(map_df)), random_state=42)

        st.map(map_df.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon"}))

        st.markdown(f"<div class='insight-box'><b>Insight:</b><br> The map shows that crash locations are concentrated in New York City. "
            "Denser clusters appear in more populated boroughs, suggesting that crashes are more likely in areas with heavier traffic and road activity.</div>", unsafe_allow_html=True)

    # --- TAB 3: SEVERITY BY BOROUGH ---
    with tabs[2]:
        severity_df = (
            df[df["BOROUGH"] != "Unknown"]
            .groupby("BOROUGH")
            .agg(
                total_crashes=("BOROUGH", "count"),
                total_injuries=("NUMBER OF PERSONS INJURED", "sum")
            )
            .reset_index()
        )

        severity_df["Injuries per Crash"] = (
            severity_df["total_injuries"] / severity_df["total_crashes"]
        )

        severity_df["Severity %"] = severity_df["Injuries per Crash"] * 100
        severity_df = severity_df.sort_values("Injuries per Crash", ascending=False)

        fig = px.bar(
            severity_df,
            x="BOROUGH",
            y="Injuries per Crash",
            color="BOROUGH",
            color_discrete_map=color_map,
            text="Severity %"
        )

        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")

        fig.update_layout(
            xaxis_title="Borough",
            yaxis_title="Average Injuries per Crash",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"<div class='insight-box'><b>Insight:</b><br> Brooklyn has the highest average injuries per crash, followed closely by the Bronx. Queens and Staten Island show similar levels, while Manhattan has the lowest average injuries per crash. This means that even though Manhattan has many crashes, they are usually less severe. On the other hand, crashes in Brooklyn and the Bronx are more likely to result in higher injuries. Staten Island, even with fewer total crashes, still has a relatively high number of injuries per crash, which shows that crashes there can still be serious.</div>", unsafe_allow_html=True)