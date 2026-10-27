"""
TASK 3 - STEP 5: Everything together
Crawl -> extract (text, mailto, obfuscated) -> remove duplicates ->
remember which page each email came from -> save JSON.

This file reuses the code from steps 2, 3 and 4 by importing it.
(Python can't import a file whose name starts with a number directly, so we
use importlib below. You don't need to understand that part.)

Run:   python 5_full_email_collector.py https://your-authorized-site.com
Saves: emails.json
"""
import sys
import json
import importlib

from bs4 import BeautifulSoup

crawler = importlib.import_module("4_crawler")
extract = importlib.import_module("2_extract_emails_regex")
hidden = importlib.import_module("3_mailto_and_obfuscated")

# Addresses like these belong to a role, not a person
ROLE_NAMES = {"info", "contact", "support", "admin", "sales", "help", "office",
              "press", "hr", "jobs", "billing", "security", "webmaster", "noreply"}


def main():
    if len(sys.argv) < 2:
        print("Usage: python 5_full_email_collector.py https://site.com")
        return

    pages = crawler.crawl(sys.argv[1])

    found = {}   # email -> set of pages where it appeared
    for url, html in pages.items():
        soup = BeautifulSoup(html, "html.parser")
        emails = set(extract.find_emails(html))
        emails |= hidden.emails_from_mailto(soup)
        emails |= hidden.emails_from_obfuscated(soup.get_text(" "))
        for e in emails:
            found.setdefault(e, set()).add(url)

    results = []
    for email in sorted(found):
        local_part = email.split("@")[0]
        results.append({
            "email": email,
            "type": "role" if local_part in ROLE_NAMES else "personal",
            "found_on": sorted(found[email]),
        })

    with open("emails.json", "w") as f:
        json.dump({"start_url": sys.argv[1], "pages_visited": len(pages),
                   "emails": results}, f, indent=2)

    print(f"\nFound {len(results)} unique email(s) on {len(pages)} page(s):")
    for r in results:
        print(f"  {r['email']:35} ({r['type']})")
    print("Saved to emails.json")


main()
