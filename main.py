import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

"""
Step 1: Import and prepare the data
"""

#Set 'Apple Health Export Data' folder as wd
#Copy FoI 'Glucose Data.csv' into wd
# Parse Apple Health Export Data folder:
#see https://github.com/markwk/qs_ledger/tree/218e9d8abd52135f8c1de797a8ec390621bf6bc2/apple_health
%run -i 'apple-health-data-parser' 'export.xml' 

# Load the CGM data
glucose_data = 'Glucose Data.csv'
df = pd.read_csv(glucose_data)

# Convert the 'Reading date' to a datetime object
df['Timestamp'] = pd.to_datetime(df['Reading date'])

# Filter out non-physiological blood sugar values (< 5 mg/dL)
df = df[df['Measurement (mg/dL)'] >= 5]

""" Code snippet to convert mg/dL to mmol/L (Toggle on/off as needed)
#Conversion factor: 1 mg/dL = 0.0555 mmol/L
df['BloodSugar_mmol_L'] = df['Measurement (mg/dL)'] * 0.0555
"""

"""
Step 2: Visualise the CGM data
"""

# Data over time (scatter/line chart)
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Measurement (mg/dL)'], marker='o', linestyle='-', color='blue')
plt.title('Blood Sugar Levels Over Time')
plt.xlabel('Date')
plt.ylabel('Blood Sugar (mg/dL)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Average data per week (bar chart)
df['Week'] = df['Timestamp'].dt.isocalendar().week
weekly_avg = df.groupby('Week')['Measurement (mg/dL)'].mean()
plt.figure(figsize=(12, 6))
sns.barplot(x=weekly_avg.index, y=weekly_avg.values, color='green')
plt.title('Average Blood Sugar per Week')
plt.xlabel('Week of the Year')
plt.ylabel('Average Blood Sugar (mg/dL)')
plt.show()

# Average data per day of the week (bar chart)
df['DayOfWeek'] = df['Timestamp'].dt.day_name()
dayofweek_avg = df.groupby('DayOfWeek')['Measurement (mg/dL)'].mean()
plt.figure(figsize=(12, 6))
sns.barplot(x=dayofweek_avg.index, y=dayofweek_avg.values, color='orange')
plt.title('Average Blood Sugar per Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Average Blood Sugar (mg/dL)')
plt.show()

# Average data per hour of the day (bar chart)
df['HourOfDay'] = df['Timestamp'].dt.hour
hourofday_avg = df.groupby('HourOfDay')['Measurement (mg/dL)'].mean()
plt.figure(figsize=(12, 6))
sns.barplot(x=hourofday_avg.index, y=hourofday_avg.values, color='purple')
plt.title('Average Blood Sugar per Hour of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Blood Sugar (mg/dL)')
plt.show()

"""
Step 3: Match the Events data [for demonstration purposes I will use Workout events]
"""
# Create a set of dates when workouts occurred
workout_dates = set(workout_df_filtered['startDate'].dt.date)

# Assign colors based on workout days
colors = ['green' if timestamp.date() in workout_dates else 'blue' for timestamp in df['Timestamp']]

plt.figure(figsize=(12, 6))

# Plotting blood sugar levels with color coding
plt.scatter(df['Timestamp'], df['Measurement (mg/dL)'], c=colors)

# Adding legends for color coding
plt.scatter([], [], color='blue', label='No Workout')
plt.scatter([], [], color='green', label='Workout Day')

# Plotting workout start and end times
plt.scatter(workout_df_filtered['startDate'], [1] * len(workout_df_filtered), color='red', label='Workout Start')
plt.scatter(workout_df_filtered['endDate'], [1] * len(workout_df_filtered), color='green', label='Workout End')

plt.title('Blood Sugar Levels and Workout Events Over Time')
plt.xlabel('Date')
plt.ylabel('Blood Sugar (mg/dL)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

"""
Step 4: Split CGM data by workout vs non-workout periods 
"""

# Calculating average blood glucose during workout events
avg_glucose_during_workout = []
for _, row in workout_df_filtered.iterrows():
    glucose_during_workout = df[(df['Timestamp'] >= row['startDate']) & (df['Timestamp'] <= row['endDate'])]
    avg_glucose = glucose_during_workout['Measurement (mg/dL)'].mean()
    if not pd.isna(avg_glucose):
        avg_glucose_during_workout.append(avg_glucose)

average_glucose_during_workouts = np.mean(avg_glucose_during_workout) if avg_glucose_during_workout else None

# Filtering out the times of workouts from the CGM data
non_workout_times = ~df['Timestamp'].isin(workout_df_filtered['startDate']) & ~df['Timestamp'].isin(workout_df_filtered['endDate'])

# Calculating average blood glucose outside of workout events (10am to 8pm)
df['Hour'] = df['Timestamp'].dt.hour
avg_glucose_outside_workout = df[(df['Hour'] >= 6) & (df['Hour'] <= 22) & non_workout_times]['Measurement (mg/dL)'].mean()

"""
Step 5: Comparison with TOD and DOW matched readings
"""
# Add day of the week to df
df['DayOfWeek'] = df['Timestamp'].dt.dayofweek

# Add day of the week and hour of the day to workout_df_filtered
workout_df_filtered['DayOfWeek'] = workout_df_filtered['startDate'].dt.dayofweek
workout_df_filtered['Hour'] = workout_df_filtered['startDate'].dt.hour

# Collecting matched non-workout readings
matched_non_workout_readings = pd.DataFrame()

for _, workout in workout_df_filtered.iterrows():
    matching_times = df[(df['DayOfWeek'] == workout['DayOfWeek']) & 
                        (df['HourOfDay'] == workout['Hour']) & 
                        ~df['Timestamp'].between(workout['startDate'], workout['endDate'])]
    matched_non_workout_readings = matched_non_workout_readings.append(matching_times)

# Calculate average glucose levels for matched non-workout periods
average_glucose_matched_non_workout = matched_non_workout_readings['Measurement (mg/dL)'].mean()

# Print the average glucose levels
print("Average Glucose During Workouts:", average_glucose_during_workouts)

# Collecting all glucose readings during matched non-workout periods
glucose_matched_non_workout_readings = matched_non_workout_readings['Measurement (mg/dL)']

# Calculate average glucose level during matched non-workout periods
average_glucose_matched_non_workout = np.mean(glucose_matched_non_workout_readings)
print("Average Glucose During Matched Non-Workout Periods:", average_glucose_matched_non_workout)

# Perform the t-test
t_stat, p_value = stats.ttest_ind(glucose_during_workout_readings, glucose_matched_non_workout_readings, equal_var=False)
print("T-test results -- T-Statistic:", t_stat, "P-value:", p_value)

# Plot the results
means = [np.mean(glucose_during_workout_readings), average_glucose_matched_non_workout]
std_devs = [np.std(glucose_during_workout_readings, ddof=1), np.std(glucose_matched_non_workout_readings, ddof=1)]

plt.bar(['During Workouts', 'Matched Non-Workout Periods'], means, yerr=std_devs, capsize=10)
plt.ylabel('Average Blood Glucose (mg/dL)')
plt.title('Blood Glucose Levels: Workouts vs Matched Non-Workout Periods')
plt.show()

""" This is the code to convert csv format ECG labels to text list #add after Step 2 and modify 'events' in step 3-5
path_ecg = 'electrocardiograms'

# Get all csv files in the folder
files = [f for f in os.listdir(path_ecg) if os.path.isfile(os.path.join(path_ecg, f)) and f.endswith('.csv')]

# Pull the data from first 8 rows and the filename into a DataFrame
dfs = []
for f in files:
    df = pd.read_csv(os.path.join(path_ecg, f), nrows=8, header=None, index_col=0, encoding='ISO-8859-1')
    df = df.transpose()  # Transpose the dataframe
    df['Filename'] = f  # Add filename column to each dataframe
    dfs.append(df)

output = pd.concat(dfs)

# Only keep the first 9 columns
output = output.iloc[:, :9]

# Set the header names
output.columns = ['Name', 'Date of Birth', 'Recorded Date', 'Classification', 'Symptoms', 'Software Version', 'Device', 'Sample Rate', 'Filename']

# Convert the Recorded Date column to datetime format
output['Recorded Date'] = pd.to_datetime(output['Recorded Date'])

output['Category'] = ''

# Sorting the dataframe by 'Recorded Date'
output = output.sort_values(by='Recorded Date')
"""
