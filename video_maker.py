"""
MP Board Class 10th NCERT Educational Long Video Renderer (16:9 Full HD, 1920x1080)
- 100% Educational Purpose (YouTube Category 27: Education)
- Renders each chapter section in two clear phases:
  Phase 1: 📖 NCERT मूल पाठ वाचन (Highlights Left Book Passage + Visual Illustration while reading chapter text)
  Phase 2: 💡 अंदर की बातों की सरल व्याख्या (Highlights Right Deep Explanation + Word Meanings + MP Board IMP Question)
- Streams directly to FFmpeg for low-memory, fast 1080p HD rendering on GitHub Actions & Local Server
"""

import os
import math
import wave
import random
import shutil
import subprocess
from io import BytesIO
import requests
import numpy as np
import imageio_ffmpeg
from gtts import gTTS
from PIL import Image, ImageDraw, ImageEnhance
import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MP_ASSETS = os.path.join(BASE_DIR, "assets", "mpboard_c10")
TEMP_DIR = "/tmp/mpboard_auto_build"

os.makedirs(MP_ASSETS, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)


def _ensure_devanagari_font():
    font_src = os.path.join(BASE_DIR, "assets", "NotoSansDevanagari-Bold.ttf")
    user_fonts = os.path.expanduser("~/.fonts")
    os.makedirs(user_fonts, exist_ok=True)
    dst = os.path.join(user_fonts, "NotoSansDevanagari-Bold.ttf")
    if os.path.exists(font_src) and not os.path.exists(dst):
        shutil.copy2(font_src, dst)
        subprocess.run(["fc-cache", "-f"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


_ensure_devanagari_font()


def _sanitize_pango_markup(text: str) -> str:
    """Keeps <b> and </b> tags while escaping stray & or < > characters."""
    if not text:
        return ""
    s = str(text).replace("&", " और ")
    s = s.replace("<b>", "___B_OPEN___").replace("</b>", "___B_CLOSE___")
    s = s.replace("<", "(").replace(">", ")")
    s = s.replace("___B_OPEN___", "<b>").replace("___B_CLOSE___", "</b>")
    return s


def render_pango_block(markup_text: str, width_px: int, font_size: int = 19) -> Image.Image:
    """Renders multi-line Pango markup with 100% accurate Hindi Devanagari shaping and exact pixel width."""
    os.makedirs(TEMP_DIR, exist_ok=True)
    pango_bin = "/usr/bin/pango-view"
    pango_pts = int(width_px * 0.71)
    out_png = os.path.join(TEMP_DIR, f"pango_{abs(hash((markup_text, pango_pts, font_size))) % 10000000}.png")
    if not os.path.exists(out_png):
        cmd = [
            pango_bin,
            "--no-display",
            "--markup",
            f"--font=Noto Sans Devanagari Bold {font_size}",
            f"--width={pango_pts}",
            "--margin=4",
            "--background=#00000000",
            f"--output={out_png}",
            f"--text={markup_text}",
        ]
        env = os.environ.copy()
        env["LC_ALL"] = "C.UTF-8"
        subprocess.run(cmd, check=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    im = Image.open(out_png).convert("RGBA")
    if im.width > width_px:
        new_h = max(1, int(im.height * (width_px / float(im.width))))
        im = im.resize((width_px, new_h), Image.Resampling.LANCZOS)
    return im


def synthesize_voice(text: str, out_wav: str, mode: str = "read"):
    os.makedirs(os.path.dirname(out_wav), exist_ok=True)
    mp3_path = out_wav.replace(".wav", ".mp3")
    tts = gTTS(text=text, lang="hi", slow=False)
    tts.save(mp3_path)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    af = (
        "asetrate=24000*1.01,atempo=1.06,aresample=24000,highpass=f=75,dynaudnorm"
        if mode == "read"
        else "asetrate=24000*0.98,atempo=1.09,aresample=24000,highpass=f=75,dynaudnorm"
    )
    subprocess.run(
        [ff, "-y", "-i", mp3_path, "-af", af, "-ac", "1", "-ar", "24000", out_wav],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if os.path.exists(mp3_path):
        os.remove(mp3_path)


def _fetch_or_get_illustration(query: str, sec_idx: int, width: int = 884, height: int = 340) -> Image.Image:
    """Gets a clean illustration for the chapter section."""
    local_fallbacks = [
        "netaji_s1_statue.jpg",
        "netaji_s2_panwala.jpg",
        "netaji_s3_captain.jpg",
        "netaji_s4_sarkanda.jpg"
    ]
    headers = {"User-Agent": "MPBoardNCERTBot/1.0"}
    if query:
        try:
            resp = requests.get(
                "https://commons.wikimedia.org/w/api.php",
                params={
                    "action": "query",
                    "generator": "search",
                    "gsrsearch": f"filetype:bitmap {query}",
                    "gsrnamespace": 6,
                    "gsrlimit": 5,
                    "prop": "imageinfo",
                    "iiprop": "url",
                    "iiurlwidth": 1280,
                    "format": "json"
                },
                headers=headers,
                timeout=5
            )
            if resp.status_code == 200:
                pages = list(resp.json().get("query", {}).get("pages", {}).values())
                for p in pages[:3]:
                    thumb_url = p.get("imageinfo", [{}])[0].get("thumburl")
                    if thumb_url:
                        img_r = requests.get(thumb_url, headers=headers, timeout=5)
                        if img_r.status_code == 200 and len(img_r.content) > 15000:
                            im = Image.open(BytesIO(img_r.content)).convert("RGBA")
                            return im.resize((width, height), Image.Resampling.LANCZOS)
        except Exception:
            pass

    fb_name = local_fallbacks[(sec_idx - 1) % len(local_fallbacks)]
    fb_path = os.path.join(MP_ASSETS, fb_name)
    if os.path.exists(fb_path):
        return Image.open(fb_path).convert("RGBA").resize((width, height), Image.Resampling.LANCZOS)
    return Image.new("RGBA", (width, height), (30, 58, 138, 255))


def build_smartboard_plate(
    subject_header: str,
    sec: dict,
    sec_idx: int,
    ill_img: Image.Image,
    phase: str,
    width: int = 1920,
    height: int = 1080
) -> Image.Image:
    canvas = Image.new("RGBA", (width, height), (11, 17, 32, 255))
    draw = ImageDraw.Draw(canvas)

    sec_title = _sanitize_pango_markup(sec.get("title", f"भाग {sec_idx}"))
    subj_hdr = _sanitize_pango_markup(subject_header or "MP BOARD कक्षा 10वीं NCERT संपूर्ण व्याख्या")

    # Top Header Bar
    draw.rounded_rectangle([24, 16, width - 24, 96], radius=18, fill=(22, 34, 62, 255), outline=(59, 130, 246, 255), width=2)
    hdr_markup = (
        f"<span foreground='#FBBF24' weight='heavy' size='18500'>{subj_hdr}</span>   "
        f"<span foreground='#FFFFFF' weight='heavy' size='19000'>|   {sec_title}</span>"
    )
    hdr_img = render_pango_block(hdr_markup, width - 90, font_size=18)
    canvas.paste(hdr_img, (44, 30), hdr_img)

    # Mode Status Pill Bar
    if phase == "read":
        pill_bg = (6, 78, 59, 255)
        pill_border = (16, 185, 129, 255)
        mode_markup = "<span foreground='#6EE7B7' weight='heavy' size='18500'>▶ अभी चल रहा है: NCERT मूल पाठ वाचन (चैप्टर की पंक्तियाँ ध्यान से सुनें और पढ़ें)</span>"
    else:
        pill_bg = (88, 28, 135, 255)
        pill_border = (192, 132, 252, 255)
        mode_markup = "<span foreground='#FDE047' weight='heavy' size='18500'>▶ अभी चल रहा है: अंदर की बातों की सरल व्याख्या (गहरा अर्थ, शब्दार्थ और परीक्षा बिंदु)</span>"

    draw.rounded_rectangle([24, 106, width - 24, 160], radius=14, fill=pill_bg, outline=pill_border, width=2)
    mode_img = render_pango_block(mode_markup, width - 80, font_size=18)
    canvas.paste(mode_img, (44, 116), mode_img)

    # LEFT PANEL: Scene Illustration + NCERT Book Passage
    left_border = (16, 185, 129, 255) if phase == "read" else (51, 65, 85, 255)
    left_w = 4 if phase == "read" else 2
    draw.rounded_rectangle([24, 172, 948, 986], radius=20, fill=(17, 24, 39, 255), outline=left_border, width=left_w)

    canvas.paste(ill_img, (44, 190))
    draw.rounded_rectangle([44, 190, 928, 530], radius=14, outline=(251, 191, 36, 220), width=2)

    draw.rounded_rectangle(
        [40, 542, 932, 970], radius=14,
        fill=(30, 41, 59, 255) if phase == "read" else (15, 23, 42, 255),
        outline=(52, 211, 153, 255) if phase == "read" else (51, 65, 85, 200), width=2
    )

    book_heading = _sanitize_pango_markup(sec.get("book_heading", f"★ NCERT मूल पाठ (भाग {sec_idx}):"))
    book_text = _sanitize_pango_markup(sec.get("book_text") or sec.get("narration_hindi", ""))
    book_color = "#FEF08A" if phase == "read" else "#CBD5E1"
    book_markup = (
        f"<span foreground='#34D399' weight='heavy' size='19000'>{book_heading}</span>\n"
        f"<span foreground='{book_color}' weight='bold' size='17500'>{book_text}</span>"
    )
    book_img = render_pango_block(book_markup, 860, font_size=18)
    canvas.paste(book_img, (54, 552), book_img)

    # RIGHT PANEL: Inside Explanation ("अंदर की बातें") + Word Meanings + MP Board Exam Tip
    right_border = (250, 204, 21, 255) if phase == "explain" else (51, 65, 85, 255)
    right_w = 4 if phase == "explain" else 2
    draw.rounded_rectangle(
        [968, 172, 1896, 986], radius=20,
        fill=(23, 31, 50, 255) if phase == "explain" else (15, 23, 42, 255),
        outline=right_border, width=right_w
    )

    inside_heading = _sanitize_pango_markup(sec.get("inside_heading", "★ अंदर की बातें और सरल व्याख्या (Deep Meaning):"))
    raw_points = sec.get("inside_points", [])
    clean_points = [_sanitize_pango_markup(pt) for pt in raw_points]
    pts_joined = "\n\n".join(clean_points)
    right_markup = (
        f"<span foreground='#FBBF24' weight='heavy' size='20000'>{inside_heading}</span>\n\n"
        f"<span foreground='#F8FAFC' size='17500'>{pts_joined}</span>"
    )
    right_img = render_pango_block(right_markup, 884, font_size=18)
    canvas.paste(right_img, (990, 190), right_img)

    # Bottom Right Box: MP Board Exam Tip
    draw.rounded_rectangle([986, 848, 1878, 968], radius=14, fill=(127, 29, 29, 255), outline=(248, 113, 113, 255), width=2)
    exam_tip = _sanitize_pango_markup(sec.get("exam_tip", "★ MP Board IMP प्रश्न: इस गद्यांश का मुख्य भाव अपने शब्दों में स्पष्ट कीजिए।"))
    tip_markup = f"<span foreground='#FEF08A' weight='heavy' size='17500'>{exam_tip}</span>"
    tip_img = render_pango_block(tip_markup, 860, font_size=18)
    canvas.paste(tip_img, (1002, 862), tip_img)

    return canvas


def build_complete_video(plan: dict, video_type: str = "long") -> tuple:
    """
    Renders a 16:9 Full HD (1920x1080) MP Board Class 10th NCERT Chapter Explanation Long Video.
    """
    video_type = "long"
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    scenes = plan.get("scenes", [])
    subject_header = plan.get("subject_header", "MP BOARD कक्षा 10वीं NCERT संपूर्ण व्याख्या")
    sr = 24000
    master_wav = os.path.join(TEMP_DIR, "auto_master.wav")
    segment_plan = []

    print(f"\n📚 Rendering {len(scenes)}-Section MP Board Class 10th NCERT Long Video (1920x1080)...")

    with wave.open(master_wav, "wb") as out_wf:
        out_wf.setnchannels(1)
        out_wf.setsampwidth(2)
        out_wf.setframerate(sr)

        for idx, sec in enumerate(scenes, start=1):
            read_txt = sec.get("read_audio") or sec.get("narration_hindi") or sec.get("book_text", "")
            explain_txt = sec.get("explain_audio") or "आइए अब इस भाग के मुख्य बिंदुओं को समझते हैं।"

            r_wav = os.path.join(TEMP_DIR, f"s{idx}_read.wav")
            synthesize_voice(read_txt, r_wav, mode="read")
            with wave.open(r_wav, "rb") as wf:
                r_pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
            out_wf.writeframes(r_pcm.tobytes())
            r_dur = len(r_pcm) / float(sr)

            e_wav = os.path.join(TEMP_DIR, f"s{idx}_explain.wav")
            synthesize_voice(explain_txt, e_wav, mode="explain")
            with wave.open(e_wav, "rb") as wf:
                e_pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
            out_wf.writeframes(e_pcm.tobytes())
            e_dur = len(e_pcm) / float(sr)

            ill_img = _fetch_or_get_illustration(sec.get("search_query", ""), idx)
            segment_plan.append((idx, sec, ill_img, r_dur, e_dur))
            print(f"  -> Section {idx}/{len(scenes)}: Read={r_dur:.1f}s | Explain={e_dur:.1f}s")

    total_dur = sum(r + e for _, _, _, r, e in segment_plan)
    video_out_path = os.path.join(config.OUTPUT_DIR, f"final_{video_type}.mp4")
    thumb_out_path = os.path.join(config.OUTPUT_DIR, f"thumbnail_{video_type}.jpg")

    # Save Thumbnail from Section 1 Explain Plate
    if segment_plan:
        _, s1, ill1, _, _ = segment_plan[0]
        p1 = build_smartboard_plate(subject_header, s1, 1, ill1, "explain", 1920, 1080)
        p1.resize((1280, 720), Image.Resampling.LANCZOS).convert("RGB").save(thumb_out_path, "JPEG", quality=92)

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    fps = 6
    cmd = [
        ff, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(fps),
        "-i", "-",
        "-i", master_wav,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
        "-maxrate", "450k", "-bufsize", "900k",
        "-r", "24", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart",
        "-shortest",
        video_out_path
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elapsed = 0.0
    for idx, sec, ill_img, r_dur, e_dur in segment_plan:
        for phase, p_dur in [("read", r_dur), ("explain", e_dur)]:
            base_plate = build_smartboard_plate(subject_header, sec, idx, ill_img, phase, 1920, 1080)
            n_frames = max(1, int(round(p_dur * fps)))
            for f_idx in range(n_frames):
                t_local = f_idx / float(fps)
                prog_ratio = min(1.0, (elapsed + t_local) / max(1.0, total_dur))
                frame = base_plate.copy()
                draw = ImageDraw.Draw(frame)

                scan_y = int(570 + 340 * (0.5 + 0.5 * math.sin(t_local * 1.4))) if phase == "read" else int(230 + 560 * ((t_local / max(1.0, p_dur)) % 1.0))
                if phase == "read":
                    draw.rounded_rectangle([30, scan_y, 42, scan_y + 48], radius=5, fill=(16, 185, 129, 255))
                else:
                    draw.rounded_rectangle([974, scan_y, 986, scan_y + 54], radius=5, fill=(250, 204, 21, 255))

                draw.rounded_rectangle([24, 1004, 1896, 1030], radius=10, fill=(30, 41, 59, 255))
                bar_w = max(20, int(1872 * prog_ratio))
                draw.rounded_rectangle([24, 1004, 24 + bar_w, 1030], radius=10, fill=(16, 185, 129, 255) if phase == "read" else (250, 204, 21, 255))

                proc.stdin.write(frame.convert("RGB").tobytes())
            elapsed += p_dur

    proc.stdin.close()
    proc.wait()
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    return video_out_path, thumb_out_path
