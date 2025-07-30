import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from statsmodels.tsa.seasonal import STL
from flask import Flask, jsonify, request  # Import request to handle POST data
from flask_cors import CORS  # Import CORS
from tensorflow.keras.models import load_model  # Import load_model for loading the trained model

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load dataset
file_path = 'D:/SANG/Do An Tot Nghiep/dataset1/processed_job_data_human-readable_date.csv'
data = pd.read_csv(file_path)

# Convert 'time' to datetime format
data['time'] = pd.to_datetime(data['time'])

# Clean 'city' and 'job' columns
data['city'] = data['city'].astype(str).str.strip()
data['job'] = data['job'].astype(str).str.strip().str.upper()

# Debug: Check for NaN values in 'job' column before filtering
print(f"\n🔹 Initial NaN count in 'job' column: {data['job'].isna().sum()}")

# Drop NaN values in 'job'
data = data.dropna(subset=['job'])

# Identify top 20 jobs by total job_counting
job_counts = data.groupby('job')['job_counting'].sum().nlargest(20)
print("\n🔹 Top 20 Jobs by Job Counting:")
print(job_counts)

top_jobs = job_counts.index.tolist()
data = data[data['job'].isin(top_jobs)].copy()

# Extract unique cities BEFORE dropping the column
unique_cities = data['city'].unique().tolist()

# One-hot encode city
city_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
city_encoded = city_encoder.fit_transform(data[['city']])
city_encoded_df = pd.DataFrame(city_encoded, columns=city_encoder.get_feature_names_out(['city']))

data.drop(columns=['city'], inplace=True)
data = pd.concat([data, city_encoded_df], axis=1)

# One-hot encode job
job_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
job_encoded = job_encoder.fit_transform(data[['job']])
job_encoded_df = pd.DataFrame(job_encoded, columns=job_encoder.get_feature_names_out(['job']))

data.drop(columns=['job'], inplace=True)
data = pd.concat([data, job_encoded_df], axis=1)

data.set_index('time', inplace=True)

# Debug: Check if 'job_nan' column still exists
print("\n🔹 Checking for 'job_nan' column:")
print([col for col in data.columns if 'job_nan' in col])

# Resample job_counting
data_numerical = data[['job_counting']].resample('ME').sum().fillna(0)
data_categorical = data.drop(columns=['job_counting']).resample('ME').max().fillna(0)  # Fix applied here
data = pd.concat([data_numerical, data_categorical], axis=1)

# Debug: Check if 'job_BACKEND' and 'job_FRONTEND' exist
debug_jobs = ['job_BACKEND', 'job_FRONTEND']
print("\n🔹 Checking for missing jobs:")
for job in debug_jobs:
    print(f"{job} exists: {job in data.columns}")

# Apply STL Decomposition
stl = STL(data['job_counting'], seasonal=13)
result = stl.fit()
data['trend'] = result.trend
data['seasonal'] = result.seasonal
data['residual'] = result.resid

# Reorder columns
city_columns = [col for col in data.columns if col.startswith('city_')]
job_columns = [col for col in data.columns if col.startswith('job_')]
data = data[city_columns + job_columns + ['trend', 'seasonal', 'residual', 'job_counting']]

# Remove duplicate columns
data = data.loc[:, ~data.columns.duplicated()]

# Data Augmentation with Stability
def augment_data(df, factor=30):
    augmented = []
    for _ in range(factor):
        noise = np.random.normal(0, df['job_counting'].std() * 0.015, df.shape[0])
        augmented_df = df.copy()
        augmented_df['job_counting'] += noise
        augmented_df['job_counting'] = np.maximum(0, augmented_df['job_counting'])
        augmented.append(augmented_df)
    return pd.concat(augmented).sort_index()

data = augment_data(data, 30)

# Create lagged features
look_back = 18
for lag in range(1, look_back + 1):
    data[f'lag_{lag}'] = data['job_counting'].shift(lag)

data.dropna(inplace=True)

# Normalize numerical features
num_cols = ['job_counting', 'trend', 'seasonal', 'residual'] + [f'lag_{i}' for i in range(1, look_back + 1)]

# Split data into training and testing sets
train_size = int(len(data) * 0.8)
train_data = data.iloc[:train_size].copy()
test_data = data.iloc[train_size:].copy()

# Fit MinMaxScaler ONLY on training data
scaler = MinMaxScaler()
scaler.fit(train_data[num_cols])  

# Transform train and test data separately
train_data[num_cols] = scaler.transform(train_data[num_cols])
test_data[num_cols] = scaler.transform(test_data[num_cols])

# Prepare data for LSTM
def create_dataset(data, look_back=18):
    X, Y = [], []
    for i in range(len(data) - look_back):
        X.append(data.iloc[i:i + look_back].values)
        Y.append(data.iloc[i + look_back]['job_counting'])
    return np.array(X, dtype=np.float32), np.array(Y, dtype=np.float32)

X_train, Y_train = create_dataset(train_data, look_back)
X_test, Y_test = create_dataset(test_data, look_back)

# Count the number of distinct job samples
job_columns = [col for col in data.columns if col.startswith('job_')]
distinct_job_samples = {col: (data[col] == 1.0).sum() for col in job_columns}

# Print results
print("\n🔹 Number of distinct samples for each job:")
for job, count in distinct_job_samples.items():
    print(f"{job}: {count}")

# Total number of distinct job samples
total_distinct_samples = sum(distinct_job_samples.values())
print(f"\n🔹 Total distinct job samples: {total_distinct_samples}")

# Load trained model
model_path = "D:/SANG/Do An Tot Nghiep/crawl-data/data/DATA PRE-PROCESSING/model/job_trend_forecasting_model.keras"
model = load_model(model_path)

# Prediction function
def predict_future(city_name, job_name, start_date, steps=12, add_noise=True):
    print(f"DEBUG: Inputs - City: {city_name}, Job: {job_name}, Start Date: {start_date}, Steps: {steps}")

    city_name = city_name.strip().lower()
    job_name = job_name.strip().upper()

    # Match city & job
    matched_city = next((c for c in city_encoder.categories_[0] if c.strip().lower() == city_name), None)
    matched_job = next((j for j in job_encoder.categories_[0] if j.strip().upper() == job_name), None)

    if matched_city is None or matched_job is None:
        print(f"Error: City '{city_name}' or Job '{job_name}' not found!")
        return

    print("DEBUG: One-hot encoding successful.")

    # Create one-hot vectors
    city_vector = np.zeros(len(city_encoder.categories_[0]))
    city_vector[np.where(city_encoder.categories_[0] == matched_city)[0][0]] = 1

    job_vector = np.zeros(len(job_encoder.categories_[0]))
    job_vector[np.where(job_encoder.categories_[0] == matched_job)[0][0]] = 1

    # Filter data for the given city & job
    job_city_filter = (data[f'city_{matched_city}'] == 1) & (data[f'job_{matched_job}'] == 1)
    filtered_data = data[job_city_filter].copy()

    if filtered_data.empty:
        print(f"Error: No historical data found for City '{city_name}' and Job '{job_name}'")
        return

    # Ensure unique timestamps
    filtered_data = filtered_data.groupby(level=0).first()

    # Convert start_date to datetime
    start_date = pd.to_datetime(start_date)

    # Find closest historical date before start_date
    filtered_data = filtered_data.sort_index()
    past_data = filtered_data.loc[:start_date]

    if past_data.empty:
        print(f"ERROR: No historical data available before {start_date}. Cannot predict!")
        return

    # Select the last 'look_back' months before start_date
    available_data = past_data.iloc[-look_back:].copy()

    # Fix Missing Data with Interpolation
    if available_data.shape[0] < look_back:
        print(f"DEBUG: Insufficient data ({available_data.shape[0]} rows), using interpolation.")
        available_data = available_data.resample('M').interpolate(method='linear').iloc[-look_back:]

    print(f"DEBUG: Using {available_data.shape[0]} months of historical data from {available_data.index[0]} to {available_data.index[-1]}")

    # Normalize historical data
    available_data[num_cols] = scaler.transform(available_data[num_cols])

    # Check if there is a gap between the last historical data and start_date
    last_historical_date = available_data.index[-1]
    if last_historical_date < start_date:
        print(f"DEBUG: Gap detected between {last_historical_date} and {start_date}. Predicting for the missing period.")

        missing_months = (start_date.year - last_historical_date.year) * 12 + (start_date.month - last_historical_date.month)
        missing_dates = pd.date_range(start=last_historical_date + pd.DateOffset(months=1), periods=missing_months, freq='M')
        missing_predictions = []

        batch_sizes = []
        while missing_months > 0:
            if missing_months >= 12:
                batch_sizes.append(12)
                missing_months -= 12
            elif missing_months >= 6:
                batch_sizes.append(6)
                missing_months -= 6
            elif missing_months >= 3:
                batch_sizes.append(3)
                missing_months -= 3
            else:
                batch_sizes.append(missing_months)
                missing_months = 0

        for batch in batch_sizes:
            for _ in range(batch):
                input_data = available_data.values
                input_data = np.expand_dims(input_data, axis=0)

                pred = model.predict(input_data, verbose=0)[0, 0]
                denormalized_pred = scaler.inverse_transform([[pred] + [0] * (len(num_cols) - 1)])[0, 0]

                if add_noise:
                    denormalized_pred += np.random.normal(0, 2)

                missing_predictions.append(denormalized_pred)
                available_data.iloc[:-1] = available_data.iloc[1:].values
                available_data.iloc[-1, 0] = pred

    predictions = []
    future_dates = pd.date_range(start=start_date, periods=steps, freq='M')
    for _ in range(steps):
        input_data = available_data.values
        input_data = np.expand_dims(input_data, axis=0)

        pred = model.predict(input_data, verbose=0)[0, 0]
        denormalized_pred = scaler.inverse_transform([[pred] + [0] * (len(num_cols) - 1)])[0, 0]

        if add_noise:
            denormalized_pred += np.random.normal(0, 2)

        predictions.append(denormalized_pred)
        available_data.iloc[:-1] = available_data.iloc[1:].values
        available_data.iloc[-1, 0] = pred

    return predictions

# Flask API to serve top 20 jobs data
@app.route('/api/top-jobs', methods=['GET'])
def get_top_jobs():
    top_jobs_data = job_counts.reset_index().to_dict(orient='records')
    return jsonify(top_jobs_data)

# Flask API to serve all unique cities
@app.route('/api/cities', methods=['GET'])
def get_cities():
    return jsonify(unique_cities)

# Flask API to handle prediction requests
@app.route('/api/predict', methods=['POST'])
def handle_predict():
    # Get the data from the request
    data = request.get_json()
    print("\n🔹 Received prediction data:")
    print(data)

    # Extract inputs from the request
    city_name = data.get('city')
    job_name = data.get('job')
    start_date = data.get('time')
    steps = data.get('step', 12)  # Default to 12 steps if not provided

    # Call the prediction function
    predictions = predict_future(city_name, job_name, start_date, steps=steps)

    # Print the predictions JSON
    response_data = {"message": "Prediction successful", "predictions": predictions}
    print("\n🔹 Prediction results JSON:")
    print(response_data)

    # Return the predictions
    return jsonify(response_data)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)