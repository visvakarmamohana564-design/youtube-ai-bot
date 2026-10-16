#!/usr/bin/env python3
"""CLOUD AUTO — Fact-or-Myth Shorts (GitHub Actions).
Roz ek fact khud chunta hai -> image (Openverse) -> Hindi awaaz (edge-tts/gTTS)
-> 9:16 vertical video -> YouTube auto-upload (#shorts).
Usage: python cloud_shorts_factmyth.py [--upload]"""
import os, sys, math, json, subprocess, shutil, asyncio, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests

W, H, FPS = 1080, 1920, 30
FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe")
BASE = os.path.dirname(os.path.abspath(__file__))
TMP = "/tmp/fmshort"
os.makedirs(TMP, exist_ok=True)
os.makedirs(os.path.join(BASE, "output"), exist_ok=True)

FACTS = [
    dict(q="octopus underwater", stmt="Octopus ke TEEN DIL hote hain!", fact=True,
         stmt_hi="Octopus के तीन दिल होते हैं!", title="Octopus ke 3 Dil? FACT ya MYTH",
         ex_hi="Octopus के सचमुच तीन दिल होते हैं। दो दिल gills को खून भेजते हैं, और एक दिल पूरे शरीर को।",
         ex1="2 dil → gills ko khoon", ex2="1 dil → pure shareer ko",
         bo_hi="और एक और मज़ेदार बात — octopus का खून नीला होता है!", bo="Bonus: khoon NEELA hota hai!"),
    dict(q="human brain illustration", stmt="Hum dimaag ka sirf 10% istemal karte hain!", fact=False,
         stmt_hi="हम दिमाग़ का सिर्फ़ दस percent इस्तेमाल करते हैं!", title="Dimaag ka 10%? FACT ya MYTH",
         ex_hi="झूठ! Brain scan से पता चला है — हम पूरे दिमाग़ का इस्तेमाल करते हैं, सोते समय भी।",
         ex1="Brain scan: pura dimaag active", ex2="10% wali baat galatfehmi hai",
         bo_hi="यह 10 percent वाली बात, एक बहुत पुरानी ग़लतफ़हमी है!", bo="Bonus: ye 100 saal purani galatfehmi hai!"),
    dict(q="honey jar", stmt="Shehad (Honey) kabhi kharab nahi hota!", fact=True,
         stmt_hi="शहद कभी ख़राब नहीं होता!", title="Shehad kabhi kharab nahi hota? FACT ya MYTH",
         ex_hi="सच! शहद में नमी कम और acid ज़्यादा होता है — bacteria जी ही नहीं सकते। तीन हज़ार साल पुराना शहद भी खाने लायक़ मिला है!",
         ex1="Nami kam + acid zyada", ex2="Bacteria jee nahi sakte",
         bo_hi="मिस्र की पुरानी क़ब्रों में मिला शहद, आज भी मीठा है!", bo="Bonus: 3000 saal purana shehad bhi fresh!"),
    dict(q="goldfish aquarium", stmt="Goldfish ki yaaddasht sirf 3 second hoti hai!", fact=False,
         stmt_hi="Goldfish की याददाश्त सिर्फ़ तीन second होती है!", title="Goldfish ki 3 second yaad? FACT ya MYTH",
         ex_hi="झूठ! Goldfish को चीज़ें महीनों तक याद रहती हैं। उसे घंटी बजाकर खाना खाना भी सिखाया जा सकता है।",
         ex1="Yaad: mahino tak rehti hai", ex2="Seekhne ki shakti bhi hai",
         bo_hi="Goldfish अपने मालिक को पहचान भी सकती है!", bo="Bonus: goldfish malik ko pehchanti hai!"),
    dict(q="lightning storm sky", stmt="Bijli suraj se 5 guna zyada garam hoti hai!", fact=True,
         stmt_hi="बिजली, सूरज से पाँच गुना ज़्यादा गरम होती है!", title="Bijli suraj se garam? FACT ya MYTH",
         ex_hi="सच! बिजली गिरते समय हवा तीस हज़ार degree तक गरम हो जाती है — सूरज की सतह से लगभग पाँच गुना!",
         ex1="Hawa: 30,000 degree tak", ex2="Suraj ki satah se 5 guna",
         bo_hi="बिजली एक second से भी कम समय में गिरती है!", bo="Bonus: bijli palak jhapakte girti hai!"),
    dict(q="banana fruit", stmt="Kele aur insaan ka 60% DNA ek jaisa hota hai!", fact=True,
         stmt_hi="केले और इंसान का साठ percent DNA एक जैसा होता है!", title="Kela = 60% Insaan? FACT ya MYTH",
         ex_hi="सच! इंसान और केले के लगभग साठ percent genes एक जैसे हैं। इसीलिए वैज्ञानिक केले पर भी research करते हैं।",
         ex1="60% genes ek jaise", ex2="Vigyaan ke liye upyogi",
         bo_hi="हम एक केले से आधे से ज़्यादा genes साझा करते हैं!", bo="Bonus: hum aadhe se zyada 'kela' hain!"),
    dict(q="moon surface astronaut footprint", stmt="Chaand par pairon ke nishan hamesha rahenge!", fact=True,
         stmt_hi="चाँद पर पैरों के निशान हमेशा रहेंगे!", title="Chaand ke nishan hamesha? FACT ya MYTH",
         ex_hi="सच! चाँद पर न हवा है न पानी — इसीलिए 1969 के पैरों के निशान आज भी वैसे के वैसे हैं।",
         ex1="Na hawa, na paani", ex2="1969 ke nishan aaj bhi hain",
         bo_hi="वह निशान लाखों साल तक रह सकते हैं!", bo="Bonus: nishan lakhon saal rahenge!"),
    dict(q="blue whale ocean", stmt="Blue Whale duniya ka sabse bada janwar hai!", fact=True,
         stmt_hi="Blue Whale दुनिया का सबसे बड़ा जानवर है!", title="Sabse bada janwar? FACT ya MYTH",
         ex_hi="सच! इसका दिल एक छोटी car जितना बड़ा होता है, और जीभ एक हाथी जितनी भारी!",
         ex1="Dil: chhoti car jitna bada", ex2="Jeebh: haathi jitni bhaari",
         bo_hi="Blue Whale की आवाज़, सैकड़ों kilometre दूर तक जाती है!", bo="Bonus: awaaz 100s km door tak!"),
    dict(q="human skeleton bones", stmt="Insaan ki haddi steel se zyada mazboot hoti hai!", fact=True,
         stmt_hi="इंसान की हड्डी, steel से ज़्यादा मज़बूत होती है!", title="Haddi steel se mazboot? FACT ya MYTH",
         ex_hi="सच! वज़न के हिसाब से हड्डी, steel से लगभग पाँच गुना ज़्यादा मज़बूत होती है।",
         ex1="Wazan ke hisaab se 5 guna", ex2="Halki, par zabardast mazboot",
         bo_hi="हड्डी टूटकर ख़ुद जुड़ भी जाती है — steel नहीं जुड़ता!", bo="Bonus: haddi khud theek ho jati hai!"),
    dict(q="ocean underwater waves", stmt="Paani mein awaaz hawa se tez chalti hai!", fact=True,
         stmt_hi="पानी में आवाज़, हवा से तेज़ चलती है!", title="Paani mein awaaz tez? FACT ya MYTH",
         ex_hi="सच! पानी में आवाज़ लगभग चार गुना तेज़ — चौदह सौ अस्सी metre per second चलती है।",
         ex1="Paani: 1480 m/s", ex2="Hawa se lagbhag 4 guna tez",
         bo_hi="इसीलिए whale की आवाज़, समुद्र में दूर-दूर तक जाती है!", bo="Bonus: whale ki awaaz samundar paar!"),
    dict(q="peacock feathers", stmt="Mor (Peacock) bilkul udd nahi sakta!", fact=False,
         stmt_hi="मोर बिल्कुल उड़ नहीं सकता!", title="Mor nahi udd sakta? FACT ya MYTH",
         ex_hi="झूठ! मोर छोटी दूरी तक उड़ सकता है — पेड़ पर चढ़ने के लिए वह उड़ता ही है।",
         ex1="Chhoti doori tak udta hai", ex2="Ped par uddkar chadhta hai",
         bo_hi="मोर के pankh, डेढ़ metre तक लंबे हो सकते हैं!", bo="Bonus: pankh 1.5 metre lambe!"),
    dict(q="human breathing lungs", stmt="Hum ek din mein 20,000 baar saans lete hain!", fact=True,
         stmt_hi="हम एक दिन में बीस हज़ार बार साँस लेते हैं!", title="Din mein 20,000 saans? FACT ya MYTH",
         ex_hi="सच! एक वयस्क इंसान, एक दिन में लगभग बीस हज़ार बार साँस लेता है — बिना सोचे, अपने आप!",
         ex1="Har din ~20,000 saans", ex2="Bina soche, apne aap",
         bo_hi="ज़िंदगी भर में हम, करोड़ों बार साँस लेते हैं!", bo="Bonus: zindagi mein karodon saans!"),
]

def pick_fact():
    idx = os.environ.get("FACT_INDEX", "").strip()
    if idx.isdigit():
        return int(idx) % len(FACTS), FACTS[int(idx) % len(FACTS)]
    i = datetime.date.today().toordinal() % len(FACTS)
    return i, FACTS[i]

def fetch_image(query):
    try:
        r = requests.get("https://api.openverse.org/v1/images/",
                         params={"q": query, "page_size": 5}, timeout=25,
                         headers={"User-Agent": "EducationalBroBot/1.0"})
        for it in r.json().get("results", []):
            url = it.get("url")
            if not url:
                continue
            d = requests.get(url, timeout=25, headers={"User-Agent": "EducationalBroBot/1.0"})
            if d.status_code == 200 and len(d.content) > 20000:
                p = os.path.join(TMP, "img.jpg")
                open(p, "wb").write(d.content)
                Image.open(p).convert("RGB").save(p)
                print("image:", url[:90])
                return p
    except Exception as e:
        print("image fetch failed:", e)
    # fallback art: deep-sea gradient
    im = Image.new("RGB", (1000, 1000), (16, 42, 86))
    d = ImageDraw.Draw(im, "RGBA")
    for k in range(60):
        x, y = np.random.randint(0, 1000, 2); r_ = np.random.randint(6, 26)
        d.ellipse([x - r_, y - r_, x + r_, y + r_], fill=(120, 200, 255, 60))
    p = os.path.join(TMP, "img.jpg"); im.save(p)
    return p

