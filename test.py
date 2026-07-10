import requests

try:
    r = requests.get(
        "https://nevalo.com",
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
