"""
Business logic services for the application
"""
import hashlib
import secrets
import string
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json


class UserService:
    """Service for user management"""
    
    def __init__(self):
        self.users = {}
    
    def create_user(self, username: str, email: str) -> Dict[str, Any]:
        """Create a new user"""
        if not username or not email:
            raise ValueError("Username and email are required")
        
        user_id = self._generate_user_id()
        user = {
            'id': user_id,
            'username': username,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def update_user(self, user_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Update user information"""
        if user_id not in self.users:
            return None
        
        self.users[user_id].update(kwargs)
        self.users[user_id]['updated_at'] = datetime.now().isoformat()
        return self.users[user_id]
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def _generate_user_id(self) -> str:
        """Generate unique user ID"""
        return hashlib.md5(f"{datetime.now()}{secrets.token_hex(8)}".encode()).hexdigest()[:8]


class DataService:
    """Service for data processing"""
    
    def __init__(self):
        self.cache = {}
    
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data"""
        processed = {
            'original': data,
            'processed_at': datetime.now().isoformat(),
            'checksum': self._calculate_checksum(data),
            'size': len(json.dumps(data)),
            'fields_count': len(data.keys())
        }
        
        # Cache the result
        cache_key = self._calculate_checksum(data)
        self.cache[cache_key] = processed
        
        return processed
    
    def get_cached_data(self, checksum: str) -> Optional[Dict[str, Any]]:
        """Get cached data by checksum"""
        return self.cache.get(checksum)
    
    def clear_cache(self) -> int:
        """Clear cache and return number of cleared items"""
        count = len(self.cache)
        self.cache.clear()
        return count
    
    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate checksum for data"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()


class SecurityService:
    """Service for security operations"""
    
    @staticmethod
    def generate_password(length: int = 12) -> str:
        """Generate secure password"""
        # Ensure at least one character from each category
        password = []
        password.append(secrets.choice(string.ascii_uppercase))  # At least one uppercase
        password.append(secrets.choice(string.ascii_lowercase))  # At least one lowercase
        password.append(secrets.choice(string.digits))           # At least one digit
        password.append(secrets.choice("!@#$%^&*"))             # At least one special char
        
        # Fill the rest with random characters
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        for _ in range(length - 4):
            password.append(secrets.choice(alphabet))
        
        # Shuffle the password
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        return ''.join(password_list)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256()
        hash_obj.update((password + salt).encode())
        return f"{salt}${hash_obj.hexdigest()}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_value = hashed.split('$', 1)
            hash_obj = hashlib.sha256()
            hash_obj.update((password + salt).encode())
            return hash_obj.hexdigest() == hash_value
        except ValueError:
            return False
    
    @staticmethod
    def generate_token() -> str:
        """Generate secure token"""
        return secrets.token_urlsafe(32)


class AnalyticsService:
    """Service for analytics and metrics"""
    
    def __init__(self):
        self.metrics = {
            'requests': 0,
            'errors': 0,
            'start_time': datetime.now().isoformat()
        }
    
    def record_request(self, endpoint: str, status_code: int) -> None:
        """Record API request"""
        self.metrics['requests'] += 1
        if status_code >= 400:
            self.metrics['errors'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        uptime = datetime.now() - datetime.fromisoformat(self.metrics['start_time'])
        return {
            **self.metrics,
            'uptime_seconds': int(uptime.total_seconds()),
            'error_rate': (self.metrics['errors'] / max(self.metrics['requests'], 1)) * 100
        }
    
    def reset_metrics(self) -> Dict[str, Any]:
        """Reset metrics and return previous values"""
        old_metrics = self.metrics.copy()
        self.metrics = {
            'requests': 0,
            'errors': 0,
            'start_time': datetime.now().isoformat()
        }
        return old_metrics 