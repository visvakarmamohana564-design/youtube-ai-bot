"""
Automated YouTube Data API v3 Uploader + Multi-Channel Switcher Support
- Reads active channel credentials from channel_config.json (if set from Mobile App)
  or falls back to environment variables / config.py
- Uploads MP4 with SEO Title, Description, Tags, Category & Custom Thumbnail
"""

import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHANNEL_CFG_PATH = os.path.join(BASE_DIR, "channel_config.json")


def _load_active_credentials():
    client_id = config.YOUTUBE_CLIENT_ID or os.environ.get("YOUTUBE_CLIENT_ID", "")
    client_secret = config.YOUTUBE_CLIENT_SECRET or os.environ.get("YOUTUBE_CLIENT_SECRET", "")
    refresh_token = config.YOUTUBE_REFRESH_TOKEN or os.environ.get("YOUTUBE_REFRESH_TOKEN", "")

    if os.path.exists(CHANNEL_CFG_PATH):
        try:
            with open(CHANNEL_CFG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("refresh_token_rev"):
                refresh_token = data["refresh_token_rev"][::-1]
            if data.get("client_id_rev"):
                client_id = data["client_id_rev"][::-1]
            if data.get("client_secret_rev"):
                client_secret = data["client_secret_rev"][::-1]
        except Exception as e:
            print(f"ℹ️ channel_config.json read note: {e}")

    return client_id, client_secret, refresh_token


def get_youtube_service():
    client_id, client_secret, refresh_token = _load_active_credentials()
    if not (client_id and client_secret and refresh_token):
        raise ValueError("YouTube API Credentials missing!")

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=[
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube"
        ]
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)


def upload_to_youtube(
    video_path: str,
    thumbnail_path: str,
    plan: dict,
    video_type: str = "shorts",
    publish_at_iso: str = None
) -> str:
    youtube = get_youtube_service()
    cfg = config.VIDEO_CONFIG[video_type]

    title = plan.get("title", "Amazing Hindi Facts #shorts")[:100]
    description = plan.get("description", "")
    tags = plan.get("tags", ["hindi fact", "hindi facts", "rahasya", "shorts"])

    if video_type == "shorts" and "#shorts" not in title.lower():
        if len(title) <= 91:
            title = f"{title} #shorts"

    status_body = {
        "selfDeclaredMadeForKids": False
    }

    if publish_at_iso:
        status_body["privacyStatus"] = "private"
        status_body["publishAt"] = publish_at_iso
    else:
        status_body["privacyStatus"] = cfg.get("privacy_status", "public")

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": cfg.get("category_id", "27"),
            "defaultLanguage": "hi",
            "defaultAudioLanguage": "hi"
        },
        "status": status_body
    }

    print(f"\n📤 Uploading '{title}' to YouTube...")
    media = MediaFileUpload(video_path, chunksize=1024 * 1024 * 5, resumable=True, mimetype="video/mp4")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    try:
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"   Upload progress: {int(status.progress() * 100)}%")
    except Exception as e:
        if "uploadLimitExceeded" in str(e):
            print("⚠️ YouTube 24-Hour Daily Upload Limit reached for this channel! Video will auto-upload on next scheduled slot once the 24h window resets.")
            return "PENDING_DAILY_LIMIT_RESET"
        raise

    video_id = response["id"]
    print(f"✅ Video Successfully Uploaded! YouTube Link: https://youtu.be/{video_id}")

    if thumbnail_path and os.path.exists(thumbnail_path) and video_type == "long":
        try:
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path, mimetype="image/jpeg")
            ).execute()
            print("✅ Custom Thumbnail Set!")
        except Exception as e:
            print(f"⚠️ Custom thumbnail note (requires phone verification in YT Studio): {e}")

    first_comment = plan.get(
        "first_comment",
        "🔥 आपको यह वीडियो कैसा लगा? कमेंट में अपनी राय ज़रूर बताएं और चैनल को Subscribe करें! 👇"
    )
    if status_body.get("privacyStatus") == "public":
        try:
            youtube.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": video_id,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": first_comment
                            }
                        }
                    }
                }
            ).execute()
            print("💬 Auto-Posted Viral First Comment on Video!")
        except Exception as e:
            print(f"ℹ️ First comment skipped ({e})")

    return video_id
