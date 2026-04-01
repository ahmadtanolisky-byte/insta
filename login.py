"""
InstaViral — One-time Manual Login
====================================
Run this ONCE to save your Instagram session cookies.
After this, app.py uses the saved cookies automatically.
Users never need to log in.

Usage:
    python login.py

Requirements:
    pip install playwright
    playwright install chromium
"""

from playwright.sync_api import sync_playwright
import json, time
from pathlib import Path

COOKIES_FILE = "ig_cookies.json"

def main():
    print("\n" + "=" * 55)
    print("  InstaViral — One-time Instagram Login")
    print("=" * 55)
    print("\n  A real Chrome window will open.")
    print("  Log into Instagram manually with your account.")
    print("  Once you can see your Instagram home feed,")
    print("  come back here and press ENTER to save the session.")
    print("\n  TIP: Use a dedicated dummy account, not")
    print("       your personal account.\n")
    input("  Press ENTER to open the browser...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = browser.new_context(
            viewport=None,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            locale="en-US",
        )

        page = context.new_page()
        page.goto("https://www.instagram.com/accounts/login/",
                  wait_until="domcontentloaded")

        print("\n  ✓ Browser is open.")
        print("  → Log into Instagram in the browser window now.")
        print("  → Wait until you can fully see your home feed.")
        print("  → Then come back to this terminal window.\n")

        # User controls when to save — most reliable method
        input("  Press ENTER here after you are fully logged in...")

        print("\n  → Saving session cookies, please wait...")
        time.sleep(3)  # let any final cookies settle

        cookies = context.cookies()

        if not cookies:
            print("\n  ✗ No cookies found.")
            print("    Make sure you logged in successfully and try again.")
            browser.close()
            return

        # Verify Instagram session cookies are present
        cookie_names = [c["name"] for c in cookies]
        has_session  = any(n in cookie_names for n in ["sessionid", "ds_user_id", "csrftoken"])

        if not has_session:
            print("\n  ✗ Instagram session cookie not found.")
            print("    Make sure you are fully logged into Instagram, then try again.")
            browser.close()
            return

        # Save cookies to file
        with open(COOKIES_FILE, "w") as f:
            json.dump(cookies, f, indent=2)

        print(f"  ✓ {len(cookies)} cookies saved to: {COOKIES_FILE}")

        # Show logged-in user ID as confirmation
        user_id = next((c["value"] for c in cookies if c["name"] == "ds_user_id"), None)
        if user_id:
            print(f"  ✓ Instagram user ID: {user_id}")

        browser.close()

    print("\n" + "=" * 55)
    print("  Setup complete!")
    print("=" * 55)
    print("\n  Now run:  python app.py")
    print("  Open:     http://127.0.0.1:5000\n")
    print("  Your team can scrape any public account.")
    print("  Users never need to log in.\n")
    print("  NOTE: Re-run login.py if scraping stops working.")
    print("        Cookies expire every 3-6 months.\n")


if __name__ == "__main__":
    main()