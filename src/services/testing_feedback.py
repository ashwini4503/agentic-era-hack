"""
Personalized Trip Planner - Testing & Feedback Service

Handles user testing, feedback collection, and iteration using Firebase and BigQuery.
"""


class TestingFeedbackService:
    def __init__(self, firebase_client, bigquery_client):
        self.firebase = firebase_client
        self.bigquery = bigquery_client

    def collect_feedback(self, user_id, feedback):
        """
        Store user feedback in Firebase.
        """
        self.firebase.save_feedback(user_id, feedback)

    def analyze_feedback(self):
        """
        Analyze feedback using BigQuery (actual query integration).
        """
        query = "SELECT * FROM `your_project.your_dataset.feedback`"
        results = self.bigquery.query(query)
        return [dict(row) for row in results]
