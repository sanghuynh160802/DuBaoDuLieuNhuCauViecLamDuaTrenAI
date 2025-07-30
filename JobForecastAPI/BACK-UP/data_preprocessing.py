# data_preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_and_preprocess_data(file_path):
    # Load dataset
    data = pd.read_csv(file_path)

    # Convert 'time' to datetime format
    data['time'] = pd.to_datetime(data['time'])

    # Clean and preprocess 'city' and 'job'
    data['city'] = data['city'].astype(str).str.strip()
    data['job'] = data['job'].astype(str).str.strip().str.upper()
    data['job_city'] = data['job'] + '_' + data['city']

    # Extract unique cities (before filtering to top jobs)
    unique_cities = data['city'].unique().tolist()

    # Identify top 10 jobs by total job_counting
    job_counts = data.groupby('job')['job_counting'].sum().nlargest(10)
    top_jobs = job_counts.index.tolist()
    data = data[data['job'].isin(top_jobs)].copy()

    # Pivot the table to get job_counting of all job-city combinations
    data_numerical = data.pivot_table(index='time', columns='job_city', values='job_counting', aggfunc='sum', fill_value=0)

    # Resample job_counting to monthly frequency
    data_numerical = data_numerical.resample('ME').sum().fillna(0)

    # Normalize using MinMaxScaler (fitted on full dataset)
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data_numerical)

    return data_numerical, data_scaled, scaler, job_counts, top_jobs, unique_cities

def create_lookback_dataset(data_scaled, look_back=12):
    X, y = [], []
    for i in range(look_back, len(data_scaled)):
        X.append(data_scaled[i - look_back:i])
        y.append(data_scaled[i])
    return np.array(X), np.array(y)
