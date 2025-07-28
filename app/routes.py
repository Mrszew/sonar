from flask import json, jsonify, request
from app import app
from app import db
from app.models import Menu
from app.utils import format_response, get_current_timestamp, validate_input
from app.config import Config

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