from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)

    page = browser.new_page()

    response = page.goto(
        "http://tycoident.com",
        wait_until="networkidle"
    )

    print("Status:", response.status)
    print("Final URL:", page.url)

    browser.close()
