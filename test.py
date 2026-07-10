import os

import requests

print("HTTP_PROXY =", os.environ.get("HTTP_PROXY"))
print("HTTPS_PROXY =", os.environ.get("HTTPS_PROXY"))

try:
    r = requests.get(
        "https://tycoident.com",
        timeout=30,
        allow_redirects=True
    )
    print(r.status_code)
    print(r.url)

except requests.exceptions.ProxyError as e:
    print("PROXY ERROR:", e)

except requests.exceptions.ConnectionError as e:
    print("CONNECTION ERROR:", e)

except Exception as e:
    print("ERROR:", e)
