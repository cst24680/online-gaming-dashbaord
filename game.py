
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Online Gaming Dashboard",
    page_icon="🎮",
    layout="wide"
)

# --------------------------------
# 2. LOAD DATASET
# --------------------------------

df = pd.read_csv("online_gaming_behavior_insights.csv")

st.title("🎮 Online Gaming Behavior Insights")
st.write("Interactive Dashboard for Analyzing Online Gaming Behaviour")

st.divider()

# --------------------------------
# 3. SIDEBAR FILTERS
# --------------------------------

st.sidebar.header("Player Filters")

# Age slider
age = st.sidebar.slider(
    "Select Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

# Gender filter
gender = st.sidebar.multiselect(
    "Select Gender",
    sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

# Game genre filter
genre = st.sidebar.multiselect(
    "Select Game Genre",
    sorted(df["GameGenre"].dropna().unique()),
    default=sorted(df["GameGenre"].dropna().unique())
)

# Location filter
location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + sorted(df["Location"].dropna().unique())
)

# Engagement level filter
engagement = st.sidebar.multiselect(
    "Select Engagement Level",
    sorted(df["EngagementLevel"].dropna().unique()),
    default=sorted(df["EngagementLevel"].dropna().unique())
)

# --------------------------------
# 4. FILTER THE DATASET
# --------------------------------

filtered_df = df[
    (df["Age"].between(age[0], age[1])) &
    (df["Gender"].isin(gender)) &
    (df["GameGenre"].isin(genre)) &
    (df["EngagementLevel"].isin(engagement))
].copy()

if location != "All":
    filtered_df = filtered_df[
        filtered_df["Location"] == location
    ]

# --------------------------------
# 5. DISPLAY KPIs
# --------------------------------

st.header("Player Statistics")

if filtered_df.empty:
    st.warning("No data available. Please change the filters.")
    st.stop()

with st.container():

    col1, col2, col3, col4 = st.columns(4)

    # KPI calculations

    total_records = len(filtered_df)

    total_players = filtered_df["PlayerID"].nunique()

    total_playtime = filtered_df["PlayTimeHours"].sum()

    average_playtime = filtered_df["PlayTimeHours"].mean()

    # Display KPIs

    col1.metric(
        "Total Records",
        total_records
    )

    col2.metric(
        "Total Players",
        total_players
    )

    col3.metric(
        "Total Playtime",
        f"{total_playtime:.2f} Hours"
    )

    col4.metric(
        "Average Playtime",
        f"{average_playtime:.2f} Hours"
    )

    col5, col6 = st.columns(2)

    total_purchases = filtered_df["InGamePurchases"].sum()

    average_session = filtered_df["AvgSessionDurationMinutes"].mean()

    col5.metric(
        "In-game Purchases",
        int(total_purchases)
    )

    col6.metric(
        "Average Session Duration",
        f"{average_session:.2f} Min"
    )

st.divider()

# --------------------------------
# 6. GROUP BY ANALYSIS
# --------------------------------

st.header("Game Genre Analysis")

genre_count = filtered_df.groupby(
    "GameGenre"
)["PlayerID"].count().reset_index()

genre_count.columns = [
    "Game Genre",
    "Number of Players"
]

st.dataframe(
    genre_count,
    width="stretch"
)

st.divider()

# --------------------------------
# 7. CREATE TABS
# --------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Dataset Overview",
    "Data Analysis",
    "Visualizations",
    "Insights"
])

# --------------------------------
# TAB 1 - DATASET OVERVIEW
# --------------------------------

with tab1:

    st.subheader("Dataset Preview")

    st.dataframe(
        filtered_df.head(20),
        width="stretch"
    )

    with st.expander("View Dataset Information"):

        st.write("Total Rows:", filtered_df.shape[0])

        st.write("Total Columns:", filtered_df.shape[1])

        st.write(
            "Column Names:",
            filtered_df.columns.tolist()
        )

        st.write("Missing Values:")

        st.write(filtered_df.isnull().sum())

