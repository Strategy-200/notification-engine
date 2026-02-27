import random
from datetime import datetime


class DecisionEngine:

    def __init__(self, fatigue_manager):
        self.fatigue_manager = fatigue_manager

    def _priority_to_score(self, priority_hint):
        """
        Convert priority text to numeric urgency score
        """
        mapping = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.9
        }
        return mapping.get(priority_hint, 0.5)

    def _check_expiry(self, expires_at):
        """
        Check if notification expired
        """
        if not expires_at:
            return False

        expiry_time = datetime.fromisoformat(expires_at)
        return datetime.now() > expiry_time

    def evaluate(self, notification):
        """
        Main decision function
        """

        user_id = notification.get("user_id")
        priority_hint = notification.get("priority_hint", "low")
        expires_at = notification.get("expires_at")

        # Expiry check
        if self._check_expiry(expires_at):
            return {
                "decision": "NEVER",
                "reason": "Notification expired",
                "score": 0
            }

        # Urgency
        urgency = self._priority_to_score(priority_hint)

        # Fatigue
        fatigue = self.fatigue_manager.get_fatigue_score(user_id)

        # Simulated engagement probability
        engagement = random.uniform(0.3, 0.9)

        # Repetition penalty (simple random for demo)
        repetition_penalty = random.uniform(0, 0.3)

        # Final score calculation
        score = (
            0.5 * urgency +
            0.4 * engagement -
            0.3 * fatigue -
            repetition_penalty
        )

        # Classification
        if priority_hint == "high" and fatigue < 0.5:
            decision = "NOW"
        else:
            if score > 0.7:
                decision = "NOW"
            elif score > 0.4:
                decision = "LATER"
            else:
                decision = "NEVER"

        # Explanation log
        explanation = {
            "decision": decision,
            "score": round(score, 2),
            "urgency": urgency,
            "fatigue": round(fatigue, 2),
            "engagement": round(engagement, 2),
            "reason": f"Calculated using urgency, engagement, and fatigue"
        }

        return explanation
"""
if __name__ == "__main__":
    from fatigue_manager import FatigueManager

    fm = FatigueManager()
    engine = DecisionEngine(fm)

    notif = {
        "user_id": "U1",
        "priority_hint": "high"
    }

    result = engine.evaluate(notif)
    print(result)
"""