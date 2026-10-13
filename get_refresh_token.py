"""
One-Time Helper Script: Get Your YouTube OAuth2 Refresh Token
Sirf 1 baar apne laptop/PC par ye script chalayein taaki aapko `YOUTUBE_REFRESH_TOKEN` mil jaye.
Uske baad GitHub Actions zindagi bhar bina browser khole automatic video upload karega!
"""

import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]


def main():
    print("=" * 65)
    print("🔑 YOUTUBE AUTOMATION — ONE-TIME REFRESH TOKEN GENERATOR")
    print("=" * 65)

    client_secret_file = "client_secret.json"
    if not os.path.exists(client_secret_file):
        print(
            "\n❌ 'client_secret.json' file nahi mili!\n"
            "Kripya Google Cloud Console -> APIs & Services -> Credentials se "
            "OAuth 2.0 Client ID (Desktop App) download karke is folder mein "
            "'client_secret.json' naam se save karein."
        )
        return

    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
    creds = flow.run_local_server(port=8080, prompt="consent", access_type="offline")

    with open(client_secret_file, "r", encoding="utf-8") as f:
        raw = json.load(f)
        info = raw.get("installed") or raw.get("web") or {}

    print("\n" + "=" * 65)
    print("✅ SUCCESS! Niche diye gaye 3 Secrets ko copy karke GitHub Secrets mein daalein:")
    print("=" * 65)
    print(f"\nYOUTUBE_CLIENT_ID:\n{info.get('client_id', creds.client_id)}")
    print(f"\nYOUTUBE_CLIENT_SECRET:\n{info.get('client_secret', creds.client_secret)}")
    print(f"\nYOUTUBE_REFRESH_TOKEN:\n{creds.refresh_token}")
    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()
