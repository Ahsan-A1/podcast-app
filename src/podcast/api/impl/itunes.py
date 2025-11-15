"""
Module for finding podcast RSS feeds using iTunes API.
"""
from typing import List, Dict, Any
import requests
from urllib.parse import quote

from podcast.api.feed_finder import FeedFinder
from podcast.secrets import ITUNES_BASE_URL


class Itunes(FeedFinder):
    """Class to search and find podcast RSS feeds using iTunes API."""

    def __init__(self):
        self.search_url = ITUNES_BASE_URL

    def search_podcasts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for podcasts and return their RSS feeds.

        Args:
            query (str): Search query for the podcast

        Returns:
            List[Dict]: List of dictionaries containing podcast information including:
                       - name: Name of the podcast
                       - artist: Creator/host name
                       - feed_url: RSS feed URL
                       - artwork_url: URL to podcast artwork
                       - genre: Primary genre
        """
        encoded_query = quote(query)

        params = {
            'term': encoded_query,
            'entity': 'podcast',
            'media': 'podcast',
            'limit': 10  # Limit results to top 10
        }

        try:
            response = requests.get(f"{self.search_url}/search", params=params, timeout=10)
            response.raise_for_status()
            results = response.json()

            podcasts = []
            for item in results.get('results', []):
                if not item.get('feedUrl'):  # Skip if no feed URL
                    continue

                podcast = {
                    'id': str(item.get('artistId', 0)),
                    'name': item.get('collectionName', 'Unknown'),
                    'artist': item.get('artistName', 'Unknown'),
                    'feed_url': item['feedUrl'],
                    'artwork_url': item.get('artworkUrl600', ''),
                    'genre': item.get('primaryGenreName', [])
                }
                podcasts.append(podcast)

            return podcasts

        except requests.RequestException as e:
            print(f"Error searching for podcast: {e}")
            return []
