# bike
bike
# Data app -- Bike Sharing Demand
## Step 1 : Pick a Dataset and a Decision-Maker
I selected the Bike Sharing Demand dataset from Kaggle, which contains 10,886 hourly records of bike rentals in Washington, D.C., from January 2011 to December 2012.  

This dataset contains hourly rental data for the bike-sharing system in Washington, USA over approximately two years, covering:number of bike rentals,time,temperature,humidity,weather conditions,working days and holidays,rental volumes for members and non-members.   

I chose this dataset because bike-sharing demand changes significantly throughout the day and under different weather conditions. Understanding these patterns can help operators improve bike availability and resource allocation.It can be used for the bike demand and fleet management dashboard.

```python
import numpy as np 
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
df=pd.read_csv('bike.csv')
df.info()
df.columns
df.datetime
```

Data Fields from Kaggle :   
datetime - hourly date + timestamp    
season -  1 = spring, 2 = summer, 3 = fall, 4 = winter   
holiday - whether the day is considered a holiday.  
workingday - whether the day is neither a weekend nor holiday.  
weather - 1: Clear, Few clouds, Partly cloudy, Partly cloudy.  
2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist.  
3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds.    
4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog   
temp - temperature in Celsius  
atemp - "feels like" temperature in Celsius.  
humidity - relative humidity.   
windspeed - wind speed.  
casual - number of non-registered user rentals initiated.  
registered - number of registered user rentals initiated.  
count - number of total rentals.

The data is real and it was provided by Hadi Fanaee Tork using data from Capital Bikeshare.
Our target user is a **Bike Sharing Operations Manager**.
The manager is responsible for monitoring rental demand, identifying peak hours, and adjusting bike availability and staffing based on historical demand patterns and weather conditions.   
The dashboard helps the operations manager identify peak rental periods and understand how weather affects demand, supporting better bike supply planning and operational decisions.

## Step 2 : Justify the dashboard
### Q1. Who will look at it, more than once?

The Bike Sharing Operations Manager will review the dashboard every Monday to plan bike availability and staffing for the upcoming week based on historical demand patterns and expected weather conditions.

### Q2. What decision does it support? 

If the operations manager sees that rental demand is consistently high during weekday morning and evening rush hours, they will increase bike availability and adjust staffing during those periods.

If historical data shows lower demand under certain weather conditions, they will reduce planned bike supply and schedule maintenance during these quieter periods.

### Q3. What do they do today without it — and what does that cost them in time, money, or mistakes?

Without the dashboard, managers would manually analyze historical rental records and weather data, which would be time-consuming and make demand patterns harder to identify.

Poor planning could lead to bike shortages during peak hours or excess bike availability during low-demand periods, resulting in lost rental opportunities and inefficient resource allocation.


### Q4. Why a dashboard rather than a weekly email, a report, or an alert?

Unlike static reports or emails, the dashboard allows managers to interactively filter rental data by season, weather conditions, and working days.Managers can quickly compare demand patterns under different conditions and make repeated operational decisions.A dashboard is therefore more suitable for weekly planning than a fixed report or a simple alert.

## Step 3 ： Decide What Matters
### 1 Exploratory Data Analysis

```python
df["datetime"] = pd.to_datetime(df["datetime"])
print("Dataset shape:", df.shape)
print("Dataset types:", df.dtypes)
print("Missing values:", df.isnull().sum())
#从日期中提取出年，月，小时
df["hour"] = df["datetime"].dt.hour
df["month"] = df["datetime"].dt.month
df["year"] = df["datetime"].dt.year
df.head()
#先分析一下工作日每小时的租赁需求
hourly_demand = (df[df["workingday"] == 1].groupby("hour")["count"].mean())
hourly_demand.plot()
plt.title("Average Hourly Bike Rentals on Working Days")
plt.xlabel("Hour")
plt.ylabel("Average Rentals")
plt.xticks(range(24))
plt.show()
# 分析非工作日情况
hourly_demand = (df[df["workingday"] == 0].groupby("hour")["count"].mean())
hourly_demand.plot()
plt.title("Average Hourly Bike Rentals on Nonworking Days")
plt.xlabel("Hour")
plt.ylabel("Average Rentals")
plt.xticks(range(24))
plt.show()
```

