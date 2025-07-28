from flask import json, jsonify, request
from app import app
from app import db
from app.models import Menu
from app.utils import format_response, get_current_timestamp, validate_input
from app.config import Config
from app.services import UserService, DataService, SecurityService, AnalyticsService

# Initialize services
user_service = UserService()
data_service = DataService()
security_service = SecurityService()
analytics_service = AnalyticsService()

@app.route('/')
def home():
	return jsonify({ "status": "ok" })

@app.route('/menu')
def menu():
    today = Menu.query.first()
    if today:
        body = { "today_special": today.name }
        status = 200
    else:
        body = { "error": "Sorry, the service is not available today." }
        status = 404
    return jsonify(body), status

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "service": "third-party-integration-demo"
    })

@app.route('/test-integration')
def test_integration():
    """Test endpoint for SonarCloud integration"""
    return jsonify({
        "message": "SonarCloud integration test successful!",
        "timestamp": "2024-01-15",
        "branch": "feature/test-integration"
    })

@app.route('/utils-test')
def utils_test():
    """Test endpoint for utils functions"""
    test_data = {"test": "data", "number": 42}
    formatted_response = format_response(test_data)
    return jsonify(formatted_response)

@app.route('/api/v1/data', methods=['GET', 'POST'])
def handle_data():
    """API endpoint for data handling with validation"""
    if request.method == 'GET':
        return jsonify({
            "message": "Data endpoint working",
            "method": "GET",
            "timestamp": get_current_timestamp()
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        if not validate_input(data):
            return jsonify({"error": "Invalid input data"}), 400
        
        return jsonify(format_response(data, "created"))

@app.route('/metrics')
def get_metrics():
    """Metrics endpoint for monitoring"""
    return jsonify({
        "uptime": "100%",
        "response_time": "50ms",
        "requests_per_second": 10,
        "error_rate": "0.1%"
    })

@app.route('/config')
def get_config():
    """Configuration endpoint for SonarCloud integration"""
    return jsonify({
        "api_info": Config.get_api_info(),
        "sonar_config": Config.get_sonar_config(),
        "environment": app.config.get('ENV', 'development')
    })

# New service-based endpoints
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({"error": "Username and email are required"}), 400
        
        user = user_service.create_user(data['username'], data['email'])
        return jsonify(format_response(user, "user_created")), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    data = request.get_json()
    user = user_service.update_user(user_id, **data)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    success = user_service.delete_user(user_id)
    if not success:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})

@app.route('/api/v1/process', methods=['POST'])
def process_data():
    """Process data using DataService"""
    data = request.get_json()
    if not validate_input(data):
        return jsonify({"error": "Invalid input data"}), 400
    
    processed = data_service.process_data(data)
    return jsonify(processed)

@app.route('/api/v1/security/password', methods=['POST'])
def generate_password():
    """Generate secure password"""
    data = request.get_json()
    length = data.get('length', 12) if data else 12
    
    password = security_service.generate_password(length)
    hashed = security_service.hash_password(password)
    
    return jsonify({
        "password": password,
        "hashed": hashed,
        "length": length
    })

@app.route('/api/v1/security/verify', methods=['POST'])
def verify_password():
    """Verify password"""
    data = request.get_json()
    if not data or 'password' not in data or 'hashed' not in data:
        return jsonify({"error": "Password and hash are required"}), 400
    
    is_valid = security_service.verify_password(data['password'], data['hashed'])
    return jsonify({"valid": is_valid})

@app.route('/api/v1/analytics', methods=['GET'])
def get_analytics():
    """Get analytics metrics"""
    metrics = analytics_service.get_metrics()
    return jsonify(metrics)

@app.route('/api/v1/analytics/reset', methods=['POST'])
def reset_analytics():
    """Reset analytics metrics"""
    old_metrics = analytics_service.reset_metrics()
    return jsonify({
        "message": "Analytics reset successfully",
        "previous_metrics": old_metrics
    })