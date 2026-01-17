"""
Air Quality Prediction Model
Machine Learning model for predicting Air Quality Index (AQI)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import warnings

warnings.filterwarnings('ignore')


class AirQualityModel:
    """
    Air Quality Prediction Model using Random Forest Regression
    """
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.feature_names = None

    def create_sample_dataset(self):
        """Generate synthetic air quality dataset for training"""
        print("\nCreating sample air quality dataset...")
        np.random.seed(42)
        n_samples = 1000

        # Generate synthetic air quality data
        data = {
            'temperature': np.random.uniform(0, 40, n_samples),  # Celsius
            'humidity': np.random.uniform(10, 90, n_samples),  # Percentage
            'pm25': np.random.uniform(0, 200, n_samples),  # PM2.5
            'pm10': np.random.uniform(0, 300, n_samples),  # PM10
            'no2': np.random.uniform(0, 150, n_samples),  # NO2
            'so2': np.random.uniform(0, 100, n_samples),  # SO2
            'co': np.random.uniform(0, 5, n_samples),  # CO
            'o3': np.random.uniform(0, 180, n_samples),  # O3
        }

        df = pd.DataFrame(data)

        # Calculate AQI based on pollutants (simplified formula)
        df['aqi'] = (
            df['pm25'] * 0.4 +
            df['pm10'] * 0.3 +
            df['no2'] * 0.1 +
            df['so2'] * 0.1 +
            df['co'] * 10 +
            df['o3'] * 0.1
        )

        # Add some noise
        df['aqi'] = df['aqi'] + np.random.normal(0, 5, n_samples)
        df['aqi'] = df['aqi'].clip(0, 500)

        return df

    def load_dataset_from_csv(self, csv_path):
        """Load dataset from CSV file"""
        print(f"\nLoading dataset from: {csv_path}")
        try:
            df = pd.read_csv(csv_path)
            print(f"✓ Dataset loaded: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"CSV file not found or error: {e}")
            print("Using sample dataset instead.")
            return self.create_sample_dataset()

    def train(self, df):
        """Train the model on provided dataset"""
        print("\n" + "=" * 60)
        print("TRAINING AIR QUALITY PREDICTION MODEL")
        print("=" * 60)

        X = df.drop('aqi', axis=1)
        y = df['aqi']
        self.feature_names = X.columns.tolist()

        print(f"\nDataset size: {len(df)}")
        print(f"Features: {len(X.columns)}")
        print(f"AQI Range: {y.min():.2f} - {y.max():.2f}")
        print(f"Mean AQI: {y.mean():.2f}")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print(f"\nTraining samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")

        print("\nScaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        print("Training Random Forest model...")
        self.model.fit(X_train_scaled, y_train)

        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print("\n" + "=" * 60)
        print("MODEL EVALUATION RESULTS")
        print("=" * 60)
        print(f"R² Score: {r2:.4f}")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"Mean Absolute Error: {mae:.4f}")
        print(f"RMSE: {np.sqrt(mse):.4f}")

        return r2

    def predict(self, features_dict):
        """Make AQI prediction based on input features"""
        try:
            features_df = pd.DataFrame([features_dict])[self.feature_names]
            features_scaled = self.scaler.transform(features_df)

            aqi_prediction = self.model.predict(features_scaled)[0]
            aqi_prediction = max(0, min(500, aqi_prediction))  # Clip to valid range

            # Determine air quality category
            if aqi_prediction <= 50:
                category = "GOOD"
                health_implication = "Air quality is satisfactory"
                color = "green"
            elif aqi_prediction <= 100:
                category = "MODERATE"
                health_implication = "Acceptable for most people"
                color = "yellow"
            elif aqi_prediction <= 150:
                category = "UNHEALTHY FOR SENSITIVE"
                health_implication = "Sensitive groups may experience health effects"
                color = "orange"
            elif aqi_prediction <= 200:
                category = "UNHEALTHY"
                health_implication = "Everyone may begin to experience health effects"
                color = "red"
            elif aqi_prediction <= 300:
                category = "VERY UNHEALTHY"
                health_implication = "Health alert: everyone may experience serious effects"
                color = "purple"
            else:
                category = "HAZARDOUS"
                health_implication = "Health warning of emergency conditions"
                color = "maroon"

            return {
                'aqi': round(aqi_prediction, 2),
                'category': category,
                'health_implication': health_implication,
                'color': color
            }
        except Exception as e:
            return {
                'error': str(e),
                'aqi': 0,
                'category': 'ERROR',
                'health_implication': 'Unable to calculate AQI',
                'color': 'gray'
            }

    def save_model(self, filepath='air_quality_model.pkl'):
        """Save trained model to file"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names
            }, f)
        print(f"\n✓ Model saved to {filepath}")

    def load_model(self, filepath='air_quality_model.pkl'):
        """Load trained model from file"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data['feature_names']
        print(f"✓ Model loaded from {filepath}")


def train_and_save_model(csv_path='AirIndex.csv', model_path='air_quality_model.pkl'):
    """Train model and save to disk"""
    air_quality_model = AirQualityModel()
    
    if csv_path:
        df = air_quality_model.load_dataset_from_csv(csv_path)
    else:
        df = air_quality_model.create_sample_dataset()
    
    air_quality_model.train(df)
    air_quality_model.save_model(model_path)
    
    return air_quality_model