FB = "/usr/share/fonts/truetype/DejaVu/DejaVuSans-Bold.ttf"
FN2 = "/usr/share/fonts/truetype/DejaVu/DejaVuSans.ttf"
_FC = {}
def font(bold, size):
    path = FB if bold and os.path.exists(FB) else (FN2 if os.path.exists(FN2) else FB)
    k = (path, size)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(path, size) if os.path.exists(path) else ImageFont.load_default()
    return _FC[k]

def seg(p, a, b): return max(0.0, min(1.0, (p - a) / (b - a))) if b > a else (1.0 if p >= b else 0.0)

def dur(path):
    try:
        out = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True).stdout.strip()
        return float(out)
    except Exception:
        return 4.0

async def _tts(text, out):
    import edge_tts
    await edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="-4%").save(out)

def synth(text, name):
    out = os.path.join(TMP, name)
    try:
        asyncio.run(_tts(text, out))
        if os.path.getsize(out) < 3000: raise RuntimeError("tiny")
    except Exception as e:
        print("edge-tts failed, gTTS fallback:", e)
        from gtts import gTTS
        gTTS(text=text, lang="hi", slow=False).save(out)
    return out

def make_frames(fact, img_path, durs):
    photo = Image.open(img_path).convert("RGB")
    def bg(zoom):
        s = max(W / photo.width, H / photo.height) * zoom
        r = photo.resize((int(photo.width * s) + 2, int(photo.height * s) + 2))
        x, y = (r.width - W) // 2, (r.height - H) // 2
        r = r.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(26))
        return Image.blend(r, Image.new("RGB", (W, H), (8, 10, 18)), 0.45)
    def cardp(zoom):
        cw, ch = 920, 700
        s = max(cw / photo.width, ch / photo.height) * zoom
        r = photo.resize((int(photo.width * s) + 2, int(photo.height * s) + 2))
        x, y = (r.width - cw) // 2, (r.height - ch) // 2
        r = r.crop((x, y, x + cw, y + ch))
        m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw, ch], 36, fill=255)
        return r, m
    def tc(d, text, cx, y, fnt, fill):
        d.text((cx, y), text, font=fnt, fill=fill, anchor="ma", stroke_width=0)
    def heart(d, cx, cy, s, col):
        d.ellipse([cx - s, cy - s, cx, cy], fill=col); d.ellipse([cx, cy - s, cx + s, cy], fill=col)
        d.polygon([(cx - s, cy - s // 3), (cx + s, cy - s // 3), (cx, cy + int(s * 1.2))], fill=col)
    caps = ["Fact ya Myth? " + fact["stmt"], ("FACT! " if fact["fact"] else "MYTH! ") + fact["ex1"],
            "Bonus: " + fact["bo"]]
    stamp_txt = "FACT ✓" if fact["fact"] else "MYTH ✗"
    stamp_col = (60, 220, 90) if fact["fact"] else (240, 90, 80)
    def frame(bi, p, tsec):
        tp = (bi + p) / 3.0
        img = bg(1.0 + 0.07 * tp)
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([0, 0, int(W * tp), 10], fill=(255, 209, 102, 255))
        bw, bh = 560, 104
        d.rounded_rectangle([(W - bw) // 2, 70, (W + bw) // 2, 70 + bh], 52, fill=(255, 190, 40, 255))
        tc(d, "FACT ya MYTH?", W // 2, 88, font(True, 58), (20, 20, 30))
        cp, mask = cardp(1.0 + 0.05 * tp)
        img.paste(cp, (80, 250), mask)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([80, 250, 1000, 950], 36, outline=(255, 255, 255, 200), width=4)
        d.rounded_rectangle([60, 1010, 1020, 1230], 28, fill=(8, 12, 22, 205))
        tc(d, fact["stmt"], W // 2, 1065, font(True, 52), (255, 209, 102))
        if bi == 0:
            tc(d, "Kya yeh sach hai? SOCHO...", W // 2, 1290, font(True, 46), (180, 220, 255))
            cw_ = int(760 * max(0.0, 1 - seg(p, 0.35, 0.97)))
            d.rounded_rectangle([160, 1400, 920, 1448], 24, outline=(255, 255, 255, 160), width=3)
            if cw_ > 8: d.rounded_rectangle([160, 1400, 160 + cw_, 1448], 24, fill=(255, 120, 90, 255))
            for i, (t_, col) in enumerate([("FACT ?", (46, 140, 70)), ("MYTH ?", (170, 60, 50))]):
                x = 290 + i * 500
                d.rounded_rectangle([x - 100, 1478, x + 100, 1562], 20, fill=col + (255,))
                tc(d, t_, x, 1496, font(True, 44), (255, 255, 255))
        elif bi == 1:
            q = seg(p, 0.05, 0.3)
            if q > 0:
                sc = (2.2 - 1.2 * q) * 0.9
                st = Image.new("RGBA", (720, 300), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
                sd.rounded_rectangle([10, 60, 710, 240], 24, outline=stamp_col + (255,), width=14)
                sd.text((360, 150), stamp_txt, font=font(True, 104), fill=stamp_col + (255,), anchor="mm")
                st = st.rotate(14, expand=True, resample=Image.BICUBIC)
                st = st.resize((int(st.width * sc), int(st.height * sc)), Image.LANCZOS)
                img.paste(st, (W // 2 - st.width // 2, 560 - st.height // 2), st)
                d = ImageDraw.Draw(img, "RGBA")
            if p > 0.35:
                if fact["fact"]:
                    for i in range(3): heart(d, 380 + i * 160, 1330, 44, (240, 80, 90, 255))
                tc(d, fact["ex1"], W // 2, 1420, font(True, 48), (255, 255, 255))
                tc(d, fact["ex2"], W // 2, 1490, font(True, 48), (160, 230, 190))
        else:
            tc(d, "BONUS FACT!", W // 2, 1300, font(True, 52), (120, 200, 255))
            tc(d, fact["bo"], W // 2, 1390, font(True, 48), (255, 255, 255))
            if p > 0.4:
                d.rounded_rectangle([110, 1590, 970, 1700], 55, fill=(255, 190, 40, 255))
                tc(d, "FOLLOW: EDUCATIONAL BRO", W // 2, 1628, font(True, 40), (20, 20, 30))
        d.rounded_rectangle([40, 1760, 1040, 1860], 18, fill=(0, 0, 0, 170))
        tc(d, caps[bi], W // 2, 1790, font(True, 38), (255, 255, 255))
        return img
    return frame

def main():
    idx, fact = pick_fact()
    print(f"FACT[{idx}]:", fact["stmt"])
    img = fetch_image(fact["q"])
    lines = [
        f"Fact, ya Myth? {fact['stmt_hi']} Kya yeh sach hai? Jaldi socho...",
        f"Jawab hai... {'FACT!' if fact['fact'] else 'MYTH!'} {fact['ex_hi']}",
        f"{fact['bo_hi']} Aise hi Fact ya Myth ke liye, follow karo... Educational bro!",
    ]
    clips = [synth(t, f"c{i}.mp3") for i, t in enumerate(lines)]
    durs = [dur(c) for c in clips]
    print("voice durations:", [round(x, 1) for x in durs])
    frame = make_frames(fact, img, durs)
    aud = os.path.join(TMP, "a.m4a"); lst = os.path.join(TMP, "list.txt")
    with open(lst, "w") as fh:
        for c in clips: fh.write(f"file '{c}'\n")
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", "apad=pad_dur=2", "-c:a", "aac", "-b:a", "160k", aud], check=True)
    out = os.path.join(BASE, "output", f"short_factmyth_{idx:02d}.mp4")
    cmd = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", aud, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", os.path.join(TMP, "v.mp4")]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    fi = 0
    for bi, ds in enumerate(durs):
        nf = int((ds + 0.35) * FPS)
        for k in range(nf):
            proc.stdin.write(np.asarray(frame(bi, k / max(1, nf - 1), fi / FPS), dtype=np.uint8).tobytes())
            fi += 1
        if bi == 1:
            frame(bi, 0.7, 0).save(os.path.join(TMP, "thumb.jpg"), quality=88)
    proc.stdin.close(); proc.wait()
    shutil.move(os.path.join(TMP, "v.mp4"), out)
    print("VIDEO:", out, f"{os.path.getsize(out)/1e6:.1f} MB", f"{dur(out):.1f}s")
    if "--upload" in sys.argv:
        sys.path.insert(0, BASE)
        from youtube_uploader import upload_to_youtube
        plan = {
            "title": f"{fact['title']} 😱 #fact #myth",
            "description": f"{fact['stmt']}\n\nJawab: {'FACT ✅' if fact['fact'] else 'MYTH ❌'}\n{fact['ex1']} | {fact['ex2']}\n\nRoz ek naya Fact ya Myth — Educational bro ko follow karo!\n#shorts #facts #myth #hindi #science",
            "tags": ["fact or myth", "hindi facts", "science facts hindi", "myth vs fact", "educational bro", "shorts"],
        }
        vid = upload_to_youtube(out, os.path.join(TMP, "thumb.jpg"), plan, "shorts")
        print("YOUTUBE_VIDEO_ID:", vid)
        print("YOUTUBE_URL: https://youtube.com/watch?v=" + str(vid))

if __name__ == "__main__":
    main()
