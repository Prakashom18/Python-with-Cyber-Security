import time
import requests

domain = input("Enter domain: ")

crtsh_names = set()
spotter_names = set()

# Source 1: crt.sh (slow sometimes, so we try up to 3 times)
url = "https://crt.sh/?q=%." + domain + "&output=json"
data = []
for attempt in range(3):
    try:
        response = requests.get(url, timeout=60)
        data = response.json()        # fails if the site sent an error page
        break
    except Exception:
        print("crt.sh failed (attempt", attempt + 1, "of 3), waiting 5 seconds...")
        time.sleep(5)

for item in data:
    for name in item["name_value"].split("\n"):
        name = name.replace("*.", "").lower()
        if name == domain or name.endswith("." + domain):
            crtsh_names.add(name)

# Source 2: Cert Spotter (a backup Certificate Transparency source)
try:
    url2 = ("https://api.certspotter.com/v1/issuances?domain=" + domain
            + "&include_subdomains=true&expand=dns_names")
    response = requests.get(url2, timeout=30)
    for item in response.json():
        for name in item["dns_names"]:
            name = name.replace("*.", "").lower()
            if name == domain or name.endswith("." + domain):
                spotter_names.add(name)
except Exception:
    print("Cert Spotter failed")

all_names = sorted(crtsh_names | spotter_names)   # | joins the two sets, no duplicates

print("crt.sh found:", len(crtsh_names))
print("Cert Spotter found:", len(spotter_names))
print("Total unique:", len(all_names))

with open("subdomains.txt", "w") as file:
    for name in all_names:
        print(name)
        file.write(name + "\n")