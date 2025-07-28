"""
Configuration settings for the application
"""
import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SonarCloud integration settings
    SONAR_PROJECT_KEY = os.environ.get('SONAR_PROJECT_KEY', 'third-party-integration-demo')
    SONAR_ORGANIZATION = os.environ.get('SONAR_ORGANIZATION', 'mrszew')
    
    # API settings
    API_VERSION = '1.0.0'
    API_TITLE = 'Third Party Integration Demo API'
    API_DESCRIPTION = 'Demo API for testing SonarCloud integration'
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Security settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'false').lower() == 'true'
    
    @staticmethod
    def get_sonar_config() -> Dict[str, Any]:
        """Get SonarCloud configuration"""
        return {
            'project_key': Config.SONAR_PROJECT_KEY,
            'organization': Config.SONAR_ORGANIZATION,
            'version': Config.API_VERSION
        }
    
    @staticmethod
    def get_api_info() -> Dict[str, Any]:
        """Get API information"""
        return {
            'title': Config.API_TITLE,
            'version': Config.API_VERSION,
            'description': Config.API_DESCRIPTION
        }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
