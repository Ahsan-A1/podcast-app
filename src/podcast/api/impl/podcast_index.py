import hashlib
import time
from typing import List, Any, Dict

import requests

from podcast.api.feed_finder import FeedFinder
from podcast.secrets import PODCAST_INDEX_API_KEY, PODCAST_INDEX_API_SECRET, PODCAST_INDEX_BASE_URL


class PodcastIndex(FeedFinder):
    def __init__(self):
        self.api_key = PODCAST_INDEX_API_KEY
        self.api_secret = PODCAST_INDEX_API_SECRET
        self.base_url = PODCAST_INDEX_BASE_URL

    def get_headers(self):
        epoch_time = int(time.time())
        data_to_hash = self.api_key + self.api_secret + str(epoch_time)
        sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()
        return {
            'X-Auth-Date': str(epoch_time),
            'X-Auth-Key': self.api_key,
            'Authorization': sha_1,
            'User-Agent': 'postcasting-index-python-cli'
        }

    def search_podcasts(self, query: str) -> List[Dict[str, Any]]:
        url = f"{self.base_url}search/byterm"
        params = {"q": query}
        response = requests.get(url, headers=self.get_headers(), params=params)
        res = response.json()
        feeds = res.get("feeds", [])
        podcasts = []
        for feed in feeds:
            podcast = {
                'id': str(feed.get('podcastGuid', 0)),
                'name': feed.get('title', 'Unknown'),
                'artist': feed.get('author', 'Unknown'),
                'feed_url': feed['url'],
                'artwork_url': feed.get('artwork', ''),
                'genre': feed.get('categories', {}).values()
            }
            podcasts.append(podcast)
        return podcasts

    def get_podcast_by_id(self, podcast_id: int):
        url = f"{self.base_url}podcasts/byid"
        params = {"id": podcast_id}
        response = requests.get(url, headers=self.get_headers(), params=params)
        return response.json()