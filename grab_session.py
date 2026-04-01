"""
Grabs your Instagram session directly from your browser cookies.
Make sure you're logged into Instagram in Chrome or Firefox first.
"""
import instaloader
import browser_cookie3

username = input("Enter your Instagram username: ").strip().lstrip("@")

L = instaloader.Instaloader(
    quiet=False,
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
)

print("\n→ Trying Chrome cookies...")
try:
    cookies = browser_cookie3.chrome(domain_name=".instagram.com")
    import requests
    L.context._session.cookies.update(cookies)
    L.context.username = username
    L.save_session_to_file(f"{username}_session")
    print(f"\n✓ Session saved to: {username}_session")
    print(f"\nNow open app.py and set:")
    print(f'   IG_USERNAME  = "{username}"')
    print(f'   SESSION_FILE = "{username}_session"')
    print("\nThen run: python app.py\n")
except Exception as e:
    print(f"Chrome failed: {e}")
    print("\n→ Trying Firefox cookies...")
    try:
        cookies = browser_cookie3.firefox(domain_name=".instagram.com")
        L.context._session.cookies.update(cookies)
        L.context.username = username
        L.save_session_to_file(f"{username}_session")
        print(f"\n✓ Session saved to: {username}_session")
        print(f"\nNow open app.py and set:")
        print(f'   IG_USERNAME  = "{username}"')
        print(f'   SESSION_FILE = "{username}_session"')
        print("\nThen run: python app.py\n")
    except Exception as e2:
        print(f"\n✗ Firefox also failed: {e2}")
        print("\nMake sure you are logged into Instagram in Chrome or Firefox first.")