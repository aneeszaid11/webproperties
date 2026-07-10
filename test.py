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

print("Status:", r.status_code)
print("URL:", r.url)

print("\nSERVER:")
print(r.headers.get("Server"))

print("\nHEADERS:")
for k, v in r.headers.items():
    print(f"{k}: {v}")

print("\nBODY:")
print(r.text[:6000])
