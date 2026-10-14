"""
Configuration file for YouTube AI Automation Bot (100% Educational Long Videos — MP Board Class 10th NCERT)
- Mode: ONLY Long Videos (16:9 Full HD, 1920x1080) — Shorts Disabled
- Purpose: Educational Purpose (YouTube Category ID = '27' Education)
- Curriculum: MP Board Class 10th NCERT (Hindi Kshitij-2 & Kritika-2, English First Flight, Science/Vigyan, Social Science/SST)
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

# Complete MP Board Class 10th NCERT Chapter Queue for Automatic Daily Long Videos
LONG_VIDEO_NICHES = [
    # हिंदी (क्षितिज भाग-2 — गद्य खंड एवं काव्य खंड)
    "MP Board कक्षा 10 हिंदी (क्षितिज भाग-2) — पाठ 10: नेताजी का चश्मा (स्वयं प्रकाश) | मूल पाठ वाचन और अंदर की बातों की सरल व्याख्या",
    "MP Board कक्षा 10 हिंदी (क्षितिज भाग-2) — पाठ 11: बालगोबिन भगत (रामवृक्ष बेनीपुरी) | मूल पाठ वाचन और संपूर्ण व्याख्या",
    "MP Board कक्षा 10 हिंदी (क्षितिज भाग-2) — पाठ 12: लखनवी अंदाज़ (यशपाल) | मूल पाठ वाचन, व्यंग्य और अंदर की बातें",
    "MP Board कक्षा 10 हिंदी (क्षितिज भाग-2) — पाठ 14: एक कहानी यह भी (मन्नू भंडारी) | मूल पाठ वाचन और सरल व्याख्या",
    "MP Board कक्षा 10 हिंदी (क्षितिज भाग-2 काव्य खंड) — पाठ 1: सूरदास के पद (ऊधो, तुम हौ अति बड़भागी) | मूल पद वाचन और भावार्थ",
    "MP Board कक्षा 10 हिंदी (क्षितिज भाग-2 काव्य खंड) — पाठ 2: तुलसीदास (राम-लक्ष्मण-परशुराम संवाद) | मूल चौपाई वाचन और सरल अर्थ",
    "MP Board कक्षा 10 हिंदी (क्षितिज भाग-2 काव्य खंड) — पाठ 5: सूर्यकांत त्रिपाठी 'निराला' (उत्साह और अट नहीं रही है) | कविता वाचन और गूढ़ अर्थ",
    "MP Board कक्षा 10 हिंदी (कृतिका भाग-2) — पाठ 1: माता का अँचल (शिवपूजन सहाय) | मूल पाठ वाचन और अंदर की मर्मस्पर्शी बातें",

    # English (First Flight & Footprints Without Feet — Explained in Hindi)
    "MP Board Class 10 NCERT English (First Flight) — Chapter 1: A Letter to God (G.L. Fuentes) | Text Reading & Deep Hindi Explanation",
    "MP Board Class 10 NCERT English (First Flight) — Chapter 2: Nelson Mandela: Long Walk to Freedom | Text Reading & Hindi Explanation",
    "MP Board Class 10 NCERT English (First Flight) — Poem: Dust of Snow & Fire and Ice (Robert Frost) | Stanza Reading & Deep Meaning in Hindi",
    "MP Board Class 10 NCERT English (First Flight) — Chapter 4: From the Diary of Anne Frank | Text Reading & Hindi Explanation",

    # विज्ञान (Science — NCERT Hindi Medium)
    "MP Board कक्षा 10 विज्ञान (NCERT Science) — अध्याय 1: रासायनिक अभिक्रियाएँ एवं समीकरण | एनसीईआरटी पाठ वाचन, सूत्र और सरल व्याख्या",
    "MP Board कक्षा 10 विज्ञान (NCERT Science) — अध्याय 2: अम्ल, क्षारक एवं लवण | एनसीईआरटी पाठ वाचन, उदाहरण और परीक्षा बिंदु",
    "MP Board कक्षा 10 विज्ञान (NCERT Science) — अध्याय 5: जैव प्रक्रम (पोषण, श्वसन, वहन और उत्सर्जन) | एनसीईआरटी पाठ वाचन और सरल व्याख्या",
    "MP Board कक्षा 10 विज्ञान (NCERT Science) — अध्याय 9: प्रकाश — परावर्तन तथा अपवर्तन | एनसीईआरटी पाठ वाचन और अंदर के नियम",

    # सामाजिक विज्ञान (Social Science — History, Geography, Civics, Economics)
    "MP Board कक्षा 10 सामाजिक विज्ञान (इतिहास) — अध्याय 1: यूरोप में राष्ट्रवाद का उदय | एनसीईआरटी पाठ वाचन और सरल व्याख्या",
    "MP Board कक्षा 10 सामाजिक विज्ञान (इतिहास) — अध्याय 2: भारत में राष्ट्रवाद (महात्मा गांधी और जन आंदोलन) | पाठ वाचन और अंदर की बातें",
    "MP Board कक्षा 10 सामाजिक विज्ञान (भूगोल) — अध्याय 1: संसाधन एवं विकास | एनसीईआरटी पाठ वाचन, प्रकार और परीक्षा उपयोगी व्याख्या"
]

# Legacy alias so any import of SHORTS_NICHES also points to Educational Long Video Niches
SHORTS_NICHES = LONG_VIDEO_NICHES

VIDEO_CONFIG = {
    "long": {
        "width": 1920,
        "height": 1080,
        "fps": 24,
        "scene_count": 5,          # 5 comprehensive chapter sections (Each = Book Reading + Deep Explanation, ~6-8 mins total)
        "category_id": "27",       # 27 = YouTube Official 'Education' Category!
        "privacy_status": "public"
    },
    # Fallback alias in case 'shorts' key is ever referenced: still renders 16:9 1080p Educational Long Video!
    "shorts": {
        "width": 1920,
        "height": 1080,
        "fps": 24,
        "scene_count": 5,
        "category_id": "27",       # 27 = Education
        "privacy_status": "public"
    }
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "topic_history.json")
