from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
import json

def run(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        captured = []

        def on_response(resp):
            ct = (resp.headers.get("content-type") or "").lower()
            if "application/json" in ct:
                try:
                    data = resp.json()
                    captured.append((resp.url, data))
                except Exception:
                    pass

        page.on("response", on_response)

        page.goto(url, wait_until="networkidle", timeout=60_000)

        browser.close()
        return captured

if __name__ == "__main__":
    URL = "https://www.dbschenker.com/app/tracking-public/?refNumber=SENYB550963616"
    results = run(URL)

    print(f"Captured {len(results)} JSON responses\n")
    for u, data in results[:5]:
        print("URL:", u)
        print(json.dumps(data, indent=2)[:2000])
        print("-" * 60)
