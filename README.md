# Real-Time Weather Monitoring System

## Description
A real-time weather monitoring system that fetches weather data from the OpenWeatherMap API every 5 minutes, processes it, logs alerts when thresholds are breached, and generates daily weather summaries and visualizations.

## Features
- Fetches real-time weather data from OpenWeatherMap.
- Stores daily summaries (average, max, min temperatures) in a SQLite database.
- Triggers alerts when temperature exceeds 35°C.
- Generates visualizations of daily weather summaries.
- Scheduled to run every 5 minutes for weather data and generates daily reports at midnight.

## Setup Instructions

### 1. Clone the repository:
```bash
git clone <repo-link>


#Step 1: Setting up the environment
Install necessary libraries:
pip install requests schedule

Step 2: Fetching Weather Data from OpenWeatherMap API
You need to sign up for an OpenWeatherMap API key. Use this API key to get real-time weather data for the specified cities.

Step 3: Processing and Storing Data

Step 4: Handling Alerting Thresholds

Step 5: Scheduling the Data Retrieval

Step 6: Test Cases
1. API Connectivity

2. Data Processing

3. Temperature Conversion

4. Alerts

