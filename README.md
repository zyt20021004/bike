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
