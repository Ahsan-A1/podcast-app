import hashlib
import time

import requests

from podcast.secrets import PODCAST_INDEX_API_KEY, PODCAST_INDEX_API_SECRET, PODCAST_INDEX_BASE_URL


class PodcastIndex:
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

    def search_podcasts(self, query: str):
        url = f"{self.base_url}search/byterm"
        params = {"q": query}
        response = requests.get(url, headers=self.get_headers(), params=params)
        return response.json()

    def get_podcast_by_id(self, podcast_id: int):
        url = f"{self.base_url}podcasts/byid"
        params = {"id": podcast_id}
        response = requests.get(url, headers=self.get_headers(), params=params)
        return response.json()