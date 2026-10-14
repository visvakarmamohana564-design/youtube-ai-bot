"""
Main Entry Point for YouTube AI Automation Bot (100% Educational Long Videos — MP Board Class 10th NCERT)
- Forces 'long' (16:9 Full HD, 1920x1080) format (Shorts Disabled!)
- Uploads under YouTube Category ID '27' (Education)
"""

import argparse
import json
import os
import shutil
from ai_generator import generate_video_plan
from video_maker import build_complete_video
from youtube_uploader import upload_to_youtube
import config


def _resolve_custom_prompt(cli_topic: str) -> str:
    if cli_topic and cli_topic.strip():
        return cli_topic.strip()
    prompt_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompt.txt")
    if os.path.exists(prompt_file):
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                txt = f.read().strip()
            if txt:
                return txt
        except Exception:
            pass
    return None


def main():
    parser = argparse.ArgumentParser(description="100% Automated Educational YouTube Bot (MP Board Class 10th NCERT Long Videos)")
    parser.add_argument(
        "--type",
        choices=["long", "shorts"],
        default="long",
        help="Locked to 'long' (16:9 Educational Full HD Video)"
    )
    parser.add_argument(
        "--step",
        choices=["all", "script", "render", "upload"],
        default="all",
        help="Which pipeline step to execute"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Optional custom MP Board Class 10 NCERT chapter topic"
    )
    parser.add_argument(
        "--voice",
        choices=["male", "female"],
        default="male",
        help="Optional voice style: 'male' or 'female'"
    )
    parser.add_argument(
        "--privacy",
        choices=["public", "private", "unlisted"],
        default="public",
        help="Optional YouTube privacy status (default: public)"
    )
    parser.add_argument(
        "--publish-at",
        type=str,
        default=None,
        help="Optional ISO 8601 UTC timestamp to schedule publish"
    )
    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="Only generate the video locally without uploading to YouTube"
    )

    args = parser.parse_args()
    # Strictly enforce Long Educational Video format (No Shorts!)
    vtype = "long"
    resolved_topic = _resolve_custom_prompt(args.topic)

    config.VOICE_STYLE = args.voice
    if args.privacy:
        config.VIDEO_CONFIG["long"]["privacy_status"] = args.privacy
    config.VIDEO_CONFIG["long"]["category_id"] = "27"  # 27 = Education

    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    plan_path = os.path.join(config.OUTPUT_DIR, f"last_{vtype}_metadata.json")
    video_out_path = os.path.join(config.OUTPUT_DIR, f"final_{vtype}.mp4")
    thumb_out_path = os.path.join(config.OUTPUT_DIR, f"thumbnail_{vtype}.jpg")

    # STEP 1: AI EDUCATIONAL CHAPTER SCRIPT GENERATION
    if args.step in ("all", "script"):
        print("📚 Step 1/3: Generating MP Board Class 10 NCERT Chapter Reading & Deep Explanation Plan...")
        plan = generate_video_plan(video_type="long", custom_topic=resolved_topic)
        with open(plan_path, "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        print(f"   📌 Generated Chapter Title: {plan.get('title')}")
        print(f"   🏷️  Educational Tags ({len(plan.get('tags', []))}): {', '.join(plan.get('tags', [])[:6])}...")

    # STEP 2: 1080p SMART-BOARD VIDEO RENDERING
    if args.step in ("all", "render"):
        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)
        print("\n🎬 Step 2/3: Rendering 1080p Full HD NCERT Smart-Board Chapter Video (Book Reading + Deep Explanation)...")
        video_path, thumbnail_path = build_complete_video(plan=plan, video_type="long")
        print(f"   ✅ Educational Long Video Ready: {video_path}")
        print(f"   ✅ Thumbnail Ready: {thumbnail_path}")

    # STEP 3: YOUTUBE UPLOAD (CATEGORY 27 = EDUCATION)
    if args.step in ("all", "upload") and not args.no_upload:
        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)
        print("\n🚀 Step 3/3: Uploading Educational Long Video to YouTube (Category: Education)...")
        publish_iso = args.publish_at.strip() if (args.publish_at and args.publish_at.strip()) else None
        video_id = upload_to_youtube(
            video_path=video_out_path,
            thumbnail_path=thumb_out_path,
            plan=plan,
            video_type="long",
            publish_at_iso=publish_iso
        )
        print(f"\n🎉 ALL DONE! Watch at: https://www.youtube.com/watch?v={video_id}")
        p_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompt.txt")
        if os.path.exists(p_file):
            open(p_file, "w", encoding="utf-8").close()


if __name__ == "__main__":
    main()
