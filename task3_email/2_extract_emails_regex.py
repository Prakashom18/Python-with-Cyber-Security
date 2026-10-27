"""
TASK 3 - STEP 2: Find emails with a regular expression (regex) + BeautifulSoup

A regex is a pattern. This one describes the shape of an email:
    letters/numbers/dots  @  domain name  .  ending (com, org, ...)

BeautifulSoup turns the HTML into plain visible text first, so we don't
accidentally match things inside code.

Run:   python 2_extract_emails_regex.py        (needs page.html from step 1)
"""
import re
from bs4 import BeautifulSoup

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}")


def find_emails(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ")                    # all visible text on the page
    matches = EMAIL_PATTERN.findall(text)
    return sorted(set(m.lower() for m in matches))   # set() removes duplicates


def main():
    with open("page.html", encoding="utf-8") as f:
        html = f.read()

    emails = find_emails(html)
    print(f"Found {len(emails)} email(s):")
    for e in emails:
        print(" ", e)


if __name__ == "__main__":
    main()
