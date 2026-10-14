"""
MASTER SYSTEM PROMPT PRODUCTION ENGINE — 11-MINUTE 3D ANIMATED HINDI FILM
Title: "समय की टूटी घड़ी और नन्हा कारीगर" (Samay Ki Tooti Ghadi Aur Nanha Karigar)
Format: 1920x1080 Full HD (16:9), 24 FPS, ~10.85 Minutes (24 Scenes × 4 Dynamic Sub-Shots = 96 Action Cuts)
Dynamic Motion System:
  - 6 Distinct Character Rigs:
      1. `vihaan` (3/4 Standing & Expressive Gesturing Rig)
      2. `vihaan_walk` (3/4 Side-Profile Wide Stride Walking & Running Rig)
      3. `vihaan_kneel` (Kneeling on One Knee & Two-Hand Reaching/Repairing Rig)
      4. `dadaji` (Natural 3/4 Storytelling Rig with Clockwork Cane & Raised Hand — ZERO T-pose)
      5. `tiktik` (3D Swooping Brass Mechanical Owl Rig with Flapping Gear Wings & Z-Depth Flight)
      6. `gajraj` & `gajraj_action` (Imposing Guard Rig + 3/4 Dynamic Reaching Action Rig)
  - 96 Multi-Shot Camera Cuts (Wide Tracking Pan, Z-Depth Walk-In, Medium Two-Shot, Close-Up Action, Parabolic River Leaps, 3D Perspective Turns, Live Rotating Clockwork Gears)
"""

import os
import math
import subprocess
import wave
import numpy as np
from gtts import gTTS
import imageio_ffmpeg
from PIL import Image, ImageDraw
from cartoon_animator import render_hindi_title_badge
from youtube_uploader import upload_to_youtube

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SG_DIR = os.path.join(BASE_DIR, "assets", "samay_ghadi")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = "/tmp/samay_ghadi_build"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# ==============================================================================
# 6 MULTI-JOINT 3D ANATOMICAL RIG SPECS (INCLUDING SIDE-WALK, KNEEL & ACTION)
# ==============================================================================
RIG_SPECS = {
    "vihaan": {
        "target_h": 540,
        "head_box": (0.25, 0.00, 0.72, 0.25),
        "neck_piv": (0.46, 0.22),
        "l_arm_box": (0.58, 0.16, 1.00, 0.48),  # Raised gesturing left hand
        "l_arm_piv": (0.62, 0.30),
        "r_arm_box": (0.00, 0.24, 0.32, 0.62),  # Right hand holding pocket watch
        "r_arm_piv": (0.26, 0.30),
        "l_leg_box": (0.20, 0.62, 0.50, 1.00),
        "l_leg_piv": (0.38, 0.64),
        "r_leg_box": (0.50, 0.62, 0.82, 1.00),
        "r_leg_piv": (0.62, 0.64),
        "mode": "stand",
    },
    "vihaan_walk": {
        "target_h": 530,
        "head_box": (0.38, 0.00, 0.76, 0.25),
        "neck_piv": (0.54, 0.22),
        "l_arm_box": (0.62, 0.22, 1.00, 0.52),  # Forward swinging arm
        "l_arm_piv": (0.64, 0.30),
        "r_arm_box": (0.00, 0.22, 0.38, 0.58),  # Back swinging arm
        "r_arm_piv": (0.34, 0.30),
        "l_leg_box": (0.00, 0.58, 0.50, 1.00),  # Back striding leg
        "l_leg_piv": (0.44, 0.60),
        "r_leg_box": (0.46, 0.58, 1.00, 1.00),  # Front striding leg
        "r_leg_piv": (0.54, 0.60),
        "mode": "walk",
    },
    "vihaan_kneel": {
        "target_h": 430,
        "head_box": (0.34, 0.00, 0.82, 0.34),
        "neck_piv": (0.56, 0.30),
        "l_arm_box": (0.52, 0.28, 1.00, 0.64),  # Reaching both hands forward
        "l_arm_piv": (0.56, 0.38),
        "r_arm_box": (0.45, 0.32, 0.95, 0.62),
        "r_arm_piv": (0.52, 0.40),
        "l_leg_box": (0.00, 0.60, 0.52, 1.00),
        "l_leg_piv": (0.38, 0.66),
        "r_leg_box": (0.48, 0.60, 0.96, 1.00),
        "r_leg_piv": (0.62, 0.66),
        "mode": "kneel",
    },
    "dadaji": {
        "target_h": 550,
        "head_box": (0.26, 0.00, 0.74, 0.28),
        "neck_piv": (0.48, 0.25),
        "l_arm_box": (0.64, 0.18, 1.00, 0.56),  # Warm raised speaking hand
        "l_arm_piv": (0.68, 0.34),
        "r_arm_box": (0.00, 0.28, 0.30, 0.98),  # Hand with carved clockwork cane
        "r_arm_piv": (0.24, 0.34),
        "l_leg_box": (0.25, 0.68, 0.52, 1.00),
        "l_leg_piv": (0.40, 0.70),
        "r_leg_box": (0.52, 0.68, 0.82, 1.00),
        "r_leg_piv": (0.62, 0.70),
        "mode": "stand",
    },
    "tiktik": {
        "target_h": 240,
        "head_box": (0.34, 0.00, 0.66, 0.42),
        "neck_piv": (0.50, 0.38),
        "l_arm_box": (0.00, 0.05, 0.38, 0.72),  # Left brass gear wing
        "l_arm_piv": (0.36, 0.42),
        "r_arm_box": (0.62, 0.05, 1.00, 0.72),  # Right brass gear wing
        "r_arm_piv": (0.64, 0.42),
        "l_leg_box": (0.34, 0.75, 0.50, 1.00),
        "l_leg_piv": (0.43, 0.78),
        "r_leg_box": (0.50, 0.75, 0.66, 1.00),
        "r_leg_piv": (0.57, 0.78),
        "mode": "fly",
    },
    "gajraj": {
        "target_h": 650,
        "head_box": (0.33, 0.00, 0.67, 0.30),
        "neck_piv": (0.50, 0.26),
        "l_arm_box": (0.00, 0.16, 0.32, 0.84),
        "l_arm_piv": (0.28, 0.28),
        "r_arm_box": (0.68, 0.16, 1.00, 0.84),
        "r_arm_piv": (0.72, 0.28),
        "l_leg_box": (0.28, 0.68, 0.50, 1.00),
        "l_leg_piv": (0.40, 0.70),
        "r_leg_box": (0.50, 0.68, 0.72, 1.00),
        "r_leg_piv": (0.60, 0.70),
        "mode": "stand",
    },
    "gajraj_action": {
        "target_h": 650,
        "head_box": (0.40, 0.08, 0.66, 0.30),
        "neck_piv": (0.54, 0.26),
        "l_arm_box": (0.00, 0.00, 0.46, 0.52),  # Giant reaching stone arm
        "l_arm_piv": (0.40, 0.28),
        "r_arm_box": (0.66, 0.20, 1.00, 0.78),
        "r_arm_piv": (0.72, 0.32),
        "l_leg_box": (0.22, 0.62, 0.54, 1.00),
        "l_leg_piv": (0.42, 0.64),
        "r_leg_box": (0.54, 0.62, 0.86, 1.00),
        "r_leg_piv": (0.64, 0.64),
        "mode": "action",
    },
}

SG_POSE_BANK = {}
GEAR_SPRITES = {}


def _build_char_layers(char_name: str):
    spec = RIG_SPECS[char_name]
    closed_im = Image.open(os.path.join(SG_DIR, f"{char_name}_closed.png")).convert("RGBA")
    W, H = closed_im.size
    pad = 64

    def _pad(im):
        c = Image.new("RGBA", (W + pad * 2, H + pad * 2), (0, 0, 0, 0))
        c.paste(im, (pad, pad))
        return c

    def _extract_box(arr, box_norm, clear_from=None):
        x0, y0, x1, y1 = int(W * box_norm[0]), int(H * box_norm[1]), int(W * box_norm[2]), int(H * box_norm[3])
        part = np.zeros_like(arr)
        part[y0:y1, x0:x1] = arr[y0:y1, x0:x1]
        if clear_from is not None:
            clear_from[y0:y1, x0:x1, 3] = 0
        return _pad(Image.fromarray(part))

    base_arr = np.array(closed_im)
    torso_arr = base_arr.copy()

    l_arm = _extract_box(base_arr, spec["l_arm_box"], torso_arr)
    r_arm = _extract_box(base_arr, spec["r_arm_box"], torso_arr)
    l_leg = _extract_box(base_arr, spec["l_leg_box"], torso_arr)
    r_leg = _extract_box(base_arr, spec["r_leg_box"], torso_arr)

    hx0, hy0, hx1, hy1 = [int(v * (W if i % 2 == 0 else H)) for i, v in enumerate(spec["head_box"])]
    torso_arr[hy0:hy1, hx0:hx1, 3] = 0
    torso = _pad(Image.fromarray(torso_arr))

    heads = {}
    for m_state in ("closed", "half", "open"):
        m_im = Image.open(os.path.join(SG_DIR, f"{char_name}_{m_state}.png")).convert("RGBA")
        m_arr = np.array(m_im)
        h_part = np.zeros_like(m_arr)
        h_part[hy0:hy1, hx0:hx1] = m_arr[hy0:hy1, hx0:hx1]
        heads[m_state] = _pad(Image.fromarray(h_part))

    return {
        "W": W, "H": H, "pad": pad, "spec": spec,
        "torso": torso, "l_arm": l_arm, "r_arm": r_arm,
        "l_leg": l_leg, "r_leg": r_leg, "heads": heads,
    }


def _ensure_sg_pose_bank():
    if SG_POSE_BANK:
        return
    print("⚙️ Pre-baking 6-Rig 3D Multi-Action Pose Bank (Walk, Run, Kneel, Fly, Action, Talk)...")
    for cname, spec in RIG_SPECS.items():
        layers = _build_char_layers(cname)
        W, H, pad = layers["W"], layers["H"], layers["pad"]
        target_h = spec["target_h"]
        scale = target_h / max(1, H)
        out_w = int((W + pad * 2) * scale)
        out_h = int((H + pad * 2) * scale)
        mode = spec["mode"]

        def _piv(key):
            px, py = spec[key]
            return (int(px * W) + pad, int(py * H) + pad)

        for p_idx in range(12):
            phase = (p_idx / 12.0) * math.pi * 2.0
            s_val = math.sin(phase)
            c_val = math.cos(phase)

            if mode == "walk":
                # Wide side-profile scissoring leg stride + opposite arm swing + torso forward lean
                l_arm_deg = s_val * 32.0
                r_arm_deg = -s_val * 32.0
                l_leg_deg = -s_val * 30.0
                r_leg_deg = s_val * 30.0
                head_deg = c_val * 5.0
                body_lean = -5.0 + s_val * 2.5
            elif mode == "kneel":
                # Kneeling upper-body work & reaching motion
                l_arm_deg = s_val * 24.0
                r_arm_deg = c_val * 20.0
                l_leg_deg = 0.0
                r_leg_deg = 0.0
                head_deg = s_val * 8.0
                body_lean = s_val * 4.0
            elif mode == "fly":
                # Rapid brass wing flapping + banking body tilt
                l_arm_deg = s_val * 34.0
                r_arm_deg = -s_val * 34.0
                l_leg_deg = c_val * 10.0
                r_leg_deg = -c_val * 10.0
                head_deg = c_val * 7.0
                body_lean = s_val * 6.0
            elif mode == "action":
                # Powerful reaching & lifting motion for Gajraj
                l_arm_deg = s_val * 26.0
                r_arm_deg = -c_val * 18.0
                l_leg_deg = s_val * 12.0
                r_leg_deg = -s_val * 12.0
                head_deg = c_val * 6.0
                body_lean = s_val * 3.5
            else:
                # Natural expressive storytelling & stepping motion
                l_arm_deg = s_val * 26.0
                r_arm_deg = -c_val * 10.0
                l_leg_deg = s_val * 14.0
                r_leg_deg = -s_val * 14.0
                head_deg = c_val * 6.5
                body_lean = s_val * 2.5

            for m_state in ("closed", "half", "open"):
                canvas = Image.new("RGBA", (W + pad * 2, H + pad * 2), (0, 0, 0, 0))

                def _rot_paste(part_im, piv_pt, deg):
                    if abs(deg) > 0.2:
                        r_im = part_im.rotate(deg, resample=Image.Resampling.BILINEAR, center=piv_pt)
                        canvas.alpha_composite(r_im)
                    else:
                        canvas.alpha_composite(part_im)

                _rot_paste(layers["r_arm"], _piv("r_arm_piv"), r_arm_deg)
                if l_leg_deg >= 0:
                    _rot_paste(layers["l_leg"], _piv("l_leg_piv"), l_leg_deg)
                    _rot_paste(layers["r_leg"], _piv("r_leg_piv"), r_leg_deg)
                else:
                    _rot_paste(layers["r_leg"], _piv("r_leg_piv"), r_leg_deg)
                    _rot_paste(layers["l_leg"], _piv("l_leg_piv"), l_leg_deg)
                _rot_paste(layers["torso"], (W // 2 + pad, int(H * 0.55) + pad), body_lean)
                _rot_paste(layers["heads"][m_state], _piv("neck_piv"), head_deg)
                _rot_paste(layers["l_arm"], _piv("l_arm_piv"), l_arm_deg)

                scaled = canvas.resize((out_w, out_h), Image.Resampling.BILINEAR)
                flipped = scaled.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                SG_POSE_BANK[(cname, m_state, p_idx, False)] = scaled
                SG_POSE_BANK[(cname, m_state, p_idx, True)] = flipped

    # Pre-bake rotating golden clockwork gear sprites (12 rotation angles)
    base_gear = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
    gd = ImageDraw.Draw(base_gear, "RGBA")
    cx, cy = 110, 110
    for i in range(12):
        ang = (i / 12.0) * math.pi * 2.0
        tx0 = cx + int(math.cos(ang - 0.12) * 74)
        ty0 = cy + int(math.sin(ang - 0.12) * 74)
        tx1 = cx + int(math.cos(ang - 0.08) * 98)
        ty1 = cy + int(math.sin(ang - 0.08) * 98)
        tx2 = cx + int(math.cos(ang + 0.08) * 98)
        ty2 = cy + int(math.sin(ang + 0.08) * 98)
        tx3 = cx + int(math.cos(ang + 0.12) * 74)
        ty3 = cy + int(math.sin(ang + 0.12) * 74)
        gd.polygon([(tx0, ty0), (tx1, ty1), (tx2, ty2), (tx3, ty3)], fill=(218, 165, 32, 185), outline=(255, 215, 90, 220))
    gd.ellipse([cx - 76, cy - 76, cx + 76, cy + 76], fill=(184, 134, 11, 165), outline=(255, 215, 90, 225), width=5)
    gd.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(40, 28, 12, 210), outline=(255, 215, 90, 230), width=4)
    for g_idx in range(12):
        GEAR_SPRITES[g_idx] = base_gear.rotate(g_idx * 7.5, resample=Image.Resampling.BILINEAR)

    print("✅ 6-Rig 3D Pose Bank & Rotating Gears Ready!")


from build_jaadui_jungle_movie import VOICE_PROFILES as _JJ_VP  # fallback reference

VOICE_PROFILES = {
    "narrator": {"rate": "0.95", "tempo": "1.06", "filter": ""},
    "vihaan":   {"rate": "1.10", "tempo": "1.00", "filter": ""},
    "dadaji":   {"rate": "0.85", "tempo": "1.15", "filter": ""},
    "tiktik":   {"rate": "1.18", "tempo": "0.96", "filter": ""},
    "gajraj":   {"rate": "0.78", "tempo": "1.22", "filter": ",aecho=0.8:0.85:45:0.25"},
}


def synthesize_line(speaker: str, text: str, out_wav: str) -> str:
    if os.path.exists(out_wav) and os.path.getsize(out_wav) > 1000:
        return out_wav
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    prof = VOICE_PROFILES.get(speaker, VOICE_PROFILES["narrator"])
    tmp_mp3 = out_wav + ".mp3"
    tts = gTTS(text=text, lang="hi", slow=False)
    tts.save(tmp_mp3)

    af = f"asetrate=24000*{prof['rate']},aresample=24000,atempo={prof['tempo']}{prof['filter']}"
    subprocess.run(
        [ffmpeg_exe, "-y", "-i", tmp_mp3, "-filter:a", af, "-ac", "1", "-ar", "24000", out_wav],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
    )
    if os.path.exists(tmp_mp3):
        os.remove(tmp_mp3)
    return out_wav


def _make_sfx_plus_bgm_samples(sfx_type: str, n: int, sr: int = 24000, scene_offset_sec: float = 0.0) -> np.ndarray:
    t = np.arange(n, dtype=np.float32) / float(sr)
    audio = np.zeros(n, dtype=np.float32)

    if sfx_type == "tick_tock":
        for sec in np.arange(0.1, n / sr, 0.5):
            idx = int(sec * sr)
            ln = min(int(0.03 * sr), n - idx)
            if ln > 0:
                freq = 1200.0 if int(sec * 2) % 2 == 0 else 900.0
                lt = np.linspace(0, 0.03, ln, dtype=np.float32)
                audio[idx:idx+ln] += 0.05 * np.sin(2 * np.pi * freq * lt) * np.exp(-lt * 400.0)
    elif sfx_type == "storm_thunder":
        rng = np.random.default_rng(int(scene_offset_sec) + 42)
        noise = rng.normal(0, 0.025, n).astype(np.float32)
        audio += noise * (np.exp(-t * 0.35) + 0.25)
    elif sfx_type == "owl_chime":
        for i, f in enumerate([880.0, 1174.6, 1318.5, 1760.0]):
            st = int(i * 0.18 * sr)
            ln = min(int(0.6 * sr), n - st)
            if ln > 0:
                lt = np.linspace(0, 0.6, ln, dtype=np.float32)
                audio[st:st+ln] += 0.05 * np.sin(2 * np.pi * f * lt) * np.exp(-lt * 4.5)
    elif sfx_type == "gear_turn":
        for sec in np.arange(0.2, n / sr, 0.45):
            idx = int(sec * sr)
            ln = min(int(0.10 * sr), n - idx)
            if ln > 0:
                lt = np.linspace(0, 0.10, ln, dtype=np.float32)
                audio[idx:idx+ln] += 0.05 * np.sin(2 * np.pi * 240.0 * lt) * np.exp(-lt * 18.0)
    elif sfx_type == "tower_bell":
        for sec in np.arange(0.2, n / sr, 2.4):
            idx = int(sec * sr)
            ln = min(int(1.8 * sr), n - idx)
            if ln > 0:
                lt = np.linspace(0, 1.8, ln, dtype=np.float32)
                audio[idx:idx+ln] += (0.07 * np.sin(2 * np.pi * 330.0 * lt) + 0.04 * np.sin(2 * np.pi * 660.0 * lt)) * np.exp(-lt * 1.8)

    chords = [
        (220.0, 261.63, 329.63),
        (174.61, 220.0, 261.63),
        (196.00, 246.94, 293.66),
        (146.83, 220.0, 293.66),
    ]
    c = chords[int(scene_offset_sec // 6) % len(chords)]
    gt = t + scene_offset_sec
    bgm = 0.032 * (
        0.38 * np.sin(2 * np.pi * c[0] * gt)
        + 0.30 * np.sin(2 * np.pi * c[1] * gt)
        + 0.24 * np.sin(2 * np.pi * c[2] * gt)
    )
    return audio + bgm


# ==============================================================================
# 24-SCENE MULTI-SHOT DYNAMIC CHOREOGRAPHY SPECIFICATION
# Every scene has `choreo_mode` controlling 4 distinct sub-shots per scene:
#   - "workshop_intro"   : Vihaan walks across room -> kneels at table -> stands & talks -> turns
#   - "owl_awakening"    : Vihaan walks to table -> kneels & winds Tik-Tik -> Tik-Tik swoops in 3D figure-8!
#   - "storm_run"        : Vihaan & Dadaji rush outside -> Vihaan runs across rain-lashed street!
#   - "river_branch_oil" : Vihaan runs in -> kneels to pull branch & pour oil -> gears rise!
#   - "river_leap"       : Vihaan leaps in 3 huge parabolic arcs across stone gears over rushing river!
#   - "cavern_wing_fix"  : Wind knocks Tik-Tik down -> Vihaan runs & kneels to fix wing -> musical rune jumps!
#   - "guardian_clash"   : Vihaan walks in Z-depth -> Gajraj steps out & reaches (`gajraj_action`)!
#   - "guardian_heal"    : Gajraj kneels -> Vihaan kneels & oils heart-gear -> Master Pendulum starts spinning!
#   - "sunrise_finale"   : Swooping aerial celebration + Dadaji gifts badge + Moral ending!
# ==============================================================================
SCENES_SPEC = [
    {
        "scene_id": 1, "bg": "sg_bg_workshop.jpg", "choreo_mode": "workshop_intro",
        "sfx": "tick_tock", "fx": "workshop_dust", "prop": "table_key_and_oil",
        "lines": [
            ("narrator", "हिमालय की हरी-भरी पहाड़ियों में बसे सुंदरगढ़ कस्बे की पहचान थी उसकी विशाल सूर्य-घड़ी, जो पूरे नगर के मौसम और नदी के बांध को संतुलित रखती थी।"),
            ("vihaan", "दादाजी, देखिए! मैंने इस पुरानी जेब-घड़ी के सबसे छोटे पीतल के पहिये को अपनी आवर्धक लेंस से बिल्कुल सीधा कर दिया है!"),
            ("dadaji", "शाबाश विहान! एक सच्चा घड़ीसाज़ सिर्फ लोहे के पुर्ज़े नहीं जोड़ता, वह हर छोटे पहिये की धड़कन को ध्यान से सुनता है।"),
        ],
    },
    {
        "scene_id": 2, "bg": "sg_bg_workshop.jpg", "choreo_mode": "workshop_intro",
        "sfx": "tick_tock", "fx": "workshop_dust", "prop": "table_key_and_oil",
        "lines": [
            ("dadaji", "विहान, इस मेज़ पर रखे पीतल के उल्लू 'टिक-टिक' और इस सुनहरी चाबी को ध्यान से देखो। इन्हें मैंने पचास साल पहले बनाया था।"),
            ("vihaan", "दादाजी, क्या यह पीतल का उल्लू सचमुच उड़ सकता है? इसके सीने पर तो चाबी लगाने का एक छोटा सा खाना बना हुआ है!"),
            ("dadaji", "हाँ बेटा, अगर कभी पहाड़ी के बड़े घंटाघर पर कोई संकट आए, तो यही सुनहरी चाबी टिक-टिक को जगाती है और मुख्य पेंडुलम का रास्ता दिखाती है।"),
        ],
    },
    {
        "scene_id": 3, "bg": "sg_bg_clocktower_storm.jpg", "choreo_mode": "storm_run",
        "sfx": "storm_thunder", "fx": "storm_rain_lightning", "prop": None,
        "lines": [
            ("narrator", "तभी अचानक आधी रात को भयानक तूफ़ान उठा! आसमान से कड़कती बिजली सीधे पहाड़ी के विशाल घंटाघर के शिखर पर जा गिरी।"),
            ("vihaan", "दादाजी, बाहर देखिए! बिजली गिरने से घंटाघर की बड़ी सुइयाँ ठीक बारह बजे रुक गई हैं और नदी के बांध का फाटक बंद हो गया है!"),
            ("dadaji", "हे भगवान! अगर सूर्योदय से पहले मुख्य पेंडुलम की कमानी फिर से नहीं घूमी, तो नदी का उफनता पानी नीचे पूरे बाज़ार में भर जाएगा!"),
        ],
    },
    {
        "scene_id": 4, "bg": "sg_bg_workshop.jpg", "choreo_mode": "owl_awakening",
        "sfx": "gear_turn", "fx": "workshop_dust", "prop": "pickup_key_and_oil",
        "lines": [
            ("narrator", "दादाजी ने तुरंत उठकर जाने की कोशिश की, लेकिन घुटने के पुराने दर्द के कारण वे लड़खड़ाकर कुर्सी पर बैठ गए।"),
            ("dadaji", "आह... मेरे पैरों में अब इतनी ताकत नहीं बची कि मैं इस तूफ़ान में पहाड़ी की तीन सौ सीढ़ियाँ चढ़ सकूँ।"),
            ("vihaan", "आप चिंता मत कीजिए दादाजी! मैं आपका शिष्य हूँ। मैं यह सुनहरी चाबी और तेल की कुप्पी लेकर अभी घंटाघर जाऊँगा!"),
        ],
    },
    {
        "scene_id": 5, "bg": "sg_bg_workshop.jpg", "choreo_mode": "owl_awakening",
        "sfx": "owl_chime", "fx": "golden_sparks", "prop": "wind_tiktik",
        "lines": [
            ("narrator", "विहान ने मेज़ से सुनहरी चाबी उठाई और टिक-टिक के सीने में लगाकर तीन बार घुमाई। अचानक टिक-टिक की नीली आँखें चमक उठीं!"),
            ("tiktik", "टिक-टिक! नमस्ते नन्हे कारीगर विहान! मेरे पीतल के पंख तैयार हैं, चलो समय रुकने से पहले घंटाघर की ओर चलें!"),
            ("dadaji", "याद रखना विहान, घंटाघर का रक्षक गजराज केवल उसी की बात सुनता है जिसके मन में लालच नहीं, बल्कि सेवा का भाव हो!"),
        ],
    },
    {
        "scene_id": 6, "bg": "sg_bg_clocktower_storm.jpg", "choreo_mode": "storm_run",
        "sfx": "storm_thunder", "fx": "storm_rain_lightning", "prop": "vihaan_lantern",
        "lines": [
            ("narrator", "हाथ में जलती लालटेन और कंधे पर टिक-टिक का बैग टाँगे विहान तेज़ बारिश को चीरता हुआ पहाड़ी नदी की घाटी तक पहुँचा।"),
            ("tiktik", "सावधान विहान! आगे नदी का लकड़ी का पुल तेज़ बहाव में बह चुका है और पानी लगातार ऊपर बढ़ रहा है!"),
            ("vihaan", "अगर पुल टूट गया है तो हम उस पार पहाड़ी की गुफा तक कैसे पहुँचेंगे टिक-टिक? ज़रा ऊपर उड़कर देखो!"),
        ],
    },
    {
        "scene_id": 7, "bg": "sg_bg_river_gears.jpg", "choreo_mode": "river_branch_oil",
        "sfx": "storm_thunder", "fx": "river_mist", "prop": "jammed_branch",
        "lines": [
            ("tiktik", "विहान, यहाँ किनारे पर देखो! पानी के नीचे पत्थर के बड़े-बड़े पहिये बने हैं, जिन्हें उठाने वाला लोहे का लीवर एक भारी टहनी से फँसा है!"),
            ("narrator", "विहान ने अपनी लालटेन पत्थर पर रखी और घुटनों के बल झुककर दोनों हाथों से लीवर में फँसी भारी लकड़ी की टहनी को बाहर खींच निकाला।"),
            ("vihaan", "टहनी तो निकल गई टिक-टिक, लेकिन इस पुराने लोहे के लीवर में तो इतना जंग लगा है कि यह हिल भी नहीं रहा!"),
        ],
    },
    {
        "scene_id": 8, "bg": "sg_bg_river_gears.jpg", "choreo_mode": "river_branch_oil",
        "sfx": "gear_turn", "fx": "golden_sparks", "prop": "pour_oil_lever",
        "lines": [
            ("tiktik", "अपनी झोली में रखी दादाजी की पीतल वाली तेल की कुप्पी निकालो विहान! तेल की बूँदें जंग को तुरंत पिघला देंगी!"),
            ("narrator", "विहान ने तुरंत पीतल की कुप्पी झुकाई और लीवर के जंग लगे दांतों पर सुनहरा तेल डाला। फिर दोनों हाथों से लीवर नीचे खींचा!"),
            ("vihaan", "कड़कड़-कड़कड़! देखो टिक-टिक, नदी के भीतर से पत्थर के विशाल पहिये ऊपर उठकर पुल बन गए हैं!"),
        ],
    },
    {
        "scene_id": 9, "bg": "sg_bg_river_gears.jpg", "choreo_mode": "river_leap",
        "sfx": "gear_turn", "fx": "river_mist", "prop": "vihaan_lantern",
        "lines": [
            ("narrator", "विहान दौड़कर आया और एक पत्थर के पहिये से दूसरे पहिये पर ऊँची छलांग लगाता हुआ उफनती नदी को पार कर गया!"),
            ("tiktik", "वाह विहान! तुमने ताकत के बजाय घड़ीसाज़ की समझदारी से पहला पड़ाव पार कर लिया! अब सामने पवन-गुफा का द्वार है।"),
        ],
    },
    {
        "scene_id": 10, "bg": "sg_bg_wind_cavern.jpg", "choreo_mode": "cavern_wing_fix",
        "sfx": "storm_thunder", "fx": "cavern_wind", "prop": "broken_wing_fall",
        "lines": [
            ("narrator", "जैसे ही वे पहाड़ी की पवन-गुफा में घुसे, एक तेज़ हवा के झोंके ने विहान की लालटेन बुझा दी और पत्थर का एक झरोखा धड़ाम से बंद हुआ!"),
            ("tiktik", "आह! विहान, हवा के झटके से मेरा बायाँ पंख पत्थर की चौखट से टकरा गया और मेरी तांबे की पिन मुड़ गई!"),
            ("vihaan", "ओह नहीं टिक-टिक! ठहरो, मैं दौड़कर आता हूँ! मैं अभी तुम्हारे पंख को ठीक करता हूँ।"),
        ],
    },
    {
        "scene_id": 11, "bg": "sg_bg_wind_cavern.jpg", "choreo_mode": "cavern_wing_fix",
        "sfx": "tick_tock", "fx": "golden_sparks", "prop": "repair_tiktik_wing",
        "lines": [
            ("narrator", "विहान ने घुटनों के बल बैठकर गले में लटकी आवर्धक लेंस आँख पर लगाई और टिक-टिक के पंख की मुड़ी हुई सूक्ष्म पिन को देखा।"),
            ("vihaan", "अरे हाँ, यहाँ सबसे छोटा पेंच ढीला हो गया है। मैं सुनहरी चाबी की नोक से इसे अभी धीरे से सीधा करके कस देता हूँ।"),
            ("tiktik", "टिक-टिक! वाह विहान, तुम्हारे सधे हुए हाथों ने तो मेरा पंख पहले से भी ज़्यादा मज़बूत और हल्का कर दिया!"),
        ],
    },
    {
        "scene_id": 12, "bg": "sg_bg_wind_cavern.jpg", "choreo_mode": "river_leap",
        "sfx": "owl_chime", "fx": "musical_runes", "prop": "golden_key_hand",
        "lines": [
            ("vihaan", "लेकिन टिक-टिक, सामने का यह विशाल पत्थर का दरवाज़ा कैसे खुलेगा? इसके नीचे फर्श पर तीन चमकते हुए पत्थर बने हैं।"),
            ("tiktik", "ऊपर छत से लटकी पीतल की घंटियों को सुनो विहान! हवा जब उनसे टकराती है तो वे 'सा - ग - प' के सुर में बजती हैं!"),
            ("vihaan", "समझ गया! जैसे घड़ी की टिक-टिक का एक निश्चित ताल होता है, वैसे ही हमें इन तीनों पत्थरों पर छलांग लगाकर उन्हें दबाना होगा!"),
        ],
    },
    {
        "scene_id": 13, "bg": "sg_bg_wind_cavern.jpg", "choreo_mode": "river_leap",
        "sfx": "owl_chime", "fx": "musical_runes", "prop": "golden_key_hand",
        "lines": [
            ("narrator", "विहान ने छलांग लगाकर पहला और दूसरा पत्थर अपने कदमों से दबाया, और टिक-टिक ने तेज़ी से गोता लगाकर तीसरे पत्थर पर दस्तक दी!"),
            ("tiktik", "देखो विहान! तीनों सुर मिलते ही पत्थर का भारी दरवाज़ा अपने आप पीछे खिसक गया और घंटाघर की सीढ़ियाँ दिखने लगीं!"),
        ],
    },
    {
        "scene_id": 14, "bg": "sg_bg_tower_interior.jpg", "choreo_mode": "guardian_clash",
        "sfx": "gear_turn", "fx": "workshop_dust", "prop": "golden_key_hand",
        "lines": [
            ("narrator", "सीढ़ियाँ चढ़कर जब विहान और टिक-टिक घंटाघर के विशाल मुख्य कक्ष में दौड़ते हुए पहुँचे, तो वहाँ शांत पड़े सोने के भीमकाय पहिये देखकर दंग रह गए।"),
            ("vihaan", "बाप रे! इतने बड़े-बड़े पीतल के पहिये! और देखो, बीच का मुख्य पेंडुलम तो एक टूटे हुए कुंदे के कारण अटका पड़ा है।"),
        ],
    },
    {
        "scene_id": 15, "bg": "sg_bg_tower_interior.jpg", "choreo_mode": "guardian_clash",
        "sfx": "storm_thunder", "fx": "guardian_aura", "prop": "golden_key_hand",
        "lines": [
            ("narrator", "जैसे ही विहान ने मुख्य पेंडुलम की ओर कदम बढ़ाया, खंभे के पीछे से पत्थर और काँसे का विशाल रक्षक 'गजराज' गरजता हुआ सामने आ खड़ा हुआ!"),
            ("gajraj", "रुक जाओ बालक! इस सूर्य-घंटाघर के मुख्य पेंडुलम को छूने की अनुमति किसी इंसान को नहीं है! तुरंत पीछे हट जाओ!"),
            ("tiktik", "अरे गजराज जी, हम चोर नहीं हैं! मुझे दामोदर घड़ीसाज़ ने भेजा है, नीचे सुंदरगढ़ में बाढ़ का पानी बढ़ रहा है!"),
        ],
    },
    {
        "scene_id": 16, "bg": "sg_bg_tower_interior.jpg", "choreo_mode": "guardian_clash",
        "sfx": "gear_turn", "fx": "guardian_aura", "prop": "golden_key_hand",
        "lines": [
            ("gajraj", "बरसों पहले भी एक व्यापारी मदद का बहाना बनाकर यहाँ आया था, और उसने मुख्य घड़ी का स्वर्ण-चक्र चुराने की कोशिश की थी!"),
            ("vihaan", "गजराज जी, मैं कोई सोना लेने नहीं आया हूँ। मेरे हाथ में केवल मेरे दादाजी की दी हुई चाबी और तेल की कुप्पी है।"),
            ("narrator", "बोलते-बोलते गजराज अचानक अपने सीने पर हाथ रखकर थोड़ा झुका, और उसके सीने के फिरोज़ी चक्र से करकश आवाज़ निकली।"),
        ],
    },
    {
        "scene_id": 17, "bg": "sg_bg_tower_interior.jpg", "choreo_mode": "guardian_heal",
        "sfx": "tick_tock", "fx": "workshop_dust", "prop": "loupe_inspect",
        "lines": [
            ("narrator", "विहान ने डरने के बजाय आगे बढ़कर अपनी आवर्धक लेंस उठाई और गजराज के सीने में लगे घड़ी-चक्र को ध्यान से देखा।"),
            ("vihaan", "अरे! गजराज जी, आपके सीने का मुख्य पेंडुलम तो बिजली के झटके से तिरछा हो गया है! इसी दर्द के कारण आप इतने क्रोधित हैं!"),
            ("gajraj", "क्या कहा बालक? तुम मेरी विशाल काया से डरने के बजाय मेरे सीने के टूटे पहिये का दर्द देख रहे हो?"),
        ],
    },
    {
        "scene_id": 18, "bg": "sg_bg_tower_interior.jpg", "choreo_mode": "guardian_heal",
        "sfx": "tick_tock", "fx": "golden_sparks", "prop": "offer_oil_and_key",
        "lines": [
            ("vihaan", "मेरे दादाजी कहते हैं कि जो रक्षक वर्षों से पूरे नगर की रक्षा कर रहा हो, पहले उसका घाव भरना एक कारीगर का धर्म है।"),
            ("tiktik", "विहान, बाहर पूरब के आकाश में भोर की पहली लाली दिखने लगी है! हमारे पास केवल कुछ ही पल बचे हैं!"),
            ("vihaan", "कोई बात नहीं टिक-टिक! गजराज जी, यदि आप घुटनों के बल बैठ जाएँ, तो मैं पहले आपके हृदय-चक्र को ठीक कर दूँगा।"),
        ],
    },
    {
        "scene_id": 19, "bg": "sg_bg_tower_interior.jpg", "choreo_mode": "guardian_heal",
        "sfx": "gear_turn", "fx": "golden_sparks", "prop": "repair_gajraj_heart",
        "lines": [
            ("narrator", "बालक की निस्वार्थ करुणा देखकर विशाल गजराज शांत होकर घुटनों के बल बैठ गया। विहान ने झुककर उसके सीने के चक्र में तेल डाला और पेंच कस दिया।"),
            ("gajraj", "ओह... वर्षों का जकड़ा हुआ दर्द एक पल में मिट गया! मेरे सीने की घड़ी फिर से मधुर ताल में धड़क रही है!"),
            ("vihaan", "अब आपका हृदय-चक्र बिल्कुल स्वस्थ है गजराज जी! लेकिन अब हमें मुख्य घंटाघर के भारी पहिये को उठाना होगा।"),
        ],
    },
    {
        "scene_id": 20, "bg": "sg_bg_tower_interior.jpg", "choreo_mode": "guardian_heal",
        "sfx": "gear_turn", "fx": "golden_sparks", "prop": "insert_master_key",
        "lines": [
            ("gajraj", "चिंता मत करो नन्हे कारीगर! तुमने मेरा हृदय जोड़ा है, अब मैं अपने दोनों हाथों से इस टूटे हुए महा-चक्र को थामकर रखता हूँ!"),
            ("narrator", "गजराज ने आगे बढ़कर अपनी विशाल भुजाओं से भारी पीतल के पहिये को ऊपर उठाया, टिक-टिक ने गोता लगाकर कमानी पकड़ी, और विहान ने सुनहरी चाबी घुमा दी!"),
            ("vihaan", "एक... दो... और तीन! घूम जाओ सूर्य-घड़ी के पहियो!"),
        ],
    },
    {
        "scene_id": 21, "bg": "sg_bg_tower_interior.jpg", "choreo_mode": "sunrise_finale",
        "sfx": "tower_bell", "fx": "golden_sparks", "prop": "spinning_gears",
        "lines": [
            ("narrator", "चाबी घूमते ही पूरे घंटाघर के हज़ारों सुनहरे पहिये एक साथ तेज़ी से घूमने लगे और विशाल घंटे की मधुर ध्वनि पूरी घाटी में गूँज उठी!"),
            ("tiktik", "डोंग... डोंग... डोंग! विहान, घंटाघर चल पड़ा! और नीचे नदी के बांध के फाटक भी सुरक्षित रूप से खुल गए हैं!"),
            ("gajraj", "धन्यवाद विहान! आज तुमने सिद्ध कर दिया कि सबसे बड़ा जादू किसी हथियार में नहीं, बल्कि सच्चे हुनर और दयालु हृदय में होता है।"),
        ],
    },
    {
        "scene_id": 22, "bg": "sg_bg_clocktower_sunrise.jpg", "choreo_mode": "sunrise_finale",
        "sfx": "tower_bell", "fx": "sunrise_motes", "prop": None,
        "lines": [
            ("narrator", "सूर्योदय की सुनहरी किरणों के साथ सुंदरगढ़ के ऊपर से काले बादल छँट गए। नदी का अतिरिक्त पानी नहरों से होकर खेतों की ओर बह निकला।"),
            ("vihaan", "देखो टिक-टिक, सूरज की रोशनी में हमारा सुंदरगढ़ और यह घंटाघर कितना सुंदर लग रहा है! चलो अब दौड़कर दादाजी के पास चलते हैं।"),
        ],
    },
    {
        "scene_id": 23, "bg": "sg_bg_workshop.jpg", "choreo_mode": "workshop_intro",
        "sfx": "owl_chime", "fx": "workshop_dust", "prop": "master_badge_gift",
        "lines": [
            ("narrator", "जब विहान और टिक-टिक दौड़ते हुए वापस कार्यशाला पहुँचे, तो दादाजी दामोदर ने आगे बढ़कर खुशी के आँसुओं के साथ अपने पोते को गले से लगा लिया।"),
            ("dadaji", "मुझे तुम पर गर्व है विहान! आज से तुम केवल मेरे शिष्य नहीं, बल्कि सुंदरगढ़ के मुख्य घड़ीसाज़ हो!"),
            ("tiktik", "टिक-टिक! और मैं हमेशा तुम्हारे कंधे पर उड़कर हर घड़ी की देखभाल करूँगा!"),
        ],
    },
    {
        "scene_id": 24, "bg": "sg_bg_clocktower_sunrise.jpg", "choreo_mode": "sunrise_finale",
        "sfx": "owl_chime", "fx": "moral_ending", "prop": "spinning_gears",
        "lines": [
            ("narrator", "इस प्रकार नन्हे विहान की सूझबूझ, निस्वार्थ सेवा और धैर्य ने पूरे नगर को बचा लिया।"),
            ("narrator", "यह कहानी हमें सिखाती है कि सच्चा हुनर और निस्वार्थ सेवा बड़े से बड़े संकट को भी मोड़ सकती है।"),
        ],
    },
]


# ==============================================================================
# DYNAMIC MULTI-SHOT CHOREOGRAPHY SOLVER
# Computes:
#   - Active Sub-Shot Camera Framing + Horizontal Tracking Pan (`cam_pan_x`, `cam_submode`)
#   - Active Character Rig (`vihaan_walk` vs `vihaan_kneel` vs `vihaan`, `gajraj` vs `gajraj_action`)
#   - Large-Scale Screen Traversal (`x` across screen, `y` parabolic jump / crouch, `z_scale` depth)
# ==============================================================================
def _solve_dynamic_choreography(choreo_mode: str, progress: float, t: float, width: int, height: int):
    """
    Divides each scene into 4 dynamic sub-shots:
      - Sub-shot 0 (0.00 - 0.25): Wide Tracking Entry / Full-Screen Walk or Run
      - Sub-shot 1 (0.25 - 0.52): Medium Two-Shot / Turn & Approach
      - Sub-shot 2 (0.52 - 0.78): Physical Action Cut (Kneeling, Leaping, Reaching, Repairing)
      - Sub-shot 3 (0.78 - 1.00): Reaction & Walk-Out / Swooping Climax
    Returns `(cam_submode, pan_x, actors_list)` where each item in `actors_list` is:
      `(rig_name, logic_name, cx, foot_y, z_scale, flip_x, fast_anim)`
    """
    sub_idx = 0 if progress < 0.25 else (1 if progress < 0.52 else (2 if progress < 0.78 else 3))
    if sub_idx == 0:
        sp = progress / 0.25
    elif sub_idx == 1:
        sp = (progress - 0.25) / 0.27
    elif sub_idx == 2:
        sp = (progress - 0.52) / 0.26
    else:
        sp = (progress - 0.78) / 0.22

    pan_x = int(math.sin(progress * math.pi * 2.0) * 85)
    actors = []

    if choreo_mode == "workshop_intro":
        if sub_idx == 0:
            # Shot 1: Vihaan walks all the way in from right edge to center in side-stride while Dadaji steps forward
            cam_submode = "wide"
            pan_x = int((0.5 - sp) * 110)
            vx = int(width * (0.92 - sp * 0.40))
            dx = int(width * (0.18 + sp * 0.12))
            actors = [
                ("dadaji", "dadaji", dx, int(height * 0.94), 0.96, False, True),
                ("vihaan_walk", "vihaan", vx, int(height * 0.95), 1.00, True, True),
            ]
        elif sub_idx == 1:
            # Shot 2: Medium Two-Shot — Vihaan turns and gestures, Tik-Tik hops/flies across workbench
            cam_submode = "medium"
            dx = int(width * (0.28 + math.sin(sp * math.pi) * 0.05))
            vx = int(width * (0.64 - sp * 0.08))
            tx = int(width * (0.48 + math.sin(sp * math.pi * 2.0) * 0.12))
            ty = int(height * (0.66 - abs(math.sin(sp * math.pi * 2.0)) * 0.12))
            actors = [
                ("dadaji", "dadaji", dx, int(height * 0.95), 1.02, False, False),
                ("tiktik", "tiktik", tx, ty, 0.92, sp > 0.5, True),
                ("vihaan", "vihaan", vx, int(height * 0.95), 1.02, True, False),
            ]
        elif sub_idx == 2:
            # Shot 3: Action Close-Up — Vihaan kneels down to inspect/work on the clockwork mechanism!
            cam_submode = "closeup"
            dx = int(width * 0.26)
            vx = int(width * (0.54 + sp * 0.04))
            actors = [
                ("dadaji", "dadaji", dx, int(height * 0.95), 1.04, False, False),
                ("vihaan_kneel", "vihaan", vx, int(height * 0.96), 1.08, True, True),
            ]
        else:
            # Shot 4: Vihaan stands up, turns right, and walks across toward the door as Tik-Tik swoops overhead
            cam_submode = "wide"
            vx = int(width * (0.52 + sp * 0.36))
            tx = int(width * (0.40 + sp * 0.45))
            ty = int(height * (0.58 - math.sin(sp * math.pi) * 0.20))
            actors = [
                ("dadaji", "dadaji", int(width * 0.28), int(height * 0.94), 0.98, False, False),
                ("vihaan_walk", "vihaan", vx, int(height * 0.95), 1.00, False, True),
                ("tiktik", "tiktik", tx, ty, 0.95, False, True),
            ]

    elif choreo_mode == "owl_awakening":
        if sub_idx == 0:
            # Dadaji stumbles & sits lower while Vihaan runs from right side to Dadaji
            cam_submode = "medium"
            dy = int(height * (0.93 + sp * 0.08))
            vx = int(width * (0.84 - sp * 0.34))
            actors = [
                ("dadaji", "dadaji", int(width * 0.26), dy, 0.98, False, True),
                ("vihaan_walk", "vihaan", vx, int(height * 0.95), 1.00, True, True),
            ]
        elif sub_idx == 1:
            # Vihaan kneels at workbench to pick up Golden Key & wind Tik-Tik
            cam_submode = "closeup"
            actors = [
                ("dadaji", "dadaji", int(width * 0.22), int(height * 1.00), 0.96, False, False),
                ("vihaan_kneel", "vihaan", int(width * 0.48), int(height * 0.96), 1.06, False, True),
                ("tiktik", "tiktik", int(width * 0.64), int(height * (0.74 - sp * 0.16)), 0.90 + sp * 0.15, True, True),
            ]
        elif sub_idx == 2:
            # Tik-Tik awakens and flies in a huge 3D loop across the workshop while Vihaan watches in awe!
            cam_submode = "wide"
            tx = int(width * (0.50 + math.cos(sp * math.pi * 2.0) * 0.32))
            ty = int(height * (0.48 + math.sin(sp * math.pi * 2.0) * 0.18))
            tz = 0.75 + 0.35 * (0.5 + 0.5 * math.sin(sp * math.pi * 2.0))
            actors = [
                ("dadaji", "dadaji", int(width * 0.24), int(height * 0.98), 0.96, False, False),
                ("vihaan", "vihaan", int(width * 0.52), int(height * 0.95), 1.00, sp > 0.5, True),
                ("tiktik", "tiktik", tx, ty, tz, math.sin(sp * math.pi * 2.0) > 0, True),
            ]
        else:
            # Vihaan & Tik-Tik sprint out the door toward the Clocktower!
            cam_submode = "wide"
            vx = int(width * (0.45 + sp * 0.48))
            tx = int(width * (0.50 + sp * 0.46))
            ty = int(height * (0.46 - math.sin(sp * math.pi) * 0.14))
            actors = [
                ("dadaji", "dadaji", int(width * 0.24), int(height * 0.96), 0.96, False, False),
                ("vihaan_walk", "vihaan", vx, int(height * 0.95), 1.02, False, True),
                ("tiktik", "tiktik", tx, ty, 1.00, False, True),
            ]

    elif choreo_mode == "storm_run":
        if sub_idx == 0:
            # Z-Depth Run: Vihaan runs from far down the cobblestone road (small in background) toward foreground!
            cam_submode = "wide"
            vx = int(width * (0.48 - sp * 0.16))
            vy = int(height * (0.72 + sp * 0.22))
            vz = 0.52 + sp * 0.48
            tx = int(width * (0.54 + math.sin(sp * math.pi * 2.0) * 0.18))
            ty = int(height * (0.45 + sp * 0.12))
            actors = [
                ("vihaan_walk", "vihaan", vx, vy, vz, False, True),
                ("tiktik", "tiktik", tx, ty, vz, False, True),
            ]
        elif sub_idx == 1:
            # Medium Shot: Vihaan stops, looks up at the lightning-struck Clocktower, and gestures
            cam_submode = "medium"
            actors = [
                ("vihaan", "vihaan", int(width * (0.36 + sp * 0.06)), int(height * 0.95), 1.04, False, False),
                ("dadaji", "dadaji", int(width * (0.74 - sp * 0.08)), int(height * 0.95), 1.00, True, False),
            ]
        elif sub_idx == 2:
            # Fast Horizontal Tracking Run: Vihaan sprints across the storm street from left to right!
            cam_submode = "wide"
            pan_x = int((sp - 0.5) * 160)
            vx = int(width * (0.10 + sp * 0.76))
            tx = int(width * (0.18 + sp * 0.74))
            ty = int(height * (0.48 + math.sin(sp * math.pi * 3.0) * 0.12))
            actors = [
                ("vihaan_walk", "vihaan", vx, int(height * 0.95), 1.02, False, True),
                ("tiktik", "tiktik", tx, ty, 0.96, False, True),
            ]
        else:
            # Close-up urgent exchange before entering the gorge
            cam_submode = "closeup"
            actors = [
                ("vihaan", "vihaan", int(width * 0.42), int(height * 0.96), 1.08, False, True),
                ("tiktik", "tiktik", int(width * (0.64 - sp * 0.08)), int(height * (0.56 + math.sin(sp * 6.0) * 0.06)), 1.05, True, True),
            ]

    elif choreo_mode == "river_branch_oil":
        if sub_idx == 0:
            # Vihaan runs into the river gorge from the left edge while Tik-Tik swoops down to the jammed lever on the right
            cam_submode = "wide"
            vx = int(width * (0.06 + sp * 0.32))
            tx = int(width * (0.20 + sp * 0.56))
            ty = int(height * (0.34 + sp * 0.30))
            actors = [
                ("vihaan_walk", "vihaan", vx, int(height * 0.94), 0.98, False, True),
                ("tiktik", "tiktik", tx, ty, 0.95, False, True),
            ]
        elif sub_idx == 1:
            # Vihaan kneels down at the lever (`vihaan_kneel`) pulling the heavy branch and pouring golden oil!
            cam_submode = "closeup"
            vx = int(width * (0.44 + math.sin(sp * math.pi * 3.0) * 0.03))
            actors = [
                ("vihaan_kneel", "vihaan", vx, int(height * 0.96), 1.08, False, True),
                ("tiktik", "tiktik", int(width * 0.68), int(height * (0.58 + math.sin(sp * 6.0) * 0.05)), 1.00, True, True),
            ]
        elif sub_idx == 2:
            # Medium Shot: Vihaan pulls the lever back with full body shift as giant stone gears rise out of the water!
            cam_submode = "medium"
            vx = int(width * (0.48 - sp * 0.12))
            actors = [
                ("vihaan_kneel", "vihaan", vx, int(height * 0.95), 1.04, False, True),
                ("tiktik", "tiktik", int(width * (0.66 - sp * 0.16)), int(height * (0.44 - sp * 0.08)), 0.98, True, True),
            ]
        else:
            # Vihaan stands up triumphantly and prepares to leap across the risen gear stones
            cam_submode = "wide"
            actors = [
                ("vihaan", "vihaan", int(width * (0.32 + sp * 0.12)), int(height * 0.94), 1.00, False, True),
                ("tiktik", "tiktik", int(width * (0.52 + sp * 0.24)), int(height * (0.48 + math.sin(sp * 6.0) * 0.08)), 0.95, False, True),
            ]

    elif choreo_mode == "river_leap":
        # 3 Huge Parabolic Jumps Across the River Gears / Musical Rune Stones!
        if sub_idx < 3:
            cam_submode = "wide" if sub_idx != 1 else "medium"
            # Each sub_idx (0, 1, 2) is ONE full parabolic jump from stone_i to stone_{i+1}!
            x_starts = [0.14, 0.38, 0.62]
            x_ends = [0.38, 0.62, 0.86]
            sx, ex = x_starts[sub_idx], x_ends[sub_idx]
            vx = int(width * (sx + (ex - sx) * sp))
            # Parabolic arc: peak height of 175 pixels in the middle of the jump!
            jump_arc = int(4.0 * sp * (1.0 - sp) * 175)
            vy = int(height * 0.93) - jump_arc
            # Squash on takeoff/landing, stretch at apex
            vz = 0.94 + 0.12 * (4.0 * sp * (1.0 - sp))
            tx = int(width * (sx + 0.10 + (ex - sx) * sp))
            ty = int(height * (0.42 - 0.12 * math.sin(sp * math.pi)))
            actors = [
                ("vihaan_walk", "vihaan", vx, vy, vz, False, True),
                ("tiktik", "tiktik", tx, ty, 0.96, False, True),
            ]
        else:
            # Sub-shot 3: Landing on the far bank & cheering together!
            cam_submode = "medium"
            actors = [
                ("vihaan", "vihaan", int(width * 0.72), int(height * 0.94), 1.02, True, False),
                ("tiktik", "tiktik", int(width * 0.54), int(height * (0.54 + math.sin(sp * 6.0) * 0.05)), 1.00, False, True),
            ]

    elif choreo_mode == "cavern_wing_fix":
        if sub_idx == 0:
            # Wind gusts in cavern: Tik-Tik tumbles downward from top-right to the stone floor (`y: 0.32 -> 0.86`)!
            cam_submode = "wide"
            vx = int(width * (0.12 + sp * 0.24))
            tx = int(width * (0.76 - sp * 0.18))
            ty = int(height * (0.32 + sp * 0.52))
            actors = [
                ("vihaan_walk", "vihaan", vx, int(height * 0.94), 0.98, False, True),
                ("tiktik", "tiktik", tx, ty, 0.95, True, True),
            ]
        elif sub_idx == 1:
            # Vihaan runs over and kneels down (`vihaan_kneel`) right beside fallen Tik-Tik on the floor
            cam_submode = "closeup"
            actors = [
                ("vihaan_kneel", "vihaan", int(width * 0.44), int(height * 0.95), 1.08, False, True),
                ("tiktik", "tiktik", int(width * 0.60), int(height * 0.84), 1.02, True, False),
            ]
        elif sub_idx == 2:
            # Vihaan tightens Tik-Tik's wing pin with the Golden Key -> Tik-Tik launches upward into the air!
            cam_submode = "medium"
            ty = int(height * (0.82 - sp * 0.38))
            tx = int(width * (0.60 + math.sin(sp * math.pi * 2.0) * 0.14))
            actors = [
                ("vihaan_kneel", "vihaan", int(width * 0.42), int(height * 0.95), 1.02, False, True),
                ("tiktik", "tiktik", tx, ty, 1.00, True, True),
            ]
        else:
            # Both walk forward toward the glowing musical rune door
            cam_submode = "wide"
            vx = int(width * (0.42 + sp * 0.28))
            actors = [
                ("vihaan_walk", "vihaan", vx, int(height * 0.94), 1.00, False, True),
                ("tiktik", "tiktik", vx + 90, int(height * 0.50), 0.96, False, True),
            ]

    elif choreo_mode == "guardian_clash":
        if sub_idx == 0:
            # Vihaan runs in from left toward the giant Master Pendulum; Gajraj emerges from behind the right pillar!
            cam_submode = "wide"
            vx = int(width * (0.08 + sp * 0.26))
            gx = int(width * (0.88 - sp * 0.20))
            actors = [
                ("vihaan_walk", "vihaan", vx, int(height * 0.94), 0.96, False, True),
                ("tiktik", "tiktik", vx + 70, int(height * 0.48), 0.90, False, True),
                ("gajraj", "gajraj", gx, int(height * 0.95), 1.05, False, True),
            ]
        elif sub_idx == 1:
            # Low-Angle Imposing Shot: Gajraj switches to his Dynamic Action Reach Rig (`gajraj_action`) & steps forward!
            cam_submode = "low_angle"
            gx = int(width * (0.68 - sp * 0.08))
            vx = int(width * (0.34 - sp * 0.06))
            actors = [
                ("vihaan", "vihaan", vx, int(height * 0.95), 0.98, False, False),
                ("gajraj_action", "gajraj", gx, int(height * 0.96), 1.12, False, True),
            ]
        elif sub_idx == 2:
            # Medium Two-Shot: Tik-Tik swoops between them while Vihaan holds up the Golden Key & Oil Can
            cam_submode = "medium"
            tx = int(width * (0.36 + sp * 0.24))
            ty = int(height * (0.44 + math.sin(sp * math.pi * 2.0) * 0.10))
            actors = [
                ("vihaan", "vihaan", int(width * 0.30), int(height * 0.95), 1.02, False, False),
                ("tiktik", "tiktik", tx, ty, 0.98, False, True),
                ("gajraj", "gajraj", int(width * 0.68), int(height * (0.95 + sp * 0.04)), 1.04, False, False),
            ]
        else:
            # Close-up as Vihaan steps closer to inspect Gajraj's cracked turquoise chest-gear
            cam_submode = "closeup"
            vx = int(width * (0.32 + sp * 0.12))
            actors = [
                ("vihaan_walk", "vihaan", vx, int(height * 0.95), 1.04, False, True),
                ("gajraj_action", "gajraj", int(width * 0.66), int(height * 0.98), 1.06, False, False),
            ]

    elif choreo_mode == "guardian_heal":
        if sub_idx == 0:
            # Gajraj kneels down (`foot_y` drops by 110px!) as Vihaan approaches with oil can & key
            cam_submode = "medium"
            gy = int(height * (0.95 + sp * 0.11))
            vx = int(width * (0.32 + sp * 0.12))
            actors = [
                ("vihaan_walk", "vihaan", vx, int(height * 0.95), 1.02, False, True),
                ("gajraj", "gajraj", int(width * 0.64), gy, 1.02, False, False),
            ]
        elif sub_idx == 1:
            # Close-Up Action: Vihaan kneels (`vihaan_kneel`) and works directly on Gajraj's chest-gear!
            cam_submode = "closeup"
            actors = [
                ("vihaan_kneel", "vihaan", int(width * 0.45), int(height * 0.95), 1.08, False, True),
                ("gajraj", "gajraj", int(width * 0.62), int(height * 1.06), 1.04, False, False),
            ]
        elif sub_idx == 2:
            # Healed Gajraj rises up in his `gajraj_action` pose to lift the giant broken tower gear while Vihaan winds the Master Pendulum!
            cam_submode = "wide"
            gy = int(height * (1.04 - sp * 0.10))
            actors = [
                ("gajraj_action", "gajraj", int(width * 0.34), gy, 1.08, True, True),
                ("vihaan_kneel", "vihaan", int(width * 0.56), int(height * 0.95), 1.02, False, True),
                ("tiktik", "tiktik", int(width * 0.56), int(height * (0.36 + math.sin(sp * 8.0) * 0.06)), 0.96, True, True),
            ]
        else:
            # All giant golden gears start spinning as all three celebrate!
            cam_submode = "wide"
            actors = [
                ("gajraj_action", "gajraj", int(width * 0.30), int(height * 0.94), 1.04, True, True),
                ("vihaan", "vihaan", int(width * 0.58), int(height * 0.94), 1.02, True, True),
                ("tiktik", "tiktik", int(width * (0.72 - sp * 0.24)), int(height * 0.44), 1.00, True, True),
            ]

    else:  # "sunrise_finale"
        if sub_idx == 0:
            cam_submode = "wide"
            vx = int(width * (0.18 + sp * 0.30))
            tx = int(width * (0.82 - sp * 0.32))
            ty = int(height * (0.34 + math.sin(sp * math.pi) * 0.16))
            actors = [
                ("dadaji", "dadaji", int(width * 0.24), int(height * 0.94), 0.98, False, False),
                ("vihaan_walk", "vihaan", vx, int(height * 0.94), 1.00, False, True),
                ("tiktik", "tiktik", tx, ty, 0.98, True, True),
            ]
        elif sub_idx == 1:
            cam_submode = "medium"
            actors = [
                ("dadaji", "dadaji", int(width * 0.32), int(height * 0.95), 1.02, False, False),
                ("vihaan", "vihaan", int(width * 0.56), int(height * 0.95), 1.02, True, False),
                ("tiktik", "tiktik", int(width * 0.72), int(height * 0.52), 1.00, True, True),
            ]
        else:
            cam_submode = "wide"
            tx = int(width * (0.50 + math.sin(sp * math.pi * 2.0) * 0.28))
            ty = int(height * (0.42 + math.cos(sp * math.pi * 2.0) * 0.10))
            actors = [
                ("dadaji", "dadaji", int(width * 0.28), int(height * 0.94), 1.00, False, False),
                ("vihaan", "vihaan", int(width * 0.52), int(height * 0.94), 1.00, False, False),
                ("tiktik", "tiktik", tx, ty, 0.98, False, True),
            ]

    return cam_submode, pan_x, actors


def _draw_prop_and_fx(
    frame: Image.Image,
    draw: ImageDraw.ImageDraw,
    fx_type: str,
    prop_type: str,
    bg_name: str,
    width: int,
    height: int,
    t: float,
    progress: float,
    actor_positions: dict,
    moral_badge: Image.Image = None,
):
    # Keep 4K Pixar background pure without 2D corner gear overlays
    if False:
        pass

    if fx_type == "workshop_dust":
        for i in range(22):
            px = int((i * 83 + t * 38 + math.sin(t * 1.8 + i) * 24) % width)
            py = int((i * 61 - t * 28) % height)
            r = 3 + (i % 3)
            draw.ellipse([px - r, py - r, px + r, py + r], fill=(255, 225, 130, 160))

    elif fx_type == "storm_rain_lightning":
        for i in range(48):
            rx = int((i * 47 + t * 560) % width)
            ry = int((i * 73 + t * 1120) % height)
            draw.line([(rx, ry), (rx - 20, ry + 44)], fill=(195, 225, 255, 180), width=2)
        if int(t * 3.5) % 13 == 0:
            draw.rectangle([0, 0, width, height], fill=(235, 245, 255, 75))

    elif fx_type == "river_mist":
        for i in range(14):
            wx = int(width * (0.10 + i * 0.065) + math.sin(t * 4.5 + i) * 38)
            wy = int(height * (0.78 + (i % 3) * 0.05))
            draw.arc([wx - 48, wy - 10, wx + 48, wy + 10], start=5, end=175, fill=(160, 240, 255, 210), width=4)

    elif fx_type == "cavern_wind":
        for i in range(20):
            wx = int((i * 97 + t * 760) % width)
            wy = int(height * (0.20 + (i % 7) * 0.10) + math.sin(t * 5.5 + i) * 20)
            draw.line([(wx, wy), (wx + 75, wy - 8)], fill=(200, 230, 255, 150), width=3)

    elif fx_type == "musical_runes":
        colors = [(56, 189, 248), (250, 204, 21), (52, 211, 153)]
        for idx, col in enumerate(colors):
            rx = int(width * (0.34 + idx * 0.16))
            ry = int(height * 0.89)
            active = progress > (idx * 0.25)
            alpha = 235 if active else 95
            draw.ellipse([rx - 46, ry - 18, rx + 46, ry + 18], fill=(*col, alpha), outline=(255, 255, 255, 225), width=3)
            if active:
                rad = int(((t * 110 + idx * 30) % 130))
                draw.ellipse([rx - rad, ry - rad // 2, rx + rad, ry + rad // 2], outline=(*col, 190), width=3)

    elif fx_type == "guardian_aura":
        gx, gy = actor_positions.get("gajraj", (int(width * 0.68), int(height * 0.60)))
        for r in range(3):
            rad = 90 + r * 45 + int(math.sin(t * 5.5 + r) * 16)
            draw.ellipse([gx - rad, gy - 260 - rad, gx + rad, gy - 260 + rad], outline=(45, 212, 191, 135 - r * 35), width=4)

    elif fx_type in ("golden_sparks", "sunrise_motes", "moral_ending"):
        for i in range(38):
            px = int((i * 67 + t * 65 + math.sin(t * 2.8 + i) * 34) % width)
            py = int((i * 53 - t * 55) % height)
            r = 4 + (i % 4)
            draw.ellipse([px - r, py - r, px + r, py + r], fill=(255, 215, 60, 220))

    vx, vy = actor_positions.get("vihaan", (int(width * 0.5), int(height * 0.85)))
    tx, ty = actor_positions.get("tiktik", (int(width * 0.6), int(height * 0.55)))
    gx, gy = actor_positions.get("gajraj", (int(width * 0.66), int(height * 0.85)))

    def _draw_golden_key(kx, ky):
        draw.ellipse([kx - 16, ky - 16, kx + 16, ky + 16], outline=(255, 215, 0, 255), width=5)
        draw.line([(kx + 14, ky), (kx + 46, ky)], fill=(255, 215, 0, 255), width=6)
        draw.line([(kx + 36, ky), (kx + 36, ky + 12)], fill=(255, 215, 0, 255), width=4)
        draw.line([(kx + 44, ky), (kx + 44, ky + 12)], fill=(255, 215, 0, 255), width=4)

    def _draw_oil_can(ox, oy, tilted=False):
        draw.polygon([(ox - 18, oy + 14), (ox + 18, oy + 14), (ox + 12, oy - 12), (ox - 12, oy - 12)], fill=(218, 165, 32, 255), outline=(120, 80, 10, 255))
        if tilted:
            draw.line([(ox + 12, oy - 4), (ox + 38, oy + 16)], fill=(218, 165, 32, 255), width=4)
            for d_i in range(3):
                dy = oy + 20 + int(((t * 150 + d_i * 22) % 55))
                draw.ellipse([ox + 36, dy, ox + 44, dy + 10], fill=(255, 215, 0, 240))
        else:
            draw.line([(ox + 12, oy - 6), (ox + 34, oy - 18)], fill=(218, 165, 32, 255), width=4)

    if prop_type == "table_key_and_oil":
        _draw_golden_key(int(width * 0.48), int(height * 0.74))
        _draw_oil_can(int(width * 0.55), int(height * 0.74), tilted=False)
    elif prop_type == "pickup_key_and_oil":
        if progress < 0.35:
            _draw_golden_key(int(width * 0.48), int(height * 0.74))
            _draw_oil_can(int(width * 0.55), int(height * 0.74), tilted=False)
        else:
            _draw_golden_key(vx + 55, vy - 190)
            _draw_oil_can(vx - 45, vy - 185, tilted=False)
    elif prop_type in ("wind_tiktik", "repair_tiktik_wing"):
        _draw_golden_key(vx + 65, vy - 180)
    elif prop_type == "vihaan_lantern":
        lx, ly = vx + 58, vy - 235
        draw.rounded_rectangle([lx - 14, ly - 22, lx + 14, ly + 22], radius=5, fill=(255, 200, 60, 235), outline=(90, 50, 20, 255), width=3)
        draw.ellipse([lx - 48, ly - 48, lx + 48, ly + 48], fill=(255, 220, 100, 75))
    elif prop_type == "jammed_branch":
        bx_off = 0 if progress < 0.45 else int((progress - 0.45) * 420)
        bx, by = int(width * 0.48) - bx_off, int(height * 0.80)
        draw.line([(bx - 75, by - 25), (bx + 85, by + 22)], fill=(105, 65, 30, 255), width=14)
    elif prop_type == "pour_oil_lever":
        _draw_oil_can(vx + 68, vy - 175, tilted=(0.20 < progress < 0.82))
    elif prop_type in ("golden_key_hand", "insert_master_key"):
        _draw_golden_key(vx + 55, vy - 210)
    elif prop_type == "offer_oil_and_key":
        _draw_golden_key(vx + 52, vy - 220)
        _draw_oil_can(vx - 48, vy - 210, tilted=False)
    elif prop_type == "repair_gajraj_heart":
        _draw_oil_can(gx - 45, gy - 260, tilted=(progress < 0.65))
        _draw_golden_key(gx + 30, gy - 250)
    elif prop_type == "master_badge_gift":
        dx, dy = actor_positions.get("dadaji", (int(width * 0.34), int(height * 0.85)))
        bx = int(dx + (vx - dx) * min(progress * 1.4, 1.0))
        by = vy - 250
        draw.ellipse([bx - 22, by - 22, bx + 22, by + 22], fill=(255, 215, 0, 255), outline=(185, 28, 28, 255), width=4)

    if fx_type == "moral_ending" and moral_badge is not None:
        mx = (width - moral_badge.width) // 2
        my = int(height * 0.10)
        frame.paste(moral_badge, (mx, my), moral_badge)


def _prepare_subshot_bg_bank(raw_bg: Image.Image, width: int, height: int) -> dict:
    """Pre-builds Wide Overscanned (for horizontal camera pan), Medium, Close-up, and Low-Angle plates."""
    wide_overscan = raw_bg.resize((int(width * 1.18), height), Image.Resampling.LANCZOS)
    base = raw_bg.resize((width, height), Image.Resampling.LANCZOS)

    cw_m, ch_m = int(width * 0.82), int(height * 0.82)
    med = base.crop(((width - cw_m) // 2, int(height * 0.10), (width + cw_m) // 2, int(height * 0.10) + ch_m)).resize((width, height), Image.Resampling.LANCZOS)

    cw_c, ch_c = int(width * 0.72), int(height * 0.72)
    cls = base.crop(((width - cw_c) // 2, int(height * 0.14), (width + cw_c) // 2, int(height * 0.14) + ch_c)).resize((width, height), Image.Resampling.LANCZOS)

    cw_l, ch_l = int(width * 0.82), int(height * 0.82)
    low = base.crop(((width - cw_l) // 2, int(height * 0.04), (width + cw_l) // 2, int(height * 0.04) + ch_l)).resize((width, height), Image.Resampling.LANCZOS)

    return {"wide_overscan": wide_overscan, "wide": base, "medium": med, "closeup": cls, "low_angle": low}


def build_and_upload_samay_ghadi_movie():
    print("=" * 72)
    print("🎬 BUILDING 96-SHOT DYNAMIC 3D ANIMATED FILM: समय की टूटी घड़ी और नन्हा कारीगर")
    print("=" * 72)

    _ensure_sg_pose_bank()
    width, height, anim_fps, out_fps = 1920, 1080, 12, 24
    sr = 24000
    moral_badge = render_hindi_title_badge("सच्चा हुनर और निस्वार्थ सेवा ही सबसे बड़ा जादू है।", font_size=48)

    master_wav = os.path.join(OUTPUT_DIR, "samay_ghadi_master_audio.wav")
    existing_mp4 = os.path.join(OUTPUT_DIR, "samay_ghadi_3d_animated_movie.mp4")
    scene_timelines = []

    if os.path.exists(existing_mp4) and os.path.getsize(existing_mp4) > 1000000:
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        subprocess.run(
            [ff, "-y", "-i", existing_mp4, "-vn", "-ac", "1", "-ar", str(sr), master_wav],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        with wave.open(master_wav, "rb") as wf:
            total_dur = wf.getnframes() / float(sr)
        total_chars = sum(sum(len(txt) for _, txt in sp["lines"]) for sp in SCENES_SPEC)
        for spec in SCENES_SPEC:
            sc_chars = sum(len(txt) for _, txt in spec["lines"])
            sc_dur = total_dur * (sc_chars / float(total_chars))
            timeline = []
            cur_s = 0.0
            for spk, txt in spec["lines"]:
                l_dur = sc_dur * (len(txt) / float(sc_chars))
                timeline.append((cur_s, cur_s + l_dur, spk))
                cur_s += l_dur
            scene_timelines.append((spec, timeline, sc_dur))
    else:
        total_samples = 0
        with wave.open(master_wav, "wb") as out_wf:
            out_wf.setnchannels(1)
            out_wf.setsampwidth(2)
            out_wf.setframerate(sr)

            for spec in SCENES_SPEC:
                sid = spec["scene_id"]
                timeline = []
                cursor_sec = 0.0
                scene_pcm_parts = []

                for l_idx, (spk, text) in enumerate(spec["lines"]):
                    wav_path = os.path.join(TEMP_DIR, f"sg_s{sid}_l{l_idx}.wav")
                    synthesize_line(spk, text, wav_path)
                    with wave.open(wav_path, "rb") as lw:
                        raw_bytes = lw.readframes(lw.getnframes())
                        pcm = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                    dur = len(pcm) / float(sr)
                    timeline.append((cursor_sec, cursor_sec + dur, spk))
                    scene_pcm_parts.append(pcm)
                    cursor_sec += dur

                dialogue_arr = np.concatenate(scene_pcm_parts) if scene_pcm_parts else np.zeros(sr * 4, dtype=np.float32)
                sfx_bgm_arr = _make_sfx_plus_bgm_samples(spec.get("sfx", "tick_tock"), len(dialogue_arr), sr=sr, scene_offset_sec=total_samples / float(sr))
                mixed = np.clip((dialogue_arr * 0.92 + sfx_bgm_arr) * 32767.0, -32767.0, 32767.0).astype(np.int16)
                out_wf.writeframes(mixed.tobytes())

                scene_dur = len(mixed) / float(sr)
                scene_timelines.append((spec, timeline, scene_dur))
                total_samples += len(mixed)
        total_dur = total_samples / float(sr)
    print(f"⏱️ Master Audio Ready: {total_dur / 60.0:.2f} minutes ({total_dur:.1f}s)")

    out_mp4 = os.path.join(OUTPUT_DIR, "samay_ghadi_3d_animated_movie.mp4")
    out_mp4_tmp = os.path.join(OUTPUT_DIR, "samay_ghadi_3d_tmp.mp4")
    out_thumb = os.path.join(OUTPUT_DIR, "samay_ghadi_3d_thumb.jpg")

    thumb_bg = Image.open(os.path.join(SG_DIR, "sg_thumb_master.jpg")).convert("RGBA").resize((1280, 720), Image.Resampling.LANCZOS)
    title_badge = render_hindi_title_badge("समय की टूटी घड़ी", font_size=64)
    thumb_bg.paste(title_badge, (36, 26), title_badge)
    thumb_bg.convert("RGB").save(out_thumb, "JPEG", quality=95)

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ff, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24", "-s", f"{width}x{height}", "-r", str(anim_fps),
        "-i", "-",
        "-i", master_wav,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "19",
        "-r", str(out_fps), "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        out_mp4_tmp
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    cur_bg_name = None
    bank = None
    for spec, timeline, duration in scene_timelines:
        sid = spec["scene_id"]
        bg_name = spec["bg"]
        if bg_name != cur_bg_name:
            raw_bg = Image.open(os.path.join(SG_DIR, bg_name)).convert("RGBA")
            bank = _prepare_subshot_bg_bank(raw_bg, width, height)
            cur_bg_name = bg_name

        choreo_mode = spec.get("choreo_mode", "workshop_intro")
        print(f"  -> Streaming 4-Cut Dynamic Scene {sid}/24 ({duration:.1f}s | Mode: {choreo_mode})...")
        n_frames = max(1, int(round(duration * anim_fps)))
        fx_type = spec.get("fx")
        prop_type = spec.get("prop")

        for f_i in range(n_frames):
            t = f_i / float(anim_fps)
            progress = min(max(t / duration, 0.0), 1.0)
            cur_spk = "narrator"
            for st, et, spk in timeline:
                if st <= t <= et:
                    cur_spk = spk
                    break

            cam_submode, pan_x, dynamic_actors = _solve_dynamic_choreography(choreo_mode, progress, t, width, height)

            if cam_submode == "wide":
                overscan = bank["wide_overscan"]
                max_off = overscan.width - width
                ox = max(0, min(max_off, (max_off // 2) + pan_x))
                frame = overscan.crop((ox, 0, ox + width, height)).copy()
            else:
                frame = bank.get(cam_submode, bank["wide"]).copy()

            draw = ImageDraw.Draw(frame, "RGBA")
            actor_pos_map = {}

            for rig_name, logic_name, cx, foot_y, z_scale, flip_x, fast_anim in dynamic_actors:
                is_speaking = (cur_spk == logic_name) or (cur_spk == "narrator" and logic_name == "vihaan" and int(t * 2) % 3 == 0)
                p_speed = 11.5 if logic_name == "tiktik" else (9.5 if (fast_anim or is_speaking) else 5.0)
                p_idx = int(t * p_speed) % 12

                if not is_speaking:
                    m_state = "closed"
                else:
                    m_cycle = int(t * 13.5) % 4
                    m_state = "open" if m_cycle in (1, 3) else ("half" if m_cycle == 2 else "closed")

                spr = SG_POSE_BANK[(rig_name, m_state, p_idx, flip_x)]
                if abs(z_scale - 1.0) > 0.04:
                    sw = max(20, int(spr.width * z_scale))
                    sh = max(20, int(spr.height * z_scale))
                    spr = spr.resize((sw, sh), Image.Resampling.BILINEAR)

                bob = 0 if logic_name == "tiktik" else int(abs(math.sin(t * 9.0)) * (16 if fast_anim else 5))
                sh_w = int(spr.width * 0.26)
                sh_y = int(height * 0.91) if logic_name == "tiktik" else min(int(height * 0.94), foot_y - 16)
                draw.ellipse([cx - sh_w, sh_y - 10, cx + sh_w, sh_y + 10], fill=(0, 0, 0, 85))

                px = cx - spr.width // 2
                py = foot_y - spr.height + 30 - bob
                frame.paste(spr, (px, py), spr)
                actor_pos_map[logic_name] = (cx, foot_y)

            _draw_prop_and_fx(frame, draw, fx_type, prop_type, bg_name, width, height, t, progress, actor_pos_map, moral_badge=moral_badge)
            proc.stdin.write(frame.convert("RGB").tobytes())

    proc.stdin.close()
    proc.wait()
    bank = None
    SG_POSE_BANK.clear()
    GEAR_SPRITES.clear()
    import gc
    gc.collect()
    if os.path.exists(out_mp4_tmp):
        subprocess.run([
            ff, "-y", "-i", out_mp4_tmp,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-maxrate", "650k", "-bufsize", "1300k", "-threads", "2",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-c:a", "copy", out_mp4
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(out_mp4_tmp)
    if os.path.exists(master_wav):
        os.remove(master_wav)

    if os.path.exists(master_wav):
        os.remove(master_wav)

    print(f"✅ 96-Shot Dynamic 1080p MP4 Ready ({round(os.path.getsize(out_mp4)/(1024*1024), 2)} MB): {out_mp4}")

    plan = {
        "title": "समय की टूटी घड़ी और नन्हा कारीगर 🕰️✨ | Samay Ki Tooti Ghadi | 3D Animated Hindi Kahani",
        "description": (
            "समय की टूटी घड़ी और नन्हा कारीगर (The Broken Clock of Time & The Young Watchmaker) — "
            "एक नन्हे घड़ीसाज़ विहान, उसके दादाजी दामोदर, पीतल के जादुई उल्लू टिक-टिक और घंटाघर के विशाल रक्षक गजराज की "
            "दिल छू लेने वाली 3D एनिमेटेड हिंदी कहानी!\n\n"
            "✨ कहानी की सीख: सच्चा हुनर और निस्वार्थ सेवा बड़े से बड़े संकट को भी मोड़ सकती है।\n\n"
            "#hindikahani #3danimatedstory #moralstoriesinhindi #jaaduikahani #samaykighadi #bedtimestories"
        ),
        "tags": [
            "समय की टूटी घड़ी", "Hindi Kahani", "Moral Stories in Hindi",
            "Jaadui Kahani", "3D Animated Hindi Story", "Samay Ki Ghadi Kahani",
            "Kahaniya in Hindi", "Kids Moral Story Hindi"
        ],
        "first_comment": "🕰️✨ आपको नन्हे कारीगर विहान और पीतल के उल्लू टिक-टिक की यह 3D कहानी कैसी लगी? कमेंट में ज़रूर बताएं और चैनल को Subscribe करें! 👇"
    }

    vid_id = upload_to_youtube(
        video_path=out_mp4,
        thumbnail_path=out_thumb,
        plan=plan,
        video_type="long",
    )
    print(f"🎉 DONE! Output file: {out_mp4} | YouTube ID: {vid_id}")
    return out_mp4, out_thumb, vid_id, total_dur


if __name__ == "__main__":
    build_and_upload_samay_ghadi_movie()
