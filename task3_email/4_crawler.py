"""
TASK 3 - STEP 4: A small, polite crawler

Starting from one page, it follows links to other pages ON THE SAME WEBSITE only.
Safety rules built in:
  - stays on the same website (scope)
  - obeys robots.txt (the site's "please don't visit these pages" file)
  - waits between requests
  - stops after a maximum number of pages

Run:   python 4_crawler.py https://your-authorized-site.com
Prints the list of pages it visited.
"""
import sys
import time
import requests
from urllib import robotparser
from urllib.parse import urljoin, urlparse, urldefrag
from bs4 import BeautifulSoup

MAX_PAGES = 20
DELAY = 1.0
HEADERS = {"User-Agent": "osint-assessment/1.0 (authorized lab use)"}


def load_robots(start_url):
    """Read the site's robots.txt so we know what we may visit."""
    parts = urlparse(start_url)
    robots = robotparser.RobotFileParser()
    try:
        r = requests.get(f"{parts.scheme}://{parts.netloc}/robots.txt", headers=HEADERS, timeout=10)
        robots.parse(r.text.splitlines() if r.status_code == 200 else [])
    except requests.RequestException:
        robots.parse([])
    return robots


def crawl(start_url):
    """Return a dict {page_url: html} for pages we visited."""
    site = urlparse(start_url).netloc
    robots = load_robots(start_url)

    to_visit = [start_url]          # pages waiting to be visited
    seen = {start_url}              # pages we already queued (avoids repeats)
    pages = {}

    while to_visit and len(pages) < MAX_PAGES:
        url = to_visit.pop(0)
        if not robots.can_fetch(HEADERS["User-Agent"], url):
            print("  skipped (robots.txt):", url)
            continue
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
        except requests.RequestException:
            continue
        time.sleep(DELAY)                                   # be polite

        if response.status_code != 200 or "html" not in response.headers.get("content-type", ""):
            continue
        pages[url] = response.text
        print("  visited:", url)

        # find links on this page
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.find_all("a", href=True):
            link = urldefrag(urljoin(url, a["href"]))[0]    # make absolute, drop #section
            if urlparse(link).netloc == site and link not in seen:
                seen.add(link)
                to_visit.append(link)
    return pages


def main():
    if len(sys.argv) < 2:
        print("Usage: python 4_crawler.py https://site.com")
        return
    pages = crawl(sys.argv[1])
    print(f"\nVisited {len(pages)} page(s)")


if __name__ == "__main__":
    main()
