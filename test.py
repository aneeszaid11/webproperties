from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="msedge",
        headless=True
    )

    page = browser.new_page()

    page.goto("https://www.microsoft.com", timeout=60000)

    print("Microsoft URL:", page.url)
    print("Title:", page.title())

    page.goto("https://tycoident.com", timeout=60000)
  
    print("Tycoident URL:", page.url)
    print("Title:", page.title())

    browser.close()
