"""
API Routes for Air Quality Prediction
"""

from flask import Blueprint, request, jsonify, render_template

# Create Blueprint
api_bp = Blueprint('api', __name__)
main_bp = Blueprint('main', __name__)

# This will be set by the app
air_quality_analyzer = None


def init_routes(analyzer):
    """Initialize routes with the trained model"""
    global air_quality_analyzer
    air_quality_analyzer = analyzer


@main_bp.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')


@api_bp.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint for air quality prediction
    Expects JSON with 'features' containing all required measurements
    """
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({
                'success': False,
                'error': 'No features provided'
            }), 400
        
        features = data['features']
        
        # Validate required features
        required_features = ['temperature', 'humidity', 'pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
        missing_features = [f for f in required_features if f not in features]
        
        if missing_features:
            return jsonify({
                'success': False,
                'error': f'Missing features: {", ".join(missing_features)}'
            }), 400
        
        # Make prediction
        result = air_quality_analyzer.predict(features)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': air_quality_analyzer is not None
    })
