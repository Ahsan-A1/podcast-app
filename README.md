# Podcast Downloader

A simple Python package for searching and downloading podcast episodes.

## Features

- Search for podcasts using the iTunes API
- Parse podcast RSS feeds
- Download episodes with progress tracking
- Command-line interface

## Installation

```bash
# Create and activate virtual environment
uv venv
# On Windows:
.venv\Scripts\activate
# On Unix:
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```

## Usage

### Command Line Interface

```bash
# Run the CLI
python -m podcast
```

### As a Python Package

```python
from podcast import Downloader, PodcastFeedFinder

# Search for podcasts
finder = PodcastFeedFinder()
results = finder.search_podcast("Python Bytes")

# Get episodes from a podcast
downloader = Downloader()
episodes = downloader.get_feed(results[0]['feed_url'])

# Download an episode
downloader.download_episode(episodes[0]['url'], "episode.mp3")
```

## Development

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Make your changes
5. Submit a pull request

## License

MIT License