# --------------------------------
# TAB 2 - DATA ANALYSIS
# --------------------------------

with tab2:

    st.subheader("Player Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.write("Players by Engagement Level")

        engagement_count = filtered_df.groupby(
            "EngagementLevel"
        )["PlayerID"].count()

        st.bar_chart(engagement_count)

    with col2:

        st.write("Average Playtime by Game Difficulty")

        difficulty = filtered_df.groupby(
            "GameDifficulty"
        )["PlayTimeHours"].mean()

        st.bar_chart(difficulty)

    st.subheader("Category-wise Summary")

    category_summary = filtered_df.groupby(
        "GameGenre"
    ).agg(
        Player_Count=("PlayerID", "count"),
        Average_Playtime=("PlayTimeHours", "mean"),
        Total_Playtime=("PlayTimeHours", "sum")
    ).reset_index()

    st.dataframe(
        category_summary,
        width="stretch"
    )

# --------------------------------
# TAB 3 - VISUALIZATIONS
# --------------------------------

with tab3:

    st.subheader("Data Visualizations")

    # BAR CHART

    bar_data = filtered_df.groupby(
        "GameGenre"
    )["PlayerID"].count().reset_index()

    bar_data.columns = [
        "GameGenre",
        "Players"
    ]

    bar_fig = px.bar(
        bar_data,
        x="GameGenre",
        y="Players",
        color="GameGenre",
        title="Number of Players by Game Genre",
        labels={
            "GameGenre": "Game Genre",
            "Players": "Number of Players"
        }
    )

    st.plotly_chart(
        bar_fig,
        width="stretch"
    )

    st.write(
        "Interpretation: This chart compares the number of "
        "players belonging to different game genres."
    )

    st.divider()

    # LINE CHART

    line_data = filtered_df.groupby(
        "Age"
    )["PlayTimeHours"].mean().reset_index()

    line_fig = px.line(
        line_data,
        x="Age",
        y="PlayTimeHours",
        markers=True,
        title="Average Playtime Across Different Ages",
        labels={
            "Age": "Player Age",
            "PlayTimeHours": "Average Playtime (Hours)"
        }
    )

    st.plotly_chart(
        line_fig,
        width="stretch"
    )

    st.write(
        "Interpretation: This chart shows how average gaming "
        "time varies with player age."
    )

    st.divider()

    # SCATTER PLOT

    scatter_fig = px.scatter(
        filtered_df,
        x="PlayTimeHours",
        y="PlayerLevel",
        color="EngagementLevel",
        title="Playtime vs Player Level",
        labels={
            "PlayTimeHours": "Playtime (Hours)",
            "PlayerLevel": "Player Level",
            "EngagementLevel": "Engagement Level"
        }
    )

    st.plotly_chart(
        scatter_fig,
        width="stretch"
    )

    st.write(
        "Interpretation: This scatter plot examines the "
        "relationship between playtime and player level."
    )

# --------------------------------
# TAB 4 - INSIGHTS
# --------------------------------

with tab4:

    st.subheader("Key Insights")

    top_genre = filtered_df.groupby(
        "GameGenre"
    )["PlayerID"].count().idxmax()

    top_engagement = filtered_df.groupby(
        "EngagementLevel"
    )["PlayerID"].count().idxmax()

    average_level = filtered_df["PlayerLevel"].mean()

    average_achievements = filtered_df[
        "AchievementsUnlocked"
    ].mean()

    st.write(
        "1. Most popular game genre:",
        top_genre
    )

    st.write(
        "2. Most common engagement level:",
        top_engagement
    )

    st.write(
        "3. Average player level:",
        round(average_level, 2)
    )

    st.write(
        "4. Average achievements unlocked:",
        round(average_achievements, 2)
    )

# --------------------------------
# 8. FOOTER
# --------------------------------

st.divider()

st.caption(
    "Online Gaming Behavior Insights | Python Programming Lab Exercise 6"
)