We can see from the chart that 8 a.m. and 5 to 6 p.m. on working days are the periods with higher rental demand. The operations manager should increase bike availability during morning and evening rush hours. While the peak hours on non-working days occur from noon to afternoon.

```python
# 再分析一下天气对租赁状况的影响
df.weather.value_counts()
weather_demand=(df.groupby('weather')['count'].mean())
weather_demand.plot.bar()
plt.title("Average Bike Rentals by Weather Condition")
plt.xlabel("Weather Condition")
plt.ylabel("Average Rentals")
plt.show()
```

From the bar chart, it shows that the average rental volume under normal weather conditions is higher than that in light rain or snow weather.  
However, there is only one record of severe weather, so a reliable operation plan cannot be formulated based on this category.
```python
season_demand=(df.groupby('season')['count'].mean())
season_demand.plot.bar()
plt.title("Average Bike Rentals by Season")
plt.xlabel("Season")
plt.ylabel("Average Rentals")
plt.show()
```

1 = spring, 2 = summer, 3 = fall, 4 = winter   
The bar charts illustrates that the average rental is higher in summer and fall,and is lowest in spring.
**Conclusion:**
The exploratory analysis reveals that rental demand varies significantly by hour, working-day status, weather conditions and seasons.  
Therefore, our dashboard will focus on identifying peak rental periods and comparing demand across weather conditions to support bike supply planning.

###Answer the questions
Three KPIs:
1. Total Rentals — Measures overall rental demand.
2. Average Hourly Rentals — Measures typical demand levels.
3. Peak Hour Demand — Identifies the highest average hourly demand.
Two Supporting Charts:
1. Average Hourly Rentals by Working-Day Type — Identifies peak rental periods on working and non-working days.
2. Average Rentals by Weather Condition — Compares demand under different weather conditions.
Filters: Season and Weather Condition.
Two Excluded Elements:
1. Casual vs. Registered Users — Not essential for immediate bike supply decisions.
2. Detailed Temperature and Humidity Charts — Add complexity without substantially improving the targeted decisions.
Data Limitations:
The dataset contains historical records from January 2011 to December 2012, covering only the first 19 days of each month. The severe weather category contains only one observation and is excluded from the weather comparison.
Dashboard Layout:
Three KPIs at the top, two explanatory charts in the middle, filters in the sidebar, and data limitations at the bottom.

## Step 4 : Decide the Refresh Frequency
### Q1. How often should the data be refreshed ?
In a real-world system, rental data should be refreshed daily after the previous day's transactions are completed. Although rentals occur hourly, our dashboard mainly supports weekly bike supply and staffing decisions. Daily updates provide sufficiently recent information without the additional cost of real-time data processing.

### Q2. How often should someone review it, and is that the same thing? 
The Bike Sharing Operations Manager should review the dashboard every Monday morning to plan bike availability and staffing for the upcoming week. Data refreshes daily, but the manager reviews it weekly because major resource allocation decisions are made on a weekly basis.


### Q3. What should be tracked over time, and what should trigger action? 
We will track Peak Hour Demand over time. If the average rental demand during a peak hour increases by more than 30% compared with the historical baseline for the same hour and working-day type, the operations manager should review the bike supply plan and consider allocating additional bikes and staff.
This 30% threshold is a proposed operational rule, not an existing company policy. It should be adjusted based on actual bike availability and operational capacity.


### Q4. What does stale data cost? What goes wrong if the dashboard is a day — or a week — out of date?
If data is one day outdated, managers may miss recent changes in rental demand caused by weather or travel patterns, leading to inefficient bike supply decisions.
If data is one week outdated, managers may repeatedly underestimate peak-hour demand, resulting in bike shortages, lost rental opportunities, and lower customer satisfaction. Alternatively, overestimating demand could lead to unnecessary staffing and maintenance costs.
Therefore, daily data refresh and weekly management reviews provide a reasonable balance between data freshness, operational efficiency, and cost.




