import json
import time
import requests

username = input("Username: ")
sites = json.load(open("sites.json"))
headers = {"User-Agent": "Mozilla/5.0 (assessment script)"}
results = []

for name, url in sites.items():
    link = url.replace("{username}", username)
    fake_link = url.replace("{username}", "zzqx9fakeuser123")
    status = "ERROR"

    for attempt in range(3):                       # retry up to 3 times
        try:
            real = requests.get(link, headers=headers, timeout=10)
            fake = requests.get(fake_link, headers=headers, timeout=10)

            if real.status_code in (403, 429):
                status = "BLOCKED"                 # the site refused us, so we stop
            elif real.status_code == 404:
                status = "NOT_FOUND"
            elif real.status_code == 200:
                looks_like_fake = (fake.status_code == 200
                                   and abs(len(real.text) - len(fake.text)) < 50)
                if looks_like_fake:
                    status = "UNCERTAIN"
                elif username.lower() in real.url.lower():
                    status = "FOUND"
                else:
                    status = "UNCERTAIN"           # redirected somewhere else
            else:
                status = "UNCERTAIN"
            break                                  # got an answer, stop retrying
        except Exception:
            time.sleep(2)                          # wait and try again

    print(name, "->", status)
    results.append({"site": name, "url": link, "status": status})
    time.sleep(1)                                  # rate limit between sites

with open("username_results.json", "w") as file:
    json.dump(results, file, indent=2)
print("Saved to username_results.json")