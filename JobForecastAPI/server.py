# server.py
from flask import Flask
from flask_cors import CORS
from config import DATASET_PATH, MODEL_PATH, FLASK_HOST, FLASK_PORT
from data_preprocessing import load_and_preprocess_data
from model_handler import ModelHandler
from api.routes import init_routes

app = Flask(__name__)
CORS(app)

# Load and preprocess data
data, data_scaled, time_feats, scaler, job_counts, unique_jobs, unique_cities = load_and_preprocess_data(DATASET_PATH)

# Load model and initialize handler
model_handler = ModelHandler(MODEL_PATH, scaler, data_scaled, time_feats, data.columns, data.index)

# Initialize routes
init_routes(app, model_handler, job_counts, unique_cities)

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT)
