#!/usr/bin/env python3
import feedparser
import argparse
import os
import json
from textwrap import fill
from bs4 import BeautifulSoup

CONFIG_FILE = os.path.expanduser("~/.rssfeeds.json")

def load_feeds():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return []

def save_feeds(feeds):
    with open(CONFIG_FILE, "w") as f:
        json.dump(feeds, f, indent=2)

def add_feed(url):
    feeds = load_feeds()
    if url not in feeds:
        feeds.append(url)
        save_feeds(feeds)
        print(f"Feed added: {url}")
    else:
        print("Feed already exists.")

def list_feeds():
    feeds = load_feeds()
    if not feeds:
        print("No feeds added yet.")
        return
    for i, url in enumerate(feeds, 1):
        print(f"[{i}] {url}")

def remove_feed(index):
    feeds = load_feeds()
    if index < 1 or index > len(feeds):
        print("Invalid feed number.")
        return
    removed = feeds.pop(index-1)
    save_feeds(feeds)
    print(f"Feed removed: {removed}")

def clean_html(raw_html: str) -> str:
    """Strip HTML tags and return plain text."""
    return BeautifulSoup(raw_html, "html.parser").get_text()

def show_feed(index):
    feeds = load_feeds()
    if index < 1 or index > len(feeds):
        print("Invalid feed number.")
        return
    url = feeds[index-1]
    feed = feedparser.parse(url)
    print(f"\n=== {feed.feed.get('title', 'No Title')} ===")
    for i, entry in enumerate(feed.entries[:10], 1):
        print(f"[{i}] {entry.title}")
    choice = input("\nSelect number (to read content): ")
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(feed.entries):
            entry = feed.entries[choice-1]
            print("\n--- TITLE ---")
            print(entry.title)

            # Ask whether to show summary or full content
            mode = input("Show [s]ummary or [f]ull content? ").strip().lower()
            if mode == "f" and "content" in entry:
                text = entry.content[0].value
                print("\n--- FULL CONTENT ---")
                print(fill(clean_html(text), width=80))
            else:
                summary = entry.get("summary", "No summary available")
                print("\n--- SUMMARY ---")
                print(fill(clean_html(summary), width=80))

            print("\n--- LINK ---")
            print(entry.link)

def main():
    parser = argparse.ArgumentParser(description="Simple RSS CLI reader")
    parser.add_argument("command", choices=["add", "list", "show", "remove"], help="Command")
    parser.add_argument("arg", nargs="?", help="Command argument")
    args = parser.parse_args()

    if args.command == "add" and args.arg:
        add_feed(args.arg)
    elif args.command == "list":
        list_feeds()
    elif args.command == "show" and args.arg:
        show_feed(int(args.arg))
    elif args.command == "remove" and args.arg:
        remove_feed(int(args.arg))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
