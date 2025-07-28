"""
Utility functions for the application
"""
import datetime
import json
from typing import Dict, Any


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