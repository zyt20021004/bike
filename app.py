
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Bike Sharing Demand Dashboard",
    page_icon="🚲",
    layout="wide"
)

st.title("🚲 Bike Sharing Demand Dashboard | Team Name")

st.caption(
    "For Bike Sharing Operations Managers: "
    "Plan bike availability and staffing based on "
    "historical hourly demand and weather conditions."
)

# --------------------------------------------------
# 2. Load and prepare data
# --------------------------------------------------

@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "bike.csv"
    df = pd.read_csv(file_path)

    df["datetime"] = pd.to_datetime(df["datetime"])

    df["hour"] = df["datetime"].dt.hour
    df["month"] = df["datetime"].dt.month

    season_map = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }

    weather_map = {
        1: "Clear / Partly Cloudy",
        2: "Mist / Cloudy",
        3: "Light Rain / Snow",
        4: "Severe Weather"
    }

    df["season_label"] = df["season"].map(season_map)
    df["weather_label"] = df["weather"].map(weather_map)

    return df


df = load_data()

# --------------------------------------------------
# 3. Sidebar filters
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

season_options = [
    "All Seasons",
    "Spring",
    "Summer",
    "Fall",
    "Winter"
]

selected_season = st.sidebar.selectbox(
    "Select Season",
    season_options
)

weather_options = [
    "All Weather",
    "Clear / Partly Cloudy",
    "Mist / Cloudy",
    "Light Rain / Snow",
    "Severe Weather"
]

selected_weather = st.sidebar.selectbox(
    "Select Weather Condition",
    weather_options
)

filtered_df = df.copy()

if selected_season != "All Seasons":
    filtered_df = filtered_df[
        filtered_df["season_label"] == selected_season
    ]

if selected_weather != "All Weather":
    filtered_df = filtered_df[
        filtered_df["weather_label"] == selected_weather
    ]

if filtered_df.empty:
    st.warning("No data is available for these filters.")
    st.stop()

# --------------------------------------------------
# 4. Calculate three KPIs
# --------------------------------------------------

total_rentals = filtered_df["count"].sum()

average_rentals = filtered_df["count"].mean()

hourly_demand = (
    filtered_df.groupby("hour")["count"]
    .mean()
)

peak_hour = int(hourly_demand.idxmax())
peak_demand = hourly_demand.max()

# --------------------------------------------------
# 5. Display KPI row
# --------------------------------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Rentals",
        value=f"{total_rentals:,.0f}"
    )

with col2:
    st.metric(
        label="Average Hourly Rentals",
        value=f"{average_rentals:,.2f}"
    )

with col3:
    st.metric(
        label=f"Peak Hour Demand ({peak_hour:02d}:00)",
        value=f"{peak_demand:,.2f}"
    )

# --------------------------------------------------
# 6. Chart 1: Hourly rental demand
# --------------------------------------------------

st.subheader("Hourly Rental Demand")

st.write(
    "Compare average rental demand between working "
    "days and non-working days to identify peak hours."
)

hourly_comparison = (
    filtered_df.groupby(["hour", "workingday"])["count"]
    .mean()
    .unstack("workingday")
    .reindex(range(24))
)

fig1, ax1 = plt.subplots(figsize=(10, 4))

if 1 in hourly_comparison.columns:
    ax1.plot(
        hourly_comparison.index,
        hourly_comparison[1],
        marker="o",
        label="Working Day"
    )

if 0 in hourly_comparison.columns:
    ax1.plot(
        hourly_comparison.index,
        hourly_comparison[0],
        marker="o",
        label="Non-Working Day"
    )

ax1.set_title("Average Hourly Bike Rentals")
ax1.set_xlabel("Hour of Day")
ax1.set_ylabel("Average Rentals")
ax1.set_xticks(range(24))
ax1.grid(True, alpha=0.3)
ax1.legend()
fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)

st.info(
    "Decision: Adjust bike availability and staffing "
    "during high-demand periods."
)

# --------------------------------------------------
# 7. Chart 2: Weather and demand
# --------------------------------------------------

st.subheader("Rental Demand by Weather")

st.write(
    "Compare average hourly rentals across weather "
    "conditions to support operational planning."
)

# Exclude severe weather due to only one observation
weather_df = filtered_df[
    filtered_df["weather"] != 4
].copy()

weather_summary = (
    weather_df.groupby("weather_label")["count"]
    .agg(["mean", "size"])
)

if not weather_summary.empty:

    fig2, ax2 = plt.subplots(figsize=(9, 4))

    weather_summary["mean"].plot(
        kind="bar",
        ax=ax2
    )

    ax2.set_title("Average Rentals by Weather Condition")
    ax2.set_xlabel("Weather Condition")
    ax2.set_ylabel("Average Hourly Rentals")
    ax2.tick_params(axis="x", rotation=15)
    fig2.tight_layout()

    st.pyplot(fig2)
    plt.close(fig2)

    st.caption(
        "The severe weather category is excluded "
        "from this chart because the full dataset "
        "contains only one observation."
    )

    with st.expander("Weather sample sizes"):
        st.dataframe(
            weather_summary.rename(
                columns={
                    "mean": "Average Rentals",
                    "size": "Hourly Records"
                }
            ),
            use_container_width=True
        )

else:
    st.warning(
        "Insufficient observations for a reliable "
        "weather comparison."
    )

st.info(
    "Decision: Use historical weather-related demand "
    "patterns to adjust bike supply plans."
)

# --------------------------------------------------
# 8. Data information and limitations
# --------------------------------------------------

st.divider()

st.subheader("Data Information")

start_date = df["datetime"].min().strftime("%b %d, %Y")
end_date = df["datetime"].max().strftime("%b %d, %Y")

st.caption(
    f"Data Period: {start_date} – {end_date} "
    "(Kaggle historical snapshot, days 1–19 each month). "
    "Intended Production Refresh: Daily. "
    "Management Review: Weekly, every Monday morning."
)

st.warning(
    "This dashboard uses historical data from 2011–2012, "
    "not live rental data. The CSV contains only days 1–19 "
    "of each month. Results describe observed rental "
    "patterns rather than current bike availability."
)
