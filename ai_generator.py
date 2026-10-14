"""
MP Board Class 10th NCERT Educational Long Video Script & Smart-Board Plan Generator
- 100% Educational Purpose (YouTube Category 27: Education)
- ONLY Long-Form 16:9 Full HD Chapter Explanation Videos (No Shorts)
- Every section includes:
  1. 📖 NCERT मूल पाठ वाचन (Actual chapter text/stanza/concept reading)
  2. 💡 अंदर की बातों की सरल व्याख्या (Deep meaning, hidden message, examples, word meanings, and MP Board Exam IMP Questions)
"""

import json
import random
import os
import time
import requests
import config


def load_used_topics() -> list:
    if os.path.exists(config.HISTORY_FILE):
        try:
            with open(config.HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data[-45:]
        except Exception:
            return []
    return []


def save_used_topic(title: str):
    topics = load_used_topics()
    topics.append(title)
    with open(config.HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(topics[-70:], f, ensure_ascii=False, indent=2)


def generate_video_plan(video_type: str = "long", custom_topic: str = None) -> dict:
    # Force Long Educational Video format
    video_type = "long"

    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY nahi mila!")

    used_topics = load_used_topics()

    if custom_topic and custom_topic.strip():
        chosen_niche = custom_topic.strip()
    else:
        unused = [t for t in config.LONG_VIDEO_NICHES if t not in used_topics]
        chosen_niche = random.choice(unused if unused else config.LONG_VIDEO_NICHES)

    section_count = config.VIDEO_CONFIG["long"]["scene_count"]

    prompt = f"""
You are Madhya Pradesh's #1 Class 10th MP Board NCERT Master Teacher (Expert in Hindi Kshitij/Kritika, English First Flight, Science/Vigyan, and Social Science/SST).
Selected Chapter / Topic: {chosen_niche}

Previously covered chapters (pick the next fresh chapter if no specific chapter was forced):
{json.dumps(used_topics[-15:], ensure_ascii=False)}

Create a COMPLETE, HIGH-RETENTION, EDUCATIONAL LONG VIDEO (16:9 Full HD, ~6 to 8 minutes) for Class 10th MP Board NCERT students.
TEACHING METHODOLOGY ("Chapter ko padhenge aur use samjhaenge uske andar ki baten"):
- Divide the chapter into {section_count} sequential sections (`scenes`) covering the chapter from start to finish.
- In EVERY section (`scene`), you MUST provide two distinct teaching phases:
  1. **NCERT मूल पाठ वाचन (`book_text` + `read_audio`):**
     - `book_heading`: e.g. `"★ NCERT मूल पाठ (गद्यांश 1):"` or `"★ NCERT Stanza / Text (Part 1):"`
     - `book_text`: 45 to 65 words of the authentic NCERT textbook passage / poem lines / key scientific text in Devanagari Hindi (or English text + Hindi reading for English chapters) to display on the Left Smart-Board Panel.
     - `read_audio`: 55 to 75 words in natural spoken Hindi (Devanagari script) where the teacher introduces the section and reads the NCERT passage clearly aloud.
  2. **अंदर की बातों की सरल व्याख्या (`inside_points` + `explain_audio`):**
     - `inside_heading`: `"★ अंदर की बातें और सरल व्याख्या (Deep Meaning):"`
     - `inside_points`: A list of 4 clear Hindi bullet points (using `• <b>मुख्य बिंदु:</b> विवरण...`) explaining the hidden meaning, character psychology / scientific logic, real-life example, and `कठिन शब्दार्थ (Word Meanings)` to display on the Right Smart-Board Panel.
     - `exam_tip`: `"★ MP Board IMP प्रश्न: ..."` (1 most important MP Board Class 10 exam question from this section).
     - `explain_audio`: 65 to 85 words in warm, conversational spoken Hindi (Devanagari script) where the teacher explains all the deep meanings ("अंदर की असली बातें") and answers the MP Board exam question in simple words!

Return ONLY valid JSON matching this exact structure:
{{
  "title": "MP Board कक्षा 10 NCERT: [Chapter Name] | मूल पाठ वाचन और संपूर्ण सरल व्याख्या 📚✨",
  "subject_header": "MP BOARD कक्षा 10वीं NCERT  |  [Subject & Chapter Name]",
  "description": "Full SEO optimized Educational YouTube description in Hindi for Class 10 MP Board NCERT students with chapter summary, key topics, MP Board important questions, and 15 educational hashtags (#mpboard #class10 #ncert #mpboardclass10 #hindimedium #boardexam)",
  "tags": ["mp board class 10", "ncert class 10 hindi medium", "mp board 10th", "class 10 chapter explanation", "mp board pariksha", "kshitij class 10", "class 10 vigyan", "class 10 samajik vigyan", "first flight class 10 in hindi"],
  "first_comment": "📚 विद्यार्थियों! इस अध्याय का कौन-सा भाग आपको सबसे अच्छे से समझ आया? अगला वीडियो किस चैप्टर पर चाहिए, कमेंट में ज़रूर लिखें! 👇",
  "thumbnail_text": "कक्षा 10 NCERT संपूर्ण व्याख्या",
  "scenes": [
    {{
      "scene_number": 1,
      "title": "भाग 1: [Section Title in Hindi]",
      "search_query": "2-3 simple English keywords for scene illustration (e.g. 'indian village school', 'subhash chandra bose statue', 'science laboratory chemistry')",
      "book_heading": "★ NCERT मूल पाठ (भाग 1):",
      "book_text": "Authentic NCERT passage / lines in Hindi Devanagari...",
      "inside_heading": "★ अंदर की बातें और सरल व्याख्या (Deep Meaning):",
      "inside_points": [
        "• <b>मुख्य बात 1:</b> सरल शब्दों में व्याख्या...",
        "• <b>असली रहस्य / गहरा अर्थ:</b> लेखक/अध्याय क्या समझाना चाहता है...",
        "• <b>उदाहरण / संदेश:</b> विद्यार्थियों के लिए मुख्य सीख...",
        "• <b>कठिन शब्दार्थ:</b> शब्द 1 = अर्थ 1  |  शब्द 2 = अर्थ 2  |  शब्द 3 = अर्थ 3"
      ],
      "exam_tip": "★ MP Board IMP प्रश्न: [Important Board Exam Question from this section?]",
      "read_audio": "Pure natural spoken Hindi text in Devanagari script reading the NCERT passage aloud...",
      "explain_audio": "Pure natural spoken Hindi text in Devanagari script explaining the deep meaning and inside points..."
    }}
  ]
}}
"""

    candidate_models = [
        "gemini-flash-latest",
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-flash-lite-latest",
        "gemini-3.1-flash-lite",
        "gemini-2.5-flash-lite"
    ]

    last_error = None
    for attempt in range(2):
        for model_name in candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={config.GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "temperature": 0.75
                }
            }
            try:
                resp = requests.post(url, json=payload, timeout=50)
                if resp.status_code == 200:
                    data = resp.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    plan = json.loads(raw_text)
                    save_used_topic(plan.get("title", chosen_niche))
                    return plan
                else:
                    last_error = f"{model_name} HTTP {resp.status_code}: {resp.text[:160]}"
                    time.sleep(2)
            except Exception as e:
                last_error = str(e)
                time.sleep(2)
        time.sleep(4)

    raise RuntimeError(f"Gemini API failed across all models. Last error: {last_error}")
