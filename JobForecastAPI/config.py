# config.py
import os

# Dataset and model paths
DATASET_PATH = 'D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/MODEL/filled_job_data_Ver1.csv'
MODEL_PATH = "D:/SANG/Do An Tot Nghiep/WEB-THAMKHAO/JOBINFOR/JobForecastAPI/MODEL/job_trend_forecasting_model_2015_2024-trend-apply-remove-residual-Ver3.keras"

# Flask configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000

# Data preprocessing constants
LOOK_BACK = 12  # Updated to match main script
ALPHA_DECAY_START = 0.5
ALPHA_DECAY_RATE = 0.01
NEUTRAL_MONTH = 6
NEUTRAL_QUARTER = 2

# Database configuration
HOST = 'localhost'
USER = 'root'
PASSWORD = 'tansangdut'
PORT = 3306
DATABASE = 'railway'