"""
Script for analyzing Google Trends data using pytrends.
Features:
- Fetch trends data for a list of keywords.
- Plot time series of interest over time.
- Create a bar plot of average interest with growth indicators (sorted by growth).
"""

# Configurable Variables
KEYWORDS = ["trauma", "meditazione", "ipnosi", "mindfulness", "hikikomori", "autostima"]
BATCH_SIZE = 5
PAUSE_BETWEEN_REQUESTS = 0.2
GEO = "IT-52"  # Geo location (e.g., "IT-52" for Tuscany)
TIMEFRAME = 'today 5-y'  # Timeframe for trends (e.g., 'today 5-y', 'today 1-m', etc.)
OUTPUT_PATH = "GoogleTrends_Mensile.csv"  # CSV output path
PLOT_PATH_SEASONAL = "GoogleTrends_Mensile_Plot.png"  # Line plot path
BAR_PLOT_PATH = "GoogleTrends_Bar_Plot_Sorted_Averages.png"  # Bar plot path

# GEO Options:
# - "IT" for Italy (nationwide)
# - "IT-52" for Tuscany
# - "IT-62" for Lazio
# - "" for Worldwide

# TIMEFRAME Options:
# - 'now 1-H': Last hour
# - 'now 4-H': Last 4 hours
# - 'now 1-d': Last day
# - 'now 7-d': Last 7 days
# - 'today 1-m': Past 30 days
# - 'today 3-m': Past 90 days
# - 'today 12-m': Past 12 months
# - 'today 5-y': Past 5 years
# - 'all': Since the beginning of available data


# Import Libraries
import subprocess
import sys
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from sklearn.linear_model import LinearRegression
from pytrends.request import TrendReq
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Install missing packages quietly
for package in ["pytrends", "pandas", "matplotlib", "numpy", "scikit-learn"]:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])

def get_trends_data(keywords, pause, geo, timeframe):
    pytrends = TrendReq(hl='it-IT', tz=360, timeout=(10, 25))
    all_data = {}
    for keyword in keywords:
        for attempt in range(4):
            try:
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
                trend_data = pytrends.interest_over_time()
                if trend_data is not None and not trend_data.empty:
                    all_data[keyword] = trend_data.resample('ME').mean()[keyword]
                    print(f"Data retrieved for '{keyword}'.")
                    break
                else:
                    print(f"No data for '{keyword}'.")
            except Exception as e:
                print(f"Error with '{keyword}': {e}")
                if attempt < 3:
                    time.sleep(pause)
        time.sleep(pause)
    return pd.DataFrame(all_data)

# Fetch data
results = []
for i in range(0, len(KEYWORDS), BATCH_SIZE):
    batch = KEYWORDS[i:i+BATCH_SIZE]
    df_batch = get_trends_data(batch, pause=PAUSE_BETWEEN_REQUESTS, geo=GEO, timeframe=TIMEFRAME)
    results.append(df_batch)

df_combined = pd.concat(results, axis=1)
df_combined.to_csv(OUTPUT_PATH)

# Plot time series
fig, ax = plt.subplots(figsize=(12, 8))
for keyword in df_combined.columns:
    ax.plot(df_combined.index, df_combined[keyword], label=keyword)
ax.set_title(f'Google Trends: Monthly Analysis ({TIMEFRAME})')
ax.set_xlabel('Time')
ax.set_ylabel('Interest (%)')
ax.legend(title='Keywords', loc='upper left', bbox_to_anchor=(1.05, 1))
ax.grid(True)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.tight_layout()
plt.savefig(PLOT_PATH_SEASONAL)

# Calculate averages and trends
averages = df_combined.mean()
slopes = {}
for keyword in df_combined.columns:
    x = np.arange(len(df_combined.index)).reshape(-1, 1)
    y = df_combined[keyword].fillna(0).values
    model = LinearRegression().fit(x, y)
    slopes[keyword] = model.coef_[0]

sorted_keywords = sorted(slopes.keys(), key=lambda k: slopes[k], reverse=True)
averages_sorted = averages[sorted_keywords]
slopes_sorted = {k: slopes[k] for k in sorted_keywords}

# Bar plot
fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.bar(averages_sorted.index, averages_sorted.values, color='skyblue', alpha=0.8)
for bar, keyword in zip(bars, averages_sorted.index):
    height = bar.get_height()
    slope = slopes_sorted[keyword]
    color = 'green' if slope > 0 else 'red'
    arrow = '↑' if slope > 0 else '↓'
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f"{arrow} {slope:.2f}", ha='center', va='bottom', fontsize=10, color=color)
ax.set_title(f'Average Interest ({TIMEFRAME}) with Growth Indicators')
ax.set_ylabel('Average Interest (%)')
ax.set_xlabel('Keywords')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(BAR_PLOT_PATH)
plt.show()
