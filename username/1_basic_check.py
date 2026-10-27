import json
import requests

username = input("Username: ")
sites = json.load(open("sites.json"))          # read the website list from the file

for name, url in sites.items():
    link = url.replace("{username}", username)  # put the username into the link
    try:
        response = requests.get(link, timeout=10)   # wait at most 10 seconds
        if response.status_code == 200:
            print(name, "-> FOUND (username is taken)")
        elif response.status_code == 404:
            print(name, "-> NOT FOUND (username is probably free)")
        else:
            print(name, "-> UNSURE, status", response.status_code)
    except requests.Timeout:
        print(name, "-> TIMEOUT")
    except Exception:
        print(name, "-> ERROR")