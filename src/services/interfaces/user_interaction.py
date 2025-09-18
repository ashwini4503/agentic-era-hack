
from abc import ABC, abstractmethod

class UserInteractionInterface(ABC):
    """
    Interface for user interaction services (profile, preferences, feedback).
    """
    @abstractmethod
    def create_profile(self, user_data: dict) -> None:
        """
        Store user profile data.
        """
        pass

    @abstractmethod
    def get_profile(self, user_id: str) -> dict:
        """
        Retrieve user profile data.
        """
        pass

    @abstractmethod
    def collect_feedback(self, user_id: str, feedback: dict) -> None:
        """
        Store user feedback.
        """
        pass
