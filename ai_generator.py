"""
Viral AI Script, Title, Description, First-Comment & Moving Animation Prompt Generator
Engineered for Maximum YouTube Algorithm Retention (APV > 95% & High CTR):
- Instant 2-Second Curiosity/Shock Hook (Zero intro fluff)
- Open-loop storytelling across every scene
- Auto-generated engaging First Comment to boost comment velocity
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


def generate_video_plan(video_type: str = "shorts", custom_topic: str = None) -> dict:
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY nahi mila!")

    used_topics = load_used_topics()

    if custom_topic and custom_topic.strip():
        chosen_niche = custom_topic.strip()
    else:
        niches = config.SHORTS_NICHES if video_type == "shorts" else config.LONG_VIDEO_NICHES
        chosen_niche = random.choice(niches)

    scene_count = config.VIDEO_CONFIG[video_type]["scene_count"]

    if video_type == "shorts":
        format_instructions = f"""
        Create an ULTRA-VIRAL, HIGH-RETENTION YouTube Short (Vertical 9:16, 35-45 seconds) in Hindi for channel 'Hindi Fact'.
        Topic/Theme: {chosen_niche}
        VIRAL ALGORITHM RULES:
        - Must have exactly {scene_count} fast-paced scenes.
        - NEVER start with "Namaste dosto" or "Kya aapko pata hai". Start Scene 1 with an IMMEDIATE 2-second shock/danger/curiosity hook (e.g., "अगर आपको कभी रात के 3 बजे ये आवाज़ सुनाई दे, तो...", "वैज्ञानिकों ने जब इस बंद कमरे को खोला, तो उनके होश उड़ गए...").
        - Each scene's `narration_hindi` MUST be 14 to 19 words in natural spoken Hindi (Devanagari script) with suspenseful transitions ("लेकिन असली रहस्य तो इसके बाद शुरू हुआ...").
        - Each scene's `subtitle_hinglish` MUST be 5 to 8 words in ALL CAPS Roman Hinglish.
        - Final scene must deliver a goosebumps twist and ask a specific 2-choice question so viewers comment!
        - Set `visual_style` to `"cartoon"` when showing animated characters/stories, or `"realistic"` for cinematic mystery/science visuals.
        - Title MUST be < 85 chars, super clickable in Hindi + Hinglish, ending with #shorts #hindifacts #viral
        """
    else:
        format_instructions = f"""
        Create a BINGE-WORTHY, ANIMATED Long-form Hindi Kahani (Cartoon Story) Video (Horizontal 16:9, ~3 minutes) in Hindi for channel 'Hindi Fact'.
        Story Genre/Theme: {chosen_niche} (Animated Hindi Horror Kahani OR Animated Jaadui Kahani).
        VIRAL STORYTELLING RULES:
        - Must have exactly {scene_count} vivid animated storytelling scenes.
        - Scene 1 MUST start right in the middle of a mysterious or thrilling moment in an Indian village, haunted haveli, or magical forest (zero boring intro!).
        - Define a consistent `character_appearance` (e.g. "two Indian village girls Radha in red lehenga and Meena in green saree, 3D Pixar Disney cartoon animation style") and include it in every `video_prompt` with clear walking/moving actions ("walking forward on a village path", "holding a glowing lantern in spooky night", "running from a ghostly shadow", "discovering a glowing magical tree").
        - Set `visual_style` to `"cartoon"` for all scenes.
        - Also include `setting` ("village_day", "village_night", "haunted_haveli", "dark_jungle", "magical_forest", or "jaadui_cave") and `characters` list.
        - Each scene's `narration_hindi` should be 28 to 36 words in expressive, suspenseful spoken Hindi (Devanagari script).
        - Each scene's `subtitle_hinglish` should be a dramatic 1-line caption in Hinglish (Roman script, max 8 words, ALL CAPS).
        """

    prompt = f"""
You are India's #1 Viral YouTube Scriptwriter & Growth Strategist (expert in 10M+ views Hindi Shorts & Animated Kahaniyan).
Selected Theme: {chosen_niche}

Previously covered titles/topics (DO NOT repeat these):
{json.dumps(used_topics, ensure_ascii=False)}

{format_instructions}

Return ONLY valid JSON matching this exact structure:
{{
  "title": "High-CTR Viral Title in Hindi/Hinglish with 2 emojis",
  "description": "Full SEO optimized YouTube description in Hindi & Hinglish with curiosity hook, timestamps/bullets, and 15 viral hashtags (#hindifacts #shorts #hindikahani #horrorstory #jaaduikahani #rahasya #viral)",
  "tags": ["hindi fact", "hindi facts", "amazing facts in hindi", "psychology facts", "rahasya", "hindi kahani", "horror story in hindi", "jaadui kahani", "bhootiya kahani", "animated story", "shorts", "viral shorts"],
  "first_comment": "🔥 Ek engaging sawaal Hindi mein jo viewers ko comment karne par majboor kar de + Subscribe reminder! 👇",
  "thumbnail_text": "3 TO 4 SHOCKING WORDS IN HINGLISH",
  "thumbnail_prompt": "3D Pixar Disney cartoon animation style, ultra dramatic Indian mystery or horror/magical story scene with expressive wide-eyed characters, glowing lighting, 8k",
  "scenes": [
    {{
      "scene_number": 1,
      "narration_hindi": "Pure natural spoken Hindi text in Devanagari script for voiceover...",
      "subtitle_hinglish": "SHORT PUNCHY HINGLISH CAPTION",
      "visual_style": "cartoon",
      "search_query": "2-3 simple English keywords for photo search when realistic (e.g. 'kailash temple', 'galaxy stars', 'human brain')",
      "setting": "village_day",
      "characters": [
        {{"type": "village_girl_1", "action": "walk_in_left"}},
        {{"type": "village_girl_2", "action": "walk_in_right"}}
      ]
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
                    "temperature": 0.90
                }
            }
            try:
                resp = requests.post(url, json=payload, timeout=45)
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
        time.sleep(5)

    raise RuntimeError(f"Gemini API failed across all models. Last error: {last_error}")
