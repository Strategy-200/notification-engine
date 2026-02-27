from flask import Flask, request, jsonify

from deduplication import DeduplicationManager
from fatigue_manager import FatigueManager
from decision_engine import DecisionEngine
from fallback import FallbackEngine


app = Flask(__name__)

# Initialize components
dedupe_manager = DeduplicationManager()
fatigue_manager = FatigueManager()
decision_engine = DecisionEngine(fatigue_manager)
fallback_engine = FallbackEngine()


@app.route("/evaluate", methods=["POST"])
def evaluate_notification():
    try:
        data = request.json

        user_id = data.get("user_id")
        message = data.get("message", "")
        event_type = data.get("event_type", "general")

        # 1️⃣ Duplicate Check
        if dedupe_manager.is_duplicate(user_id, message, event_type):
            return jsonify({
                "decision": "NEVER",
                "reason": "Duplicate notification detected"
            })

        # 2️⃣ Decision Engine
        try:
            result = decision_engine.evaluate(data)
        except Exception as e:
            # 3️⃣ Fallback if AI fails
            result = fallback_engine.evaluate(data)

        # 4️⃣ Record fatigue if notification sent now
        if result["decision"] == "NOW":
            fatigue_manager.record_notification(user_id)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/")
def home():
    return "Notification Prioritization Engine Running"


if __name__ == "__main__":
    app.run(debug=True)