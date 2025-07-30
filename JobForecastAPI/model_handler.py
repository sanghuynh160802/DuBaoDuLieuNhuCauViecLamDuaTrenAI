# model_handler.py
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from config import LOOK_BACK, ALPHA_DECAY_START, ALPHA_DECAY_RATE, NEUTRAL_MONTH, NEUTRAL_QUARTER

class ModelHandler:
    def __init__(self, model_path, scaler, data_scaled, time_feats, job_city_columns, time_index):
        self.model = load_model(model_path)
        self.scaler = scaler
        self.data_scaled = data_scaled
        self.time_feats = time_feats
        self.columns = job_city_columns
        self.time_index = time_index

    def generate_blended_features(self, dates, alpha=ALPHA_DECAY_START):
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

    def predict_future(self, city_name, job_name, start_date, steps=36, add_noise=True):
        job_city_name = f"{job_name.strip().upper()}_{city_name.strip()}"

        if job_city_name not in self.columns:
            raise ValueError(f"Job '{job_city_name}' not found in training data!")

        start_date = pd.to_datetime(start_date)
        last_historical_date = self.time_index[-1]
        job_idx = self.columns.get_loc(job_city_name)

        data_arr = self.data_scaled.values
        time_feats = self.time_feats

        def forecast(current_window, future_feats, step_count):
            preds = []
            for i in range(step_count):
                pred = self.model.predict(current_window, verbose=0)[0]
                if add_noise:
                    pred += np.random.normal(0, 0.005, pred.shape)

                denorm = self.scaler.inverse_transform(pred.reshape(1, -1))
                value = max(denorm[0, job_idx], 0)
                if value == 0:
                    value = np.random.uniform(3, 7)
                preds.append(value)

                pred[job_idx] = 0.7 * pred[job_idx] + 0.3 * current_window[0, -1, job_idx]
                next_input = np.concatenate([pred, future_feats[i]])
                current_window = np.vstack([current_window[0][1:], next_input]).reshape(1, LOOK_BACK, -1)
            return preds

        if start_date > last_historical_date:
            print("\n[Mode] Future prediction only (no historical overlap)")

            months_to_gap = (start_date.year - last_historical_date.year) * 12 + (start_date.month - last_historical_date.month)
            pre_forecast_dates = pd.date_range(start=last_historical_date + pd.DateOffset(months=1), periods=months_to_gap, freq='ME')
            future_dates = pd.date_range(start=start_date, periods=steps, freq='ME')

            current_window = np.concatenate([data_arr[-LOOK_BACK:], time_feats[-LOOK_BACK:]], axis=1).reshape(1, LOOK_BACK, -1)

            for dt in pre_forecast_dates:
                neutral_feat = self.generate_blended_features([dt])[0]
                pred = self.model.predict(current_window, verbose=0)[0]
                current_window = np.vstack([current_window[0][1:], np.concatenate([pred, neutral_feat])]).reshape(1, LOOK_BACK, -1)

            future_feats = self.generate_blended_features(future_dates)
            return forecast(current_window, future_feats, steps)

        else:
            print("\n[Mode] Historical-aware prediction (with actual data)")

            preds, actuals, dates = [], [], []
            for i in range(LOOK_BACK, len(data_arr) + 1):  # +1 to include last point
                x = np.concatenate([data_arr[i - LOOK_BACK:i], time_feats[i - LOOK_BACK:i]], axis=1).reshape(1, LOOK_BACK, -1)
                pred = self.model.predict(x, verbose=0)[0]
                denorm = self.scaler.inverse_transform(pred.reshape(1, -1))
                preds.append(denorm[0, job_idx])
                actual_val = self.scaler.inverse_transform(data_arr[i - 1].reshape(1, -1))[0, job_idx]
                actuals.append(actual_val)
                dates.append(self.time_index[i - 1])

            historical = [(d, p, a) for d, p, a in zip(dates, preds, actuals) if d >= start_date]
            hist_dates = [d for d, _, _ in historical]
            hist_preds = [p for _, p, _ in historical]

            if len(hist_preds) > steps:
                hist_preds = hist_preds[:steps]
                hist_dates = hist_dates[:steps]

            remaining = steps - len(hist_preds)
            if remaining > 0:
                last_hist_date = hist_dates[-1]
                current_window = np.concatenate([data_arr[-LOOK_BACK:], time_feats[-LOOK_BACK:]], axis=1).reshape(1, LOOK_BACK, -1)
                future_dates = pd.date_range(start=last_hist_date + pd.DateOffset(months=1), periods=remaining, freq='ME')
                future_feats = self.generate_blended_features(future_dates)
                future_forecast = forecast(current_window, future_feats, remaining)
                hist_preds += future_forecast

            return hist_preds
