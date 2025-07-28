import unittest
import json
from app import app
from app.utils import validate_email, sanitize_string, generate_id, log_operation

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_endpoint(self):
        """Test home endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'third-party-integration-demo')

    def test_integration_endpoint(self):
        """Test integration endpoint"""
        response = self.app.get('/test-integration')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertIn('timestamp', data)

    def test_utils_endpoint(self):
        """Test utils endpoint"""
        response = self.app.get('/utils-test')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('status', data)
        self.assertIn('data', data)

    def test_data_endpoint_get(self):
        """Test data endpoint GET method"""
        response = self.app.get('/api/v1/data')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertIn('method', data)

    def test_data_endpoint_post_valid(self):
        """Test data endpoint POST method with valid data"""
        test_data = {"name": "test", "value": 123}
        response = self.app.post('/api/v1/data', 
                               data=json.dumps(test_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'created')

    def test_data_endpoint_post_invalid(self):
        """Test data endpoint POST method with invalid data"""
        response = self.app.post('/api/v1/data', 
                               data="invalid json",
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('uptime', data)
        self.assertIn('response_time', data)

class TestUtils(unittest.TestCase):
    def test_validate_email_valid(self):
        """Test email validation with valid email"""
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name@domain.co.uk"))

    def test_validate_email_invalid(self):
        """Test email validation with invalid email"""
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email("@domain.com"))
        self.assertFalse(validate_email("user@"))

    def test_sanitize_string(self):
        """Test string sanitization"""
        self.assertEqual(sanitize_string("  test  "), "test")
        self.assertEqual(sanitize_string(""), "")
        self.assertEqual(sanitize_string(123), "")

    def test_generate_id(self):
        """Test ID generation"""
        id1 = generate_id()
        id2 = generate_id()
        self.assertIsInstance(id1, str)
        self.assertNotEqual(id1, id2)

    def test_log_operation(self):
        """Test operation logging"""
        # This should not raise any exceptions
        log_operation("test_operation", {"test": "data"})

if __name__ == '__main__':
    unittest.main() 