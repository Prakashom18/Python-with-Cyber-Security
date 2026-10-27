"""
TASK 3 - STEP 3: Emails hidden in links and written in disguise

1. mailto links:  <a href="mailto:bob@site.com">Email us</a>
   The email is inside the link, not in the visible text.
2. Obfuscated:    bob [at] site [dot] com     (written this way to fool robots)

Run:   python 3_mailto_and_obfuscated.py        (needs page.html from step 1)
"""
import re
from bs4 import BeautifulSoup

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}")

# matches:  name [at] domain [dot] com   (also with ( ) or { } or plain " at ")
OBFUSCATED_PATTERN = re.compile(
    r"([A-Za-z0-9._%+-]+)\s*[\[\(\{]?\s*at\s*[\]\)\}]?\s*"
    r"((?:[A-Za-z0-9-]+\s*[\[\(\{]?\s*dot\s*[\]\)\}]?\s*)+[A-Za-z]{2,})",
    re.IGNORECASE)


def emails_from_mailto(soup):
    found = set()
    for link in soup.select('a[href^="mailto:"]'):
        address = link["href"][len("mailto:"):].split("?")[0]   # cut off ?subject=...
        if EMAIL_PATTERN.fullmatch(address):
            found.add(address.lower())
    return found


def emails_from_obfuscated(text):
    found = set()
    for name, domain in OBFUSCATED_PATTERN.findall(text):
        # turn "site [dot] com" into "site.com"
        domain = re.sub(r"\s*[\[\(\{]?\s*dot\s*[\]\)\}]?\s*", ".", domain, flags=re.IGNORECASE)
        candidate = f"{name}@{domain}".lower().strip(".")
        if EMAIL_PATTERN.fullmatch(candidate):
            found.add(candidate)
    return found


def main():
    with open("page.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    print("From mailto links :", sorted(emails_from_mailto(soup)))
    print("From obfuscated   :", sorted(emails_from_obfuscated(soup.get_text(" "))))


if __name__ == "__main__":
    main()
