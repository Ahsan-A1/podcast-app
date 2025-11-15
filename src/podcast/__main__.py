"""
Command-line interface for the podcast downloader.
"""
from typing import Optional
import sys

from podcast.api.feed_finder import FeedFinder
from podcast.api.impl.itunes import Itunes
from podcast.api.impl.podcast_index import PodcastIndex
from podcast.service.downloader import Downloader


def print_progress(progress: float):
    """Print download progress."""
    sys.stdout.write(f"\rProgress: {progress:.1f}%")
    sys.stdout.flush()
    if progress >= 100:
        print("\nDownload complete!")

def select_from_list(items: list, prompt: str) -> Optional[int]:
    """
    Let user select an item from a list.

    Args:
        items: List of items to choose from
        prompt: Prompt to show user

    Returns:
        Optional[int]: Selected index or None if invalid
    """
    if not items:
        return None

    print("\n" + prompt)
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")

    try:
        choice = int(input("\nEnter number: "))
        if 1 <= choice <= len(items):
            return choice - 1
    except ValueError:
        pass

    print("Invalid selection")
    return None

def main():
    """Main entry point for the podcast downloader."""
    # finder: FeedFinder = Itunes()
    finder: FeedFinder = PodcastIndex()
    downloader = Downloader()

    query = None
    query = "The rest is politics"
    if not query:
        query = input("Enter podcast name to search: ").strip()

    if not query:
        print("Search query cannot be empty")
        return

    # Search for podcasts
    print("\nSearching for podcasts...")
    results = finder.search_podcasts(query)

    if not results:
        print("No podcasts found!")
        return

    # Show found podcasts
    podcast_names = [f"{p['name']} by {p['artist']}" for p in results]
    choice = select_from_list(podcast_names, "Found podcasts:")
    if choice is None:
        return

    podcast = results[choice]
    print(f"\nFetching episodes for: {podcast['name']}")

    # Get episodes
    episodes = downloader.get_feed(podcast['feed_url'])
    if not episodes:
        print("No episodes found!")
        return

    # Show episodes
    episode_titles = [f"{e['title']} ({e['duration']})" for e in episodes[:10]]
    choice = select_from_list(episode_titles, "Latest episodes:")
    if choice is None:
        return

    # Download selected episode
    episode = episodes[choice]
    filename = f"{episode['title']}.mp3"
    print(f"\nDownloading: {filename}")

    # Download with progress tracking
    downloader.download_episode(episode['url'], filename, callback=print_progress)

if __name__ == "__main__":
    main()
