import requests

url = input("Full URL, for example https://github.com/torvalds: ")
response = requests.get(url, timeout=10)    

for step in response.history:              
    print("Redirected from:", step.url)

print("Asked for :", url)
print("Landed on :", response.url)

if response.url.rstrip("/") != url.rstrip("/"):
    print("Warning: different page than we asked for, so don't trust a 200 blindly")