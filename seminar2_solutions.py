# Tasks
# 1. Choose a data set you are interested in
# 2. Select a region by slicing a boundary box
# 3. Estimate the spatial mean over time
# 4. Apply the MK Original Test on your time series and discuss the results
# 5. Create a plot for your data and add the test result to your plot

### Import the models and open a data set
# First you need to import all the modules we need and set an alias for each, so you do not need to write their full
# names every time.

# %% code

import xarray as xr
import matplotlib.pyplot as plt
import pymannkendall as mk

### Open the dataset using xarray and assign the data you are interested in to a new variable.
gleam = xr.open_dataset("data/gleam_europe_monmean_reduced.nc")
sm = gleam["surface_soil_moisture"]
print(sm)

### Select the region and take the spatial average
# To subset a region you can select multiple cells using xarray's sel() method in combination with the slice() function.
# Note that the order of the coordinates is important!

region = sm.sel(lon=slice(9, 10), lat=slice(51, 50))
print(region)

# You can see we selected a region with 4x4 grid cells.
# Calculate the spatial average over time using the ```mean()``` method. By passing the ```axis()``` argument you can
# specify which dimension to average. In this case we choose the 'lat' (1) and 'lon' (2) axes to return a time series.

# If you are unsure which number refers to which dimension, run ```region.dims``` before.

region_avg = region.mean(axis=(1, 2))
print(region_avg)

### Applying the Mann-Kendall Test
# Apply the Mann-Kendall Test on your time series and assign it to a new variable.
# Since our data has seasonality, and the time steps are monthly, we use the Seasonal MK-Test and set the period to 12.

results = mk.seasonal_test(region_avg, period=12)
print(results)

# We can reject the Null-Hypothesis.
# The Mann-Kendall Test shows a decreasing trend for the variable soil moisture with a very high significance (p < 0.0001).

### Visualising the results
# The last task is to visualize the time series using matplotlib.pyplot and add the results of the MK-Test to the plot.

fig = plt.figure(figsize=(15, 5))
ax = fig.add_subplot(111)
ax.plot(region_avg.time, region_avg.values, linestyle='-', linewidth=0.5, color='darkblue')
ax.set_title("Monthly surface soil moisture")
ax.set_ylabel("Surface soil moisture m3 m-3")
ax.set_ylim(0.25, 0.45)
ax.text(region_avg.time[200], 0.425, s=f"{results.trend} Trend \np={results.p:e}")
ax.grid(axis='y')
plt.show()
