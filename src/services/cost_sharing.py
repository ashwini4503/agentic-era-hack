"""
Personalized Trip Planner - Cost Breakdown & Sharing Service

Provides cost breakdowns and sharing capabilities for itineraries.
"""


class CostSharingService:
    def __init__(self, firebase_client):
        self.firebase = firebase_client

    def get_cost_breakdown(self, itinerary_id):
        """
        Retrieve cost breakdown for an itinerary from Firebase.
        """
        return self.firebase.get_cost_breakdown(itinerary_id)

    def share_itinerary(self, itinerary_id):
        """
        Generate shareable link for itinerary using Firebase.
        """
        return self.firebase.generate_shareable_link(itinerary_id)
