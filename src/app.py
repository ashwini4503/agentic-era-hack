
from flask import Flask, request, jsonify
# Import agent workflows and services from app/app/agent.py
from app.app.agent import (
    trip_planner_workflow,
    parallel_workflow,
    loop_workflow,
    itinerary_service,
    cost_service,
    translation_service,
    feedback_service
)
# If you need user profile or booking/payment, import those services as before
from services.user_profile import UserProfileService
from services.booking_payment import BookingPaymentService

app = Flask(__name__)

user_profile_service = UserProfileService(firebase_client=None)  # Replace None with actual client
booking_payment_service = BookingPaymentService(emt_client=None, firebase_client=None, payment_client=None)

@app.route('/profile', methods=['POST'])
def create_profile():
    user_data = request.json
    user_profile_service.create_profile(user_data)
    return jsonify({"status": "success", "message": "Profile created"}), 201

@app.route('/itinerary', methods=['POST'])
def generate_itinerary():
    data = request.json
    user_id = data.get('user_id')
    preferences = data.get('preferences', {})
    target_language = data.get('target_language', 'en')
    feedback = data.get('feedback', {})
    session_state = {
        "user_id": user_id,
        "preferences": preferences,
        "target_language": target_language,
        "feedback": feedback
    }
    result = trip_planner_workflow.run(session_state)
    return jsonify(result), 200

@app.route('/itinerary/<itinerary_id>/adjust', methods=['POST'])
def adjust_itinerary(itinerary_id):
    itinerary = itinerary_service.adjust_realtime(itinerary_id)
    return jsonify(itinerary), 200

@app.route('/feedback', methods=['POST'])
def collect_feedback():
    data = request.json
    user_id = data.get('user_id')
    feedback = data.get('feedback')
    session_state = {"user_id": user_id, "feedback": feedback}
    result = loop_workflow.run(session_state)
    return jsonify({"status": "success", "message": "Feedback collected", "workflow_result": result}), 201

@app.route('/feedback/analytics', methods=['GET'])
def feedback_analytics():
    analytics = feedback_service.analyze_feedback()
    return jsonify(analytics), 200

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language', 'en')
    session_state = {"text": text, "target_language": target_language}
    result = translation_service.translate(text, target_language)
    return jsonify({"translated_text": result}), 200

@app.route('/cost/<itinerary_id>', methods=['GET'])
def cost_breakdown(itinerary_id):
    result = cost_service.get_cost_breakdown(itinerary_id)
    return jsonify(result), 200

@app.route('/share/<itinerary_id>', methods=['GET'])
def share_itinerary(itinerary_id):
    link = cost_service.generate_shareable_link(itinerary_id)
    return jsonify({"shareable_link": link}), 200

@app.route('/book', methods=['POST'])
def book_itinerary():
    data = request.json
    itinerary_id = data.get('itinerary_id')
    payment_info = data.get('payment_info')
    booking_confirmation, payment_status = booking_payment_service.book(itinerary_id, payment_info)
    return jsonify({
        "booking_confirmation": booking_confirmation,
        "payment_status": payment_status
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
from flask import Flask, request, jsonify
from adk.agents import Agent, AgentRunner
from adk.tools import google_search
from services.itinerary_generator import ItineraryGenerator
from services.user_profile import UserProfileService
from services.testing_feedback import TestingFeedbackService
from services.multilingual_support import MultilingualSupportService
from services.cost_sharing import CostSharingService
from services.booking_payment import BookingPaymentService

# --- ADK Agent Definition ---
trip_agent = Agent(
    name="trip_planner_agent",
    model="gemini-2.5-flash",  # Use your preferred Gemini/Vertex AI model
    instruction="You are a travel planner agent. Generate personalized itineraries based on user preferences, budget, and interests.",
    description="Agent for personalized trip planning using Google ecosystem.",
    tools=[google_search]  # Add more tools as needed
)

runner = AgentRunner(agent=trip_agent)

app = Flask(__name__)

# Initialize your services (replace ... with actual client instances)
itinerary_service = ItineraryGenerator(ai_client=runner, maps_api_key=..., bigquery_client=..., firebase_client=...)
user_profile_service = UserProfileService(firebase_client=...)
feedback_service = TestingFeedbackService(firebase_client=..., bigquery_client=...)
multilingual_service = MultilingualSupportService(ai_client=runner)
cost_sharing_service = CostSharingService(firebase_client=...)
booking_payment_service = BookingPaymentService(emt_client=..., firebase_client=..., payment_client=...)

@app.route('/profile', methods=['POST'])
def create_profile():
    user_data = request.json
    user_profile_service.create_profile(user_data)
    return jsonify({"status": "success", "message": "Profile created"}), 201

@app.route('/itinerary', methods=['POST'])
def generate_itinerary():
    data = request.json
    user_id = data.get('user_id')
    preferences = data.get('preferences', {})
    itinerary = itinerary_service.generate(user_id, preferences)
    return jsonify(itinerary), 200

@app.route('/itinerary/<itinerary_id>/adjust', methods=['POST'])
def adjust_itinerary(itinerary_id):
    itinerary = itinerary_service.adjust_realtime(itinerary_id)
    return jsonify(itinerary), 200

@app.route('/feedback', methods=['POST'])
def collect_feedback():
    data = request.json
    user_id = data.get('user_id')
    feedback = data.get('feedback')
    feedback_service.collect_feedback(user_id, feedback)
    return jsonify({"status": "success", "message": "Feedback collected"}), 201

@app.route('/feedback/analytics', methods=['GET'])
def feedback_analytics():
    analytics = feedback_service.analyze_feedback()
    return jsonify(analytics), 200

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language')
    translated = multilingual_service.translate(text, target_language)
    return jsonify({"translated_text": translated}), 200

@app.route('/cost/<itinerary_id>', methods=['GET'])
def cost_breakdown(itinerary_id):
    cost = cost_sharing_service.get_cost_breakdown(itinerary_id)
    return jsonify(cost), 200

@app.route('/share/<itinerary_id>', methods=['GET'])
def share_itinerary(itinerary_id):
    link = cost_sharing_service.share_itinerary(itinerary_id)
    return jsonify({"shareable_link": link}), 200

@app.route('/book', methods=['POST'])
def book_itinerary():
    data = request.json
    itinerary_id = data.get('itinerary_id')
    payment_info = data.get('payment_info')
    booking_confirmation, payment_status = booking_payment_service.book(itinerary_id, payment_info)
    return jsonify({
        "booking_confirmation": booking_confirmation,
        "payment_status": payment_status
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
