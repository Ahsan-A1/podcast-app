from abc import ABC, abstractmethod
from typing import List, Dict, Any


class FeedFinder(ABC):
    """Base class for podcast feed finders."""

    @abstractmethod
    def search_podcasts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for podcasts based on a query string.

        Args:
            query: The search query string

        Returns:
            A list of dictionaries containing podcast feed information
        """
        pass

