import time


class FatigueManager:
    def __init__(self):
        # Store user notification history
        self.user_history = {}

        # Time window for fatigue calculation (seconds)
        self.window = 300  # 5 minutes

    def _cleanup(self, user_id, current_time):
        """
        Remove old notifications outside time window
        """
        if user_id not in self.user_history:
            return

        self.user_history[user_id] = [
            ts for ts in self.user_history[user_id]
            if current_time - ts <= self.window
        ]

    def record_notification(self, user_id):
        """
        Record that a notification was sent to user
        """
        current_time = time.time()

        if user_id not in self.user_history:
            self.user_history[user_id] = []

        self.user_history[user_id].append(current_time)

        self._cleanup(user_id, current_time)

    def get_fatigue_score(self, user_id):
        """
        Calculate fatigue score between 0 and 1
        """
        current_time = time.time()

        if user_id not in self.user_history:
            return 0.0

        self._cleanup(user_id, current_time)

        recent_count = len(self.user_history[user_id])

        # Normalize fatigue score
        fatigue = min(recent_count / 10, 1.0)

        return fatigue
"""   
if __name__ == "__main__":
    fm = FatigueManager()

    user = "U1"

    fm.record_notification(user)
    fm.record_notification(user)
    fm.record_notification(user)

    print("Fatigue:", fm.get_fatigue_score(user))
"""