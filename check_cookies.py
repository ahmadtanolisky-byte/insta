"""
Debug script — prints actual Instagram API response structure.
Run: python debug.py
"""
from playwright.sync_api import sync_playwright
import json, time
from pathlib import Path

COOKIES_FILE = "ig_cookies.json"
USERNAME     = "natgeo"

def main():
    with open(COOKIES_FILE) as f:
        cookies = json.load(f)

    print(f"Loaded {len(cookies)} cookies")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        context.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
        )
        context.add_cookies(cookies)

        responses = []
        page = context.new_page()

        def handle(response):
            try:
                url = response.url
                # Capture ALL responses not just graphql
                if "instagram.com" in url:
                    ct = response.headers.get("content-type", "")
                    if "json" in ct:
                        try:
                            body = response.json()
                            responses.append({"url": url, "body": body})
                            print(f"  ✓ Captured: {url[:80]}")
                        except Exception:
                            pass
            except Exception:
                pass

        page.on("response", handle)

        # Visit homepage first
        print("\n→ Loading Instagram homepage...")
        page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)

        # Now load the profile
        print(f"→ Loading profile @{USERNAME}...")
        page.goto(f"https://www.instagram.com/{USERNAME}/",
                  wait_until="domcontentloaded", timeout=30000)

        print("→ Waiting 8 seconds for API calls...")
        time.sleep(8)

        # Scroll to trigger more
        print("→ Scrolling to trigger more API calls...")
        for _ in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)

        print(f"\n→ Total responses captured: {len(responses)}")

        # Save everything
        with open("debug_responses.json", "w", encoding="utf-8") as f:
            json.dump(responses, f, indent=2, default=str)
        print("→ Saved to debug_responses.json")

        # Print structure of each response
        print("\n" + "="*60)
        print("RESPONSE STRUCTURES:")
        print("="*60)

        for i, r in enumerate(responses):
            print(f"\n[{i+1}] URL: {r['url'][:90]}")
            body = r["body"]
            if isinstance(body, dict):
                _print_keys(body, depth=1, max_depth=6)
            elif isinstance(body, list):
                print(f"  LIST of {len(body)} items")
                if body and isinstance(body[0], dict):
                    _print_keys(body[0], depth=2, max_depth=5)

        # Also check what the page HTML contains
        content = page.content()
        print(f"\n→ Page HTML size: {len(content)} chars")
        if "sessionid" in content or "ds_user_id" in content:
            print("→ Session data found in page HTML ✓")
        else:
            print("→ No session data in page HTML — may not be logged in")

        # Check if we're actually logged in
        logged_in_indicators = [
            "Log in", "Log In", "loginPage", "accounts/login"
        ]
        for indicator in logged_in_indicators:
            if indicator in content:
                print(f"⚠ Found login indicator in page: '{indicator}'")
                break
        else:
            print("→ No login wall detected ✓")

        browser.close()


def _print_keys(obj, depth=0, max_depth=6):
    if depth > max_depth:
        return
    indent = "  " * depth
    if isinstance(obj, dict):
        for k, v in list(obj.items())[:30]:  # limit to 30 keys
            if isinstance(v, list):
                item_info = ""
                if v and isinstance(v[0], dict):
                    item_info = f" → item keys: {list(v[0].keys())[:8]}"
                print(f"{indent}{k}: LIST[{len(v)}]{item_info}")
                if v and isinstance(v[0], dict) and depth < max_depth:
                    _print_keys(v[0], depth+1, max_depth)
            elif isinstance(v, dict):
                print(f"{indent}{k}: {{")
                _print_keys(v, depth+1, max_depth)
            else:
                print(f"{indent}{k}: {str(v)[:80]}")
    elif isinstance(obj, list):
        print(f"{indent}LIST[{len(obj)}]")
        if obj and isinstance(obj[0], dict):
            _print_keys(obj[0], depth+1, max_depth)


if __name__ == "__main__":
    main()