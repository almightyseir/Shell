import requests

url = "https://engine.hyperbeam.com/v0/vm"

payload = {
    "start_url": "https://render.com/",
    "kiosk": False
}
headers = {
    "Authorization": "Bearer sk_live_bHsQyqOOHDIb33YaQuuhOpHqIO4_JFG7TS7aUmyVnlY",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)