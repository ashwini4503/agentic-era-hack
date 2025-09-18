
from abc import ABC, abstractmethod

class MultilingualSupportInterface(ABC):
    """
    Interface for multilingual support services.
    """
    @abstractmethod
    def translate(self, text: str, target_language: str) -> str:
        """
        Translate the given text to the target language.
        """
        pass
