import requests

proxies = {
    "http": "http://restrictedproxy.connect.te.com:80",
    "https": "http://restrictedproxy.connect.te.com:80"
}

r = requests.get(
    "https://tycoident.com",
    timeout=40,
    allow_redirects=True,
    verify=False,
    proxies=proxies
)

print("Status:", r.status_code)
print("Final URL:", r.url)

for h in r.history:
    print(h.status_code, h.url)
