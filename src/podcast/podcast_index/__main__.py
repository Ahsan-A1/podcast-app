import argparse
import json

from podcast.podcast_index.PodcastIndex import PodcastIndex


def pretty_print(obj):
    try:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    except TypeError:
        print(obj)


def main():
    pi = PodcastIndex()
    try:
        result = pi.search_podcasts("the news agents")
    except Exception as exc:
        print("Error while calling PodcastIndex.search_podcasts:", exc)
        return

    if not result:
        print("No result returned (empty/None).")
        return

    pretty_print(result)


if __name__ == "__main__":
    main()

