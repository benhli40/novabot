import json
import time
from datetime import datetime, timedelta

class NovaBotDataManager:
    def __init__(self):
        self.data_storage = {
            "personal_settings": {},  # Always retained
            "conversations": [],  # Retained based on rules
            "scraped_data": [],  # Temporary retention
        }
        self.deletion_threshold = timedelta(days=180)  # 6-month retention
        self.short_term_retention = timedelta(days=7)  # For non-critical data
    
    def create(self, key, value):
        """Create a new entry in the data storage."""
        self.data_storage[key] = value
    
    def read(self, key):
        """Retrieve an entry from the data storage."""
        return self.data_storage.get(key, None)
    
    def update(self, key, new_value):
        """Update an existing entry in the data storage."""
        if key in self.data_storage:
            self.data_storage[key] = new_value
    
    def delete(self, key):
        """Delete an entry from the data storage."""
        if key in self.data_storage:
            del self.data_storage[key]
    
    def apply_retention_policy(self):
        """Delete old conversations and outdated scraped data based on retention rules."""
        now = datetime.now()
        self.data_storage["conversations"] = [
            convo for convo in self.data_storage["conversations"]
            if convo.get("important", False) or (now - datetime.fromisoformat(convo["timestamp"]) < self.deletion_threshold)
        ]
        
        self.data_storage["scraped_data"] = [
            data for data in self.data_storage["scraped_data"]
            if now - datetime.fromisoformat(data["timestamp"]) < self.short_term_retention
        ]
    
    def run_integrity_check(self):
        """Check data consistency by ensuring required fields exist in stored data."""
        try:
            assert isinstance(self.data_storage, dict)
            assert "personal_settings" in self.data_storage
            assert "conversations" in self.data_storage
            assert "scraped_data" in self.data_storage
            return True
        except AssertionError:
            return False
    
    def store_conversation(self, user_id, conversation, important=False, backdate_days=0):
        timestamp = datetime.now() - timedelta(days=backdate_days)
        self.data_storage["conversations"].append({
            "user_id": user_id,
            "conversation": conversation,
            "timestamp": timestamp.isoformat(),
            "important": important
        })
    
    def store_scraped_data(self, source, content):
        timestamp = datetime.now()
        self.data_storage["scraped_data"].append({
            "source": source,
            "content": content,
            "timestamp": timestamp.isoformat(),
        })
    
    def delete_old_data(self):
        """Manually trigger old data deletion."""
        self.apply_retention_policy()
    
    def summarize_conversations(self):
        """Summarize stored conversations."""
        summaries = []
        for convo in self.data_storage["conversations"]:
            summaries.append(f"Summary of chat from {convo['timestamp']}: {convo['conversation'][:50]}...")
        return summaries
    
    def request_deletion_confirmation(self, user_id):
        """Ask if user wants to delete old data."""
        to_delete = [
            convo for convo in self.data_storage["conversations"]
            if not convo["important"] and datetime.now() - datetime.fromisoformat(convo["timestamp"]) > self.deletion_threshold
        ]
        if to_delete:
            return f"You have {len(to_delete)} old conversations. Should I delete them? (yes/no)"
        return "No old data to delete."
    
    def save_to_file(self, filename="lumina_data.json"):
        """Save data to a JSON file."""
        with open(filename, "w") as file:
            json.dump(self.data_storage, file, indent=4)
    
    def load_from_file(self, filename="lumina_data.json"):
        """Load data from a JSON file."""
        try:
            with open(filename, "r") as file:
                self.data_storage = json.load(file)
        except FileNotFoundError:
            print("No previous data found. Starting fresh.")

# Example Usage
if __name__ == "__main__":
    novabot = NovaBotDataManager()
    novabot.store_conversation("user1", "This is an old conversation.", backdate_days=181)
    novabot.store_conversation("user1", "This is an important chat about AI.", important=True)
    novabot.store_scraped_data("news_site", "Latest AI trends in 2025.")
    time.sleep(1)  # Simulate passage of time
    novabot.delete_old_data()
    print(novabot.summarize_conversations())
    print(novabot.request_deletion_confirmation("user1"))