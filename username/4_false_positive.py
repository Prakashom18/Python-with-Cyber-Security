import requests

url = input("URL with {username}, for example https://github.com/{username}: ")
username = input("Username to check: ")

real = requests.get(url.replace("{username}", username), timeout=10)
fake = requests.get(url.replace("{username}", "zzqx9fakeuser123"), timeout=10)

print("Real user page:", real.status_code, "size", len(real.text))
print("Fake user page:", fake.status_code, "size", len(fake.text))

same_status = real.status_code == fake.status_code
similar_size = abs(len(real.text) - len(fake.text)) < 50

if real.status_code == 404:
    print("NOT FOUND")
elif same_status and similar_size:
    print("UNCERTAIN: looks the same as a page for a fake user")
elif real.status_code == 200:
    print("FOUND")
else:
    print("UNCERTAIN")