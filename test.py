from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="msedge",
        headless=False
    )

    page = browser.new_page()
    page.goto("http://tycoident.com")

    print(page.url)

    browser.close()
