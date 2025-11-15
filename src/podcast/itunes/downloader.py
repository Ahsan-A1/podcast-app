"""
Module for downloading podcast episodes.
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import requests
import feedparser

class PodcastDownloader:
    """Class to handle podcast feed parsing and episode downloading."""

    def __init__(self, download_dir: str = "downloads"):
        """
        Initialize the PodcastDownloader.

        Args:
            download_dir (str): Directory to store downloaded episodes
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)

    def download_episode(self, url: str, filename: str, callback=None) -> Optional[Path]:
        """
        Download a podcast episode with progress tracking.

        Args:
            url (str): URL of the episode
            filename (str): Name to save the file as
            callback (callable, optional): Function to call with progress updates

        Returns:
            Path: Path to the downloaded file, or None if download failed
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            file_path = self.download_dir / self._sanitize_filename(filename)
            total_size = int(response.headers.get('content-length', 0))

            with open(file_path, 'wb') as f:
                if total_size == 0:
                    f.write(response.content)
                else:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if callback:
                                progress = (downloaded / total_size) * 100
                                callback(progress)

            return file_path

        except requests.RequestException as e:
            print(f"Error downloading episode: {e}")
            return None

    def get_feed(self, feed_url: str) -> List[Dict]:
        """
        Get episodes from a podcast RSS feed.

        Args:
            feed_url (str): URL of the RSS feed

        Returns:
            list: List of episodes with their information
        """
        try:
            feed = feedparser.parse(feed_url)
            episodes = []

            for entry in feed.entries:
                episode = {
                    'title': entry.title,
                    'description': entry.get('description', ''),
                    'published': entry.get('published', ''),
                    'duration': entry.get('itunes_duration', ''),
                    'url': None
                }

                # Find the audio file URL
                for link in entry.links:
                    if link.get('type', '').startswith('audio/'):
                        episode['url'] = link.href
                        break

                if episode['url']:  # Only add if we found an audio URL
                    episodes.append(episode)

            return episodes

        except Exception as e:
            print(f"Error parsing feed: {e}")
            return []

    def _sanitize_filename(self, filename: str) -> str:
        """
        Clean filename to be filesystem-safe.

        Args:
            filename (str): Original filename

        Returns:
            str: Sanitized filename
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
