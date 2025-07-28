"""
Utility functions for the application
"""
import datetime
import json
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.datetime.now().isoformat()


def format_response(data: Dict[str, Any], status: str = "success") -> Dict[str, Any]:
    """Format API response"""
    return {
        "status": status,
        "data": data,
        "timestamp": get_current_timestamp()
    }


def validate_input(data: Dict[str, Any]) -> bool:
    """Validate input data"""
    if not isinstance(data, dict):
        return False
    return True


def calculate_coverage(test_results: Dict[str, Any]) -> float:
    """Calculate test coverage percentage"""
    if not test_results or 'total' not in test_results:
        return 0.0
    
    total = test_results['total']
    passed = test_results.get('passed', 0)
    
    if total == 0:
        return 0.0
    
    return (passed / total) * 100


def sanitize_string(input_string: str) -> str:
    """Sanitize input string"""
    if not isinstance(input_string, str):
        return ""
    return input_string.strip()


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def log_operation(operation: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Log operation for monitoring"""
    log_data = {
        "operation": operation,
        "timestamp": get_current_timestamp(),
        "details": details or {}
    }
    logger.info(f"Operation logged: {json.dumps(log_data)}")


def generate_id() -> str:
    """Generate unique ID"""
    import uuid
    return str(uuid.uuid4()) 