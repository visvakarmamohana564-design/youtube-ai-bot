"""
Main Entry Point for YouTube AI Automation Bot
Supports both Full Run (--step all) and Step-by-Step tracking (--step script / render / upload)
plus multi-line prompts via custom_prompt.txt or --topic!
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


def _is_jaadui_jungle_master_prompt(prompt_text: str) -> bool:
    if not prompt_text:
        return False
    low = prompt_text.lower()
    return (
        ("जादुई जंगल" in prompt_text and "सुनहरी परी" in prompt_text)
        or ("jaadui jungle" in low and "sunehri pari" in low)
        or ("mishri" in low and "kaalvan" in low)
    )


def main():
    parser = argparse.ArgumentParser(description="100% Automated AI YouTube Channel Bot (Shorts + Long Stories)")
    parser.add_argument(
        "--type",
        choices=["shorts", "long"],
        default="shorts",
        help="Video format: 'shorts' (9:16 Hindi Facts) or 'long' (16:9 Hindi Horror/Jaadui Kahaniyan)"
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
        help="Optional custom topic or story prompt"
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
    resolved_topic = _resolve_custom_prompt(args.topic)

    config.VOICE_STYLE = args.voice
    if args.privacy:
        config.VIDEO_CONFIG[args.type]["privacy_status"] = args.privacy

    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    plan_path = os.path.join(config.OUTPUT_DIR, f"last_{args.type}_metadata.json")
    video_out_path = os.path.join(config.OUTPUT_DIR, f"final_{args.type}.mp4")
    thumb_out_path = os.path.join(config.OUTPUT_DIR, f"thumbnail_{args.type}.jpg")

    # Special Route: Full 14-Scene 3D Pixar Movie for "जादुई जंगल और सुनहरी परी का रहस्य"
    if args.type == "long" and _is_jaadui_jungle_master_prompt(resolved_topic):
        if args.step in ("all", "render"):
            from build_jaadui_jungle_movie import build_and_upload_jaadui_jungle_movie
            out_v, vid_id = build_and_upload_jaadui_jungle_movie()
            if os.path.exists(out_v):
                shutil.copyfile(out_v, video_out_path)
            jj_th = os.path.join(config.OUTPUT_DIR, "jaadui_jungle_3d_thumb.jpg")
            if os.path.exists(jj_th):
                shutil.copyfile(jj_th, thumb_out_path)
            # Clear custom_prompt.txt after consuming
            p_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompt.txt")
            if os.path.exists(p_file):
                open(p_file, "w", encoding="utf-8").close()
            return
        elif args.step == "script":
            print("🧠 Master 3D Story Prompt Detected: जादुई जंगल और सुनहरी परी का रहस्य")
            return
        elif args.step == "upload":
            print("✅ Upload already handled by 3D Movie Builder!")
            return

    # STEP 1: AI SCRIPT GENERATION
    if args.step in ("all", "script"):
        print("🧠 Step 1/3: Generating Viral Hindi Script, Title & Description via Gemini AI...")
        plan = generate_video_plan(video_type=args.type, custom_topic=resolved_topic)
        with open(plan_path, "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        print(f"   📌 Generated Title: {plan.get('title')}")
        print(f"   🏷️  Tags ({len(plan.get('tags', []))}): {', '.join(plan.get('tags', [])[:6])}...")

    # STEP 2: VIDEO RENDERING
    if args.step in ("all", "render"):
        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)
        print("\n🎬 Step 2/3: Creating Hindi Voiceover, Visuals, Subtitles & Final MP4...")
        video_path, thumbnail_path = build_complete_video(plan=plan, video_type=args.type)
        print(f"   ✅ Video Ready: {video_path}")
        print(f"   ✅ Thumbnail Ready: {thumbnail_path}")

    # STEP 3: YOUTUBE UPLOAD
    if args.step in ("all", "upload") and not args.no_upload:
        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)
        print("\n🚀 Step 3/3: Uploading to YouTube with Title, Description & Tags...")
        publish_iso = args.publish_at.strip() if (args.publish_at and args.publish_at.strip()) else None
        video_id = upload_to_youtube(
            video_path=video_out_path,
            thumbnail_path=thumb_out_path,
            plan=plan,
            video_type=args.type,
            publish_at_iso=publish_iso
        )
        print(f"\n🎉 ALL DONE! Watch at: https://www.youtube.com/watch?v={video_id}")
        p_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_prompt.txt")
        if os.path.exists(p_file):
            open(p_file, "w", encoding="utf-8").close()


if __name__ == "__main__":
    main()
