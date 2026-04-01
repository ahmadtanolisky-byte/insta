"""
Run this ONCE to create your Instagram session file.
Usage:  python setup_session.py
"""
import instaloader, getpass, os, sys

SESSION_FILE = "ig_session"   # instaloader uses username-based filename

L = instaloader.Instaloader(
    quiet=False,
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False,
    post_metadata_txt_pattern='',
    request_timeout=30,
    max_connection_attempts=2,
)

print("=" * 55)
print("  InstaViral — One-time Session Setup")
print("=" * 55)
print("\nThis creates a session file so the app never needs")
print("to log in again. Run this once, then use app.py.\n")
print("TIP: Use a throwaway/dummy Instagram account here.")
print("     Make sure 2FA is DISABLED on that account.\n")

username = input("Instagram username: ").strip().lstrip("@")
password = getpass.getpass("Instagram password (hidden): ").strip()

if not username or not password:
    print("\n✗ Username and password are required.")
    sys.exit(1)

print(f"\n→ Logging in as @{username} ...")

try:
    L.login(username, password)
    L.save_session_to_file(f"{username}_session")
    print(f"\n✓ Session saved to:  {username}_session")
    print(f"\nNow open app.py and set:")
    print(f'   IG_USERNAME = "{username}"')
    print(f'   SESSION_FILE = "{username}_session"')
    print("\nThen run:  python app.py\n")

except instaloader.exceptions.BadCredentialsException:
    print("\n✗ Wrong username or password. Try again.")
except instaloader.exceptions.TwoFactorAuthRequiredException:
    print("\n✗ 2FA is enabled. Disable it on Instagram first, then re-run this script.")
except instaloader.exceptions.ConnectionException as e:
    print(f"\n✗ Connection error: {e}")
    print("\nInstagram may have flagged this login attempt.")
    print("Wait 30 minutes and try again, or try on a different network.")
except Exception as e:
    print(f"\n✗ Error: {e}")