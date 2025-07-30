# data_preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.seasonal import STL
from config import ALPHA_DECAY_START, ALPHA_DECAY_RATE, NEUTRAL_MONTH, NEUTRAL_QUARTER

# === Constants === #
LOOKBACK = 12
TOP_K_JOBS = 10

def generate_blended_features(dates, alpha=ALPHA_DECAY_START):
    neutral = np.array([
        np.sin(2 * np.pi * NEUTRAL_MONTH / 12),
        np.cos(2 * np.pi * NEUTRAL_MONTH / 12),
        np.sin(2 * np.pi * NEUTRAL_QUARTER / 4),
        np.cos(2 * np.pi * NEUTRAL_QUARTER / 4)
    ])
    features = []
    for i, date in enumerate(dates):
        month, quarter = date.month, (date.month - 1) // 3 + 1
        dynamic = np.array([
            np.sin(2 * np.pi * month / 12),
            np.cos(2 * np.pi * month / 12),
            np.sin(2 * np.pi * quarter / 4),
            np.cos(2 * np.pi * quarter / 4)
        ])
        decay_alpha = max(0.2, alpha - i * ALPHA_DECAY_RATE)
        features.append(decay_alpha * dynamic + (1 - decay_alpha) * neutral)
    return np.array(features)

# === Updated Preprocessing Function === #
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['time'] = pd.to_datetime(df['time'])
    df['city'] = df['city'].astype(str).str.strip()
    df['job'] = df['job'].astype(str).str.strip().str.upper()
    df['job_city'] = df['job'] + '_' + df['city']

    unique_cities = df['city'].unique().tolist()

    job_counts = df.groupby('job')['job_counting'].sum().nlargest(TOP_K_JOBS)
    top_jobs = job_counts.index.tolist()
    df = df[df['job'].isin(top_jobs)].copy()

    pivot = df.pivot_table(index='time', columns='job_city', values='job_counting', aggfunc='sum')
    data_raw = pivot.resample('ME').sum().fillna(0)

    # STL decomposition
    trend, seasonal = {}, {}
    for col in data_raw.columns:
        result = STL(data_raw[col], period=12, robust=True).fit()
        trend[col], seasonal[col] = result.trend, result.seasonal
    trend_df = pd.DataFrame(trend)
    seasonal_df = pd.DataFrame(seasonal)

    # Combine trend + seasonal
    data_combined = np.maximum(0, trend_df + seasonal_df)

    # Generate time features AFTER data_combined is ready
    time_feats = generate_blended_features(data_combined.index)

    # Normalize
    scaler = MinMaxScaler()
    data_scaled = pd.DataFrame(scaler.fit_transform(data_combined), columns=data_combined.columns, index=data_combined.index)

    return data_combined, data_scaled, time_feats, scaler, job_counts, top_jobs, unique_cities

# === Lookback Generator === #
def create_lookback_dataset(data_scaled, look_back=LOOKBACK):
    X, y = [], []
    for i in range(look_back, len(data_scaled)):
        X.append(data_scaled.iloc[i - look_back:i].values)
        y.append(data_scaled.iloc[i].values)
    return np.array(X), np.array(y)