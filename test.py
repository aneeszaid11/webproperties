import requests

proxies = {
    "http": "http://restrictedproxy.connect.te.com:80",
    "https": "http://restrictedproxy.connect.te.com:80"
}

r = requests.get(
    "http://tycoident.com",
    timeout=40,
    allow_redirects=True,
    proxies=proxies
)

print(r.status_code)
print(r.url)

for h in r.history:
    print(h.status_code, h.url)
