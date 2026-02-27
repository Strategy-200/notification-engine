class FallbackEngine:
    """
    Simple rule-based fallback if AI system fails
    """

    def __init__(self):
        pass

    def evaluate(self, notification):
        priority = notification.get("priority_hint", "low")

        if priority == "high":
            decision = "NOW"
            reason = "Fallback: High priority notification"
        elif priority == "medium":
            decision = "LATER"
            reason = "Fallback: Medium priority notification"
        else:
            decision = "NEVER"
            reason = "Fallback: Low priority notification"

        return {
            "decision": decision,
            "score": 0.5,
            "reason": reason
        }
"""
if __name__ == "__main__":
    engine = FallbackEngine()

    notif = {
        "priority_hint": "high"
    }

    print(engine.evaluate(notif))
"""