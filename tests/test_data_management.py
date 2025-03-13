import unittest
import json
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the data management module
from data_management.novabot_data_management import NovaBotDataManager

class TestLuminaDataManager(unittest.TestCase):
    def setUp(self):
        """Initialize a temporary instance of the data manager for testing."""
        self.data_manager = NovaBotDataManager()
        self.test_data = {
            "user": "TestUser",
            "preferences": {
                "theme": "dark",
                "notifications": True
            },
            "conversation_history": [
                {"timestamp": "2025-03-12T12:00:00", "message": "Hello, NovaBot!"}
            ]
        }
    
    def test_create_entry(self):
        """Test creating a new entry in the database."""
        self.data_manager.create("test_key", self.test_data)
        result = self.data_manager.read("test_key")
        self.assertEqual(result, self.test_data)
    
    def test_read_entry(self):
        """Test reading an existing entry."""
        self.data_manager.create("read_test", self.test_data)
        result = self.data_manager.read("read_test")
        self.assertIsNotNone(result)
    
    def test_update_entry(self):
        """Test updating an existing entry."""
        updated_data = {"user": "UpdatedUser", "preferences": {"theme": "light"}}
        self.data_manager.create("update_test", self.test_data)
        self.data_manager.update("update_test", updated_data)
        result = self.data_manager.read("update_test")
        self.assertEqual(result["user"], "UpdatedUser")
    
    def test_delete_entry(self):
        """Test deleting an entry and ensuring it's removed."""
        self.data_manager.create("delete_test", self.test_data)
        self.data_manager.delete("delete_test")
        result = self.data_manager.read("delete_test")
        self.assertIsNone(result)
    
    def test_retention_policy(self):
        """Simulate LUMINA's data retention rules and ensure they work correctly."""
        self.data_manager.create("old_entry", self.test_data)
        self.data_manager.apply_retention_policy()
        result = self.data_manager.read("old_entry")
        self.assertIsNone(result)  # Ensure old data is deleted
    
    def test_large_data_handling(self):
        """Simulate large-scale data storage and retrieval."""
        large_data = {f"entry_{i}": "TestData" * 1000 for i in range(1000)}  # 1000 large entries
        self.data_manager.create("large_test", large_data)
        result = self.data_manager.read("large_test")
        self.assertEqual(len(result), 1000)
    
    def test_automatic_testing(self):
        """Ensure LUMINA can periodically self-test its data integrity."""
        integrity_check = self.data_manager.run_integrity_check()
        self.assertTrue(integrity_check)
    
    def tearDown(self):
        """Clean up after each test run."""
        self.data_manager.delete("test_key")
        self.data_manager.delete("read_test")
        self.data_manager.delete("update_test")
        self.data_manager.delete("delete_test")
        self.data_manager.delete("old_entry")
        self.data_manager.delete("large_test")
    
if __name__ == "__main__":
    unittest.main()