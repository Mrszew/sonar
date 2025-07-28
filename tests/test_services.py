"""
Tests for business logic services
"""
import unittest
import json
from app.services import UserService, DataService, SecurityService, AnalyticsService


class TestUserService(unittest.TestCase):
    """Test UserService functionality"""
    
    def setUp(self):
        self.user_service = UserService()
    
    def test_create_user_success(self):
        """Test successful user creation"""
        user = self.user_service.create_user("testuser", "test@example.com")
        
        self.assertIn('id', user)
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['email'], "test@example.com")
        self.assertEqual(user['status'], "active")
        self.assertIn('created_at', user)
    
    def test_create_user_missing_data(self):
        """Test user creation with missing data"""
        with self.assertRaises(ValueError):
            self.user_service.create_user("", "test@example.com")
        
        with self.assertRaises(ValueError):
            self.user_service.create_user("testuser", "")
    
    def test_get_user_exists(self):
        """Test getting existing user"""
        created_user = self.user_service.create_user("testuser", "test@example.com")
        retrieved_user = self.user_service.get_user(created_user['id'])
        
        self.assertEqual(created_user, retrieved_user)
    
    def test_get_user_not_exists(self):
        """Test getting non-existing user"""
        user = self.user_service.get_user("nonexistent")
        self.assertIsNone(user)
    
    def test_update_user_success(self):
        """Test successful user update"""
        user = self.user_service.create_user("testuser", "test@example.com")
        updated_user = self.user_service.update_user(user['id'], username="newuser")
        
        self.assertEqual(updated_user['username'], "newuser")
        self.assertIn('updated_at', updated_user)
    
    def test_update_user_not_exists(self):
        """Test updating non-existing user"""
        result = self.user_service.update_user("nonexistent", username="newuser")
        self.assertIsNone(result)
    
    def test_delete_user_success(self):
        """Test successful user deletion"""
        user = self.user_service.create_user("testuser", "test@example.com")
        success = self.user_service.delete_user(user['id'])
        
        self.assertTrue(success)
        self.assertIsNone(self.user_service.get_user(user['id']))
    
    def test_delete_user_not_exists(self):
        """Test deleting non-existing user"""
        success = self.user_service.delete_user("nonexistent")
        self.assertFalse(success)


class TestDataService(unittest.TestCase):
    """Test DataService functionality"""
    
    def setUp(self):
        self.data_service = DataService()
    
    def test_process_data(self):
        """Test data processing"""
        test_data = {"name": "test", "value": 42}
        processed = self.data_service.process_data(test_data)
        
        self.assertIn('original', processed)
        self.assertIn('processed_at', processed)
        self.assertIn('checksum', processed)
        self.assertIn('size', processed)
        self.assertIn('fields_count', processed)
        self.assertEqual(processed['original'], test_data)
        self.assertEqual(processed['fields_count'], 2)
    
    def test_get_cached_data(self):
        """Test getting cached data"""
        test_data = {"name": "test", "value": 42}
        processed = self.data_service.process_data(test_data)
        checksum = processed['checksum']
        
        cached = self.data_service.get_cached_data(checksum)
        self.assertEqual(cached, processed)
    
    def test_get_cached_data_not_exists(self):
        """Test getting non-existing cached data"""
        cached = self.data_service.get_cached_data("nonexistent")
        self.assertIsNone(cached)
    
    def test_clear_cache(self):
        """Test cache clearing"""
        test_data = {"name": "test", "value": 42}
        self.data_service.process_data(test_data)
        
        cleared_count = self.data_service.clear_cache()
        self.assertEqual(cleared_count, 1)
        
        # Verify cache is empty
        cached = self.data_service.get_cached_data("any")
        self.assertIsNone(cached)


class TestSecurityService(unittest.TestCase):
    """Test SecurityService functionality"""
    
    def test_generate_password_default_length(self):
        """Test password generation with default length"""
        password = SecurityService.generate_password()
        self.assertEqual(len(password), 12)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
    
    def test_generate_password_custom_length(self):
        """Test password generation with custom length"""
        password = SecurityService.generate_password(16)
        self.assertEqual(len(password), 16)
    
    def test_hash_and_verify_password(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = SecurityService.hash_password(password)
        
        # Verify correct password
        self.assertTrue(SecurityService.verify_password(password, hashed))
        
        # Verify incorrect password
        self.assertFalse(SecurityService.verify_password("wrongpassword", hashed))
    
    def test_verify_invalid_hash(self):
        """Test password verification with invalid hash"""
        self.assertFalse(SecurityService.verify_password("password", "invalid_hash"))
    
    def test_generate_token(self):
        """Test token generation"""
        token1 = SecurityService.generate_token()
        token2 = SecurityService.generate_token()
        
        self.assertIsInstance(token1, str)
        self.assertNotEqual(token1, token2)
        self.assertTrue(len(token1) > 20)  # Should be reasonably long


class TestAnalyticsService(unittest.TestCase):
    """Test AnalyticsService functionality"""
    
    def setUp(self):
        self.analytics_service = AnalyticsService()
    
    def test_record_request_success(self):
        """Test recording successful request"""
        initial_requests = self.analytics_service.metrics['requests']
        self.analytics_service.record_request('/test', 200)
        
        self.assertEqual(self.analytics_service.metrics['requests'], initial_requests + 1)
        self.assertEqual(self.analytics_service.metrics['errors'], 0)
    
    def test_record_request_error(self):
        """Test recording error request"""
        initial_errors = self.analytics_service.metrics['errors']
        self.analytics_service.record_request('/test', 500)
        
        self.assertEqual(self.analytics_service.metrics['errors'], initial_errors + 1)
    
    def test_get_metrics(self):
        """Test getting metrics"""
        metrics = self.analytics_service.get_metrics()
        
        self.assertIn('requests', metrics)
        self.assertIn('errors', metrics)
        self.assertIn('start_time', metrics)
        self.assertIn('uptime_seconds', metrics)
        self.assertIn('error_rate', metrics)
    
    def test_reset_metrics(self):
        """Test resetting metrics"""
        # Record some activity
        self.analytics_service.record_request('/test', 200)
        self.analytics_service.record_request('/test', 500)
        
        old_metrics = self.analytics_service.reset_metrics()
        
        # Check old metrics
        self.assertIn('requests', old_metrics)
        self.assertIn('errors', old_metrics)
        
        # Check new metrics are reset
        new_metrics = self.analytics_service.get_metrics()
        self.assertEqual(new_metrics['requests'], 0)
        self.assertEqual(new_metrics['errors'], 0)


if __name__ == '__main__':
    unittest.main() 