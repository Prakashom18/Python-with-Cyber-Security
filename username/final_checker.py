import json
import time
import requests
from urllib.parse import urlparse

headers = {"User-Agent": "assessment-script/1.0"}
FAKE_NAME = "zzqx9fakeuser123"          # a name nobody has, used for the false-positive check


def get_page(url):
    """Ask for a page. Try up to 3 times. Returns None if every try fails."""
    for attempt in range(3):
        try:
            return requests.get(url, headers=headers, timeout=10)
        except Exception:
            time.sleep(2)               # wait, then retry
    return None


def check_site(site, username):
    """Check one website. Returns (result, link)."""
    link = site["url"].replace("{username}", username)
    response = get_page(link)

    if response is None:
        return "ERROR", link
    code = response.status_code
    if code in (403, 429):
        return "BLOCKED", link          # the site said no: we stop, never bypass
    if code == 404:
        return "NOT_FOUND", link
    if code != 200:
        return "UNCERTAIN", link

    # Sites that answer with a list of matching users
    if site["method"] == "list":
        try:
            return ("FOUND" if len(response.json()) > 0 else "NOT_FOUND"), link
        except Exception:
            return "UNCERTAIN", link

    # Sites where status 200 means "profile exists".
    # Check 1: were we sent to a different website?
    if urlparse(response.url).netloc != urlparse(link).netloc:
        return "UNCERTAIN", link
    # Check 2: does a fake username give the same page? (false-positive check)
    fake = get_page(site["url"].replace("{username}", FAKE_NAME))
    if fake is not None and fake.status_code == 200 \
            and abs(len(fake.text) - len(response.text)) < 50:
        return "UNCERTAIN", link
    return "FOUND", link


sites = json.load(open("sites.json"))

while True:
    username = input("\nUsername to check (press Enter to quit): ").strip()
    if username == "":
        break

    results = []
    for name, site in sites.items():
        result, link = check_site(site, username)
        print(f"{name:10} {result:10} {link}")
        results.append({"site": name, "url": link, "result": result})
        time.sleep(1)                   # rate limit: wait between websites

    counts = {}
    for r in results:
        counts[r["result"]] = counts.get(r["result"], 0) + 1
    print("Summary:", counts)

    safe_name = "".join(c for c in username if c.isalnum() or c in "-_.")
    filename = "results_" + safe_name + ".json"
    with open(filename, "w") as file:
        json.dump({"username": username, "results": results}, file, indent=2)
    print("Saved to", filename)