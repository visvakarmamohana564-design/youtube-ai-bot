"""
Configuration file for YouTube AI Automation Bot ('Hindi Fact' Channel)
- Default Shorts: Hindi Amazing Facts, Psychology, Mystery & Science Facts (Moving AI Video Clips!)
- Default Long Videos: Animated Hindi Horror Stories & Jaadui Kahaniyan (Moving AI Cartoon Animation!)
"""

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")

VOICE_STYLE = os.getenv("VOICE_STYLE", "male")  # "male" or "female"

SHORTS_NICHES = [
    "Dimag Hila Dene Wale Psychology Facts (Human Behavior & Mind Tricks)",
    "Duniya Ke Sabse Bade Rahasya Jo Aaj Tak Solve Nahi Hue (Unsolved Mysteries)",
    "Antariksh (Space) Aur Brahmand Ke Shocking Facts",
    "History Ke Ajeeb Aur Ansune Rahasya (Ancient India & World Facts)",
    "Human Body Aur Vigyan Ke Aise Facts Jo 99% Log Nahi Jaante",
    "Duniya Ki Sabse Ajeeb Jagah Aur Unke Peeche Ka Sach"
]

LONG_VIDEO_NICHES = [
    "Ek Gaon Mein Do Ladkiyan Aur Bhootiya Haveli Ka Rahasya (Animated Hindi Horror Kahani)",
    "Jaadui Jungle Aur Rahasyamayi Pari Ki Kahani (Animated Hindi Jaadui Kahani)",
    "Purani Baoli Aur Raat Ke 12 Baje Ka Khaufnak Sach (Animated Hindi Horror Story)",
    "Garib Kisan Ki Beti Aur Jaadui पेड़ Ka Chamatkar (Animated Hindi Magical Moral Kahani)",
    "Shrapit Gaon Aur Chudail Ka MayaJaal (Animated Hindi Horror & Suspense Kahani)"
]

VIDEO_CONFIG = {
    "shorts": {
        "width": 1080,
        "height": 1920,
        "fps": 24,
        "scene_count": 6,          # ~40-50 seconds vertical Short
        "category_id": "27",
        "privacy_status": "public"
    },
    "long": {
        "width": 1920,
        "height": 1080,
        "fps": 24,
        "scene_count": 10,         # ~3 minutes animated story video
        "category_id": "24",       # Entertainment / Animated Stories
        "privacy_status": "public"
    }
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "topic_history.json")
