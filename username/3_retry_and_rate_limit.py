import time
import requests

url = input("Full URL: ")

for attempt in range(3):                   
    try:
        response = requests.get(url, timeout=10)
        print("Worked! Status:", response.status_code)
        break                               
    except Exception:
        print("Attempt", attempt + 1, "failed, waiting 2 seconds...")
        time.sleep(2)                       

time.sleep(1)                              