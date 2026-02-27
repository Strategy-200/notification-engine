import hashlib
import time


class DeduplicationManager:
    def __init__(self):
        # Store hashes with timestamps
        self.seen_notifications = {}

        # Time window (seconds) to consider duplicates
        self.window = 60  # 1 minute

    def _create_hash(self, user_id, message, event_type):
        """
        Create unique hash for notification
        """
        unique_string = f"{user_id}-{message}-{event_type}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def is_duplicate(self, user_id, message, event_type):
        """
        Check if notification is duplicate
        """
        current_time = time.time()
        notif_hash = self._create_hash(user_id, message, event_type)

        # Remove old entries
        self._cleanup(current_time)

        if notif_hash in self.seen_notifications:
            return True

        # Store new notification
        self.seen_notifications[notif_hash] = current_time
        return False

    def _cleanup(self, current_time):
        """
        Remove expired entries
        """
        expired_keys = [
            key for key, ts in self.seen_notifications.items()
            if current_time - ts > self.window
        ]

        for key in expired_keys:
            del self.seen_notifications[key]
    
    def is_similar(msg1, msg2):
        """
        Simple similarity check
        """
        msg1 = msg1.lower()
        msg2 = msg2.lower()

        common_words = set(msg1.split()) & set(msg2.split())

        similarity = len(common_words) / max(len(msg1.split()), 1)

        return similarity > 0.6

"""
if __name__ == "__main__":
    manager = DeduplicationManager()

    print(manager.is_duplicate("U1", "Hello", "msg"))  # False
    print(manager.is_duplicate("U1", "Hello", "msg"))  # True 
"""