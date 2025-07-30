# model_handler.py
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from config import LOOK_BACK

class ModelHandler:
    def __init__(self, model_path, scaler, data, job_city_columns):
        self.model = load_model(model_path)
        self.scaler = scaler
        self.data = data  # Pivoted and resampled DataFrame
        self.columns = job_city_columns  # Index/column names for reference

    def predict_future(self, city_name, job_name, start_date, steps=36):
        job_city_name = f"{job_name.strip().upper()}_{city_name.strip()}"

        if job_city_name not in self.columns:
            raise ValueError(f"Job '{job_city_name}' not found in training data!")

        start_date = pd.to_datetime(start_date)
        last_historical_date = self.data.index[-1]

        data_numerical = self.data.copy()
        data_scaled = self.scaler.transform(data_numerical)

        if start_date > last_historical_date:
            print("\n[Mode] Future prediction only (no historical overlap)")

            current_window = data_scaled[-LOOK_BACK:].copy()

            months_to_predict = (start_date.year - last_historical_date.year) * 12 + \
                                (start_date.month - last_historical_date.month)

            if months_to_predict > 0:
                print(f"Bridging from {last_historical_date.strftime('%Y-%m')} to {start_date.strftime('%Y-%m')}...")
                for _ in range(months_to_predict):
                    pred = self.model.predict(current_window.reshape(1, LOOK_BACK, -1), verbose=0)[0]
                    current_window = np.vstack([current_window[1:], pred])

            future_predictions = []
            for _ in range(steps):
                pred = self.model.predict(current_window.reshape(1, LOOK_BACK, -1), verbose=0)[0]
                denorm_pred = self.scaler.inverse_transform(pred.reshape(1, -1))
                future_predictions.append(denorm_pred[0][list(self.columns).index(job_city_name)])
                current_window = np.vstack([current_window[1:], pred])

            return future_predictions

        else:
            print("\n[Mode] Historical-aware prediction (with actual data)")

            predictions = []
            dates = []
            for i in range(LOOK_BACK, len(data_scaled)):
                X_input = data_scaled[i - LOOK_BACK:i].reshape(1, LOOK_BACK, len(self.columns))
                pred = self.model.predict(X_input, verbose=0)[0]
                denorm_pred = self.scaler.inverse_transform(pred.reshape(1, -1))
                predictions.append(denorm_pred[0][list(self.columns).index(job_city_name)])
                dates.append(self.data.index[i])

            # Align start date to closest available index
            start_date_idx = self.data.index.get_indexer([start_date], method='nearest')[0]
            aligned_start_date = self.data.index[start_date_idx]

            filtered = [(date, pred) for date, pred in zip(dates, predictions) if date >= aligned_start_date]
            filtered_predictions = [p for _, p in filtered][:steps]

            remaining_steps = steps - len(filtered_predictions)
            future_predictions = []

            if remaining_steps > 0:
                last_known_index = len(data_scaled) - LOOK_BACK
                X_input = data_scaled[last_known_index:last_known_index + LOOK_BACK].reshape(1, LOOK_BACK, len(self.columns))

                for _ in range(remaining_steps):
                    pred = self.model.predict(X_input, verbose=0)[0]
                    denorm_pred = self.scaler.inverse_transform(pred.reshape(1, -1))
                    future_predictions.append(denorm_pred[0][list(self.columns).index(job_city_name)])
                    X_input = np.vstack([X_input[0, 1:], pred]).reshape(1, LOOK_BACK, len(self.columns))

            return filtered_predictions + future_predictions
