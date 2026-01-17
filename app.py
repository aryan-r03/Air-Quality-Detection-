"""
Air Quality Prediction Flask Application
Main application entry point
"""

from flask import Flask
from flask_cors import CORS
import os

from models import AirQualityModel, train_and_save_model
from routes import api_bp, main_bp, init_routes
from config import config


def create_app(config_name='development'):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app)
    
    # Initialize or load the model
    model_path = app.config['MODEL_PATH']
    csv_file = app.config['CSV_FILE']
    
    print("\n" + "=" * 60)
    print("INITIALIZING AIR QUALITY PREDICTION SYSTEM")
    print("=" * 60)
    
    if os.path.exists(model_path):
        print(f"\nLoading existing model from {model_path}...")
        air_quality_analyzer = AirQualityModel()
        air_quality_analyzer.load_model(model_path)
    else:
        print("\nNo existing model found. Training new model...")
        csv_path = csv_file if os.path.exists(csv_file) else None
        air_quality_analyzer = train_and_save_model(
            csv_path=csv_path,
            model_path=model_path
        )
    
    # Initialize routes with the model
    init_routes(air_quality_analyzer)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    print("\n✓ Application initialized successfully!")
    print("=" * 60 + "\n")
    
    return app


def main():
    """
    Main function to run the application
    """
    # Get configuration from environment or use default
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    # Create app
    app = create_app(config_name)
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    print("=" * 60)
    print(f"Starting Flask server on port {port}...")
    print(f"Open your browser: http://127.0.0.1:{port}")
    print("=" * 60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )


if __name__ == '__main__':
    main()
