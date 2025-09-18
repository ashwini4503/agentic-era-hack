"""
Personalized Trip Planner - Multilingual Support Service

Provides translation and localization using Gemini/Vertex AI.
"""


from src.interfaces.multilingual_support import MultilingualSupportInterface

class MultilingualSupportService(MultilingualSupportInterface):
    def __init__(self, ai_client):
        self.ai = ai_client

    def translate(self, text: str, target_language: str) -> str:
        """
        Translate text using Gemini/Vertex AI (actual API integration).
        """
        # Replace with actual Gemini/Vertex AI translation API call
        return self.ai.translate(text, target_language)
