from flask import json, jsonify
from app import app
from app import db
from app.models import Menu
from app.utils import format_response, get_current_timestamp

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