# GluAPI
Integrate Continuous Glucose Monitoring data (Abbott Lingo) with Wearable-recorded events (Apple Watch Atrial Fibrillation ECGs or Workouts)

**Continuous Glucose Monitoring and Apple Health Data Integration
**This repository contains a Python script designed to integrate and analyze continuous glucose monitoring (CGM) data derived from an Abbott Lingo device (but should be compatible with the output .csv from a Freestyle Libre device) with Apple Health data.
Phase 2 visualizes glucose readings and can be run using the CGM data alone.
Phase 3-5 compare glucose levels during Apple Watch derived events (I have chosen Workout events for this but have provided the snippets to use ECG-level labels to be able to compare rhythm-level labelss with matched periods)

**Features in more detail
**Phase 2. Visualize CGM Data
This section is independent of Apple Health data and is applicable to any Abbott Lingo user.
Visualizes glucose recordings over time.
Averages glucose readings by time of day and day of week.

2. Combine CGM and Apple Health Data
Integrates CGM data with workout records from Apple Health.
Compares glucose levels during recorded workouts with matched time periods (same time of day and day of week) to identify significant differences.
Uses statistical tests to validate the findings.

4. Prepare Apple Watch ECG Data
Converts Apple Watch ECG data labels to a text format.
Sets the foundation for future iterations of the script to compare blood sugar readings during periods of sinus rhythm versus atrial fibrillation.

**Getting Started**
Clone the Repository:

Clone this repository to your local machine using git clone.
Set Up Your Working Environment:

Place the script in a folder containing the relevant CGM and Apple Health export data.

**Required Data:
** -Abbott Lingo CGM data in CSV format.
- Apple Health data exported as XML and workout data in CSV format.
- Apple Watch ECG data in CSV format.

**Running the Script:
**
Run the script in a Python environment with the necessary libraries (pandas, matplotlib, seaborn, etc.).
Ensure the paths to data files are correctly set within the script.
Visualization and Analysis:

The script outputs several plots visualizing the CGM data.
It provides statistical analysis of glucose levels during workouts versus matched non-workout periods.
ECG Data Conversion:

The script prepares ECG data labels for future analyses.
**Requirements
**- Python 3.x
- Libraries: pandas, matplotlib, seaborn, numpy
- CGM data from Abbott Lingo (CSV format)
- Apple Health data (XML and CSV formats)

**Future Work
**Integrate analysis of ECG data to correlate cardiac rhythms with glucose levels.
