"""
TASK 3 - STEP 1: Fetch one web page (using requests)

Before we can look for emails we need the page's content.

Run:   python 1_fetch_page.py https://your-authorized-site.com
Saves: page.html
"""
import sys
import requests


def main():
    if len(sys.argv) < 2:
        print("Usage: python 1_fetch_page.py https://site.com")
        return
    url = sys.argv[1]

    # A User-Agent tells the website who is visiting (good practice to be honest)
    headers = {"User-Agent": "osint-assessment/1.0 (authorized lab use)"}
    response = requests.get(url, headers=headers, timeout=10)

    print("Status code :", response.status_code)
    print("Page size   :", len(response.text), "characters")

    with open("page.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Saved to page.html")


main()
