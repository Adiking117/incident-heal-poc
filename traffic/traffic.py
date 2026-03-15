import requests
import time

url = "http://localhost:5000/payment"

while True:
    try:
        r = requests.get(url)
        print(r.text)
    except:
        print("error")

    time.sleep(2)