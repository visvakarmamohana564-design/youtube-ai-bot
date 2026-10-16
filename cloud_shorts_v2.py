#!/usr/bin/env python3
"""CLOUD AUTO v2 — 5 Shorts Models (GitHub Actions), ek script, 5 dimaag.
Har model: apna bank -> khud topic chune -> real photo (Openverse) -> Hindi awaaz
(edge-tts MadhurNeural, fallback gTTS) -> alag 9:16 design -> YouTube upload (#shorts).
Usage:
  python cloud_shorts_v2.py --type fact     [--upload] [--index N]
  python cloud_shorts_v2.py --type quiz     [--upload] [--index N]
  python cloud_shorts_v2.py --type story    [--upload] [--index N]
  python cloud_shorts_v2.py --type factmyth [--upload] [--index N]
  python cloud_shorts_v2.py --type top5     [--upload] [--index N]
Index na do to roz date ke hisaab se khud rotate hota hai."""
import os, sys, subprocess, shutil, asyncio, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests

W, H, FPS = 1080, 1920, 30
FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe")
BASE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(BASE, "output"), exist_ok=True)

# ============================ CONTENT BANKS ============================
FACTS = [  # Model 1: Science Facts (did-you-know + kyun hota hai)
 dict(q="honey jar", img=None,
   hook="Kya tum jaante ho?", big="SHEHAD kabhi KHARAB nahi hota!", title="Shehad Kabhi Kharab Kyun Nahi Hota?",
   vo=["क्या तुम जानते हो? शहद कभी ख़राब नहीं होता!",
       "क्योंकि शहद में पानी बहुत कम, और acid ज़्यादा होता है। bacteria इसमें जी ही नहीं सकते।",
       "मिस्र की हज़ारों साल पुरानी क़ब्रों में मिला शहद, आज भी खाने लायक़ है! ऐसे ही science facts के लिए follow करो!"],
   pts=["Nami kam + acid zyada", "Bacteria jee hi nahi sakte", "3000 saal purana shehad bhi fresh!"]),
 dict(q="blue whale ocean",
   hook="Samundar ka sabse bada sach!", big="BLUE WHALE ka dil = ek CAR jitna!", title="Blue Whale ka Dil Car Jitna Bada?",
   vo=["दुनिया के सबसे बड़े जानवर, Blue Whale, का दिल... एक छोटी car जितना बड़ा होता है!",
       "और उसकी जीभ, एक पूरे हाथी जितनी भारी होती है!",
       "Blue Whale की आवाज़ सैकड़ों kilometre दूर तक सुनाई देती है। Amazing hai na? Follow karo aur facts seekho!"],
   pts=["Dil = chhoti car jitna bada", "Jeebh = ek haathi jitni bhaari", "Awaaz 100s km door tak jati hai"]),
 dict(q="moon surface astronaut footprint",
   hook="Chaand ka ek raaz!", big="1969 ke pairon ke nishan AAJ BHI hain!", title="Chaand Par Nishan Hamesha Kyun Rehte Hain?",
   vo=["चाँद पर 1969 में बने पैरों के निशान, आज भी वैसे के वैसे हैं!",
       "क्योंकि चाँद पर न हवा है, न पानी — मिटाने वाला कोई है ही नहीं।",
       "वे निशान लाखों साल तक रह सकते हैं! Space ke aise facts ke liye follow karo!"],
   pts=["Na hawa hai, na paani", "Mitane wala koi nahi", "Nishan lakhon saal rahenge"]),
 dict(q="lightning storm sky",
   hook="Bijli ka garam sach!", big="BIJLI, suraj se 5 GUNA garam!", title="Bijli Suraj Se Zyada Garam?",
   vo=["आसमान की बिजली, सूरज की सतह से पाँच गुना ज़्यादा गरम होती है!",
       "बिजली गिरते समय हवा तीस हज़ार degree तक गरम हो जाती है।",
       "और ये सब, एक second से भी कम समय में हो जाता है! Science facts ke liye follow karo!"],
   pts=["Hawa: 30,000 degree tak", "Suraj ki satah se 5 guna", "1 second se bhi kam samay"]),
 dict(q="octopus underwater",
   hook="8 tangon wala ajooba!", big="OCTOPUS ke 3 DIL hote hain!", title="Octopus Ke 3 Dil Hote Hain?",
   vo=["Octopus के एक नहीं, पूरे तीन दिल होते हैं!",
       "दो दिल gills को ख़ून भेजते हैं, और एक दिल पूरे शरीर को।",
       "और सुनो — octopus का ख़ून नीला होता है! Aise facts ke liye follow karo!"],
   pts=["2 dil → gills ko khoon", "1 dil → pure shareer ko", "Bonus: khoon NEELA hota hai!"]),
 dict(q="human skeleton bones",
   hook="Tumhari haddi ka sach!", big="HADDI, steel se 5 GUNA mazboot!", title="Haddi Steel Se Mazboot Hoti Hai?",
   vo=["तुम्हारी हड्डी, वज़न के हिसाब से steel से पाँच गुना ज़्यादा मज़बूत होती है!",
       "हलकी होने के बाद भी, हड्डी भारी दबाव झेल लेती है।",
       "और टूट जाए तो ख़ुद जुड़ भी जाती है — steel कभी नहीं जुड़ता! Follow karo!"],
   pts=["Wazan ke hisaab se 5 guna", "Halki par zabardast mazboot", "Toote to khud jud jati hai"]),
]

QUIZ = [  # Model 2: Quiz / GK (sawal -> 5-4-3-2-1 -> jawab + ek line kyun)
 dict(q="hummingbird flying",
   hook="Quiz Time!", qst="Duniya ka sabse CHHOTA pakshi kaunsa hai?", title="Sabse Chhota Pakshi? Quiz",
   opts=["A. Gauraiya (Sparrow)", "B. Hummingbird", "C. Kingfisher", "D. Bulbul"], ans=1, ans_txt="B. Hummingbird",
   vo=["Quiz time! दुनिया का सबसे छोटा पक्षी कौन सा है? A: गौरैया। B: Hummingbird। C: Kingfisher। D: Bulbul। सोचो... पाँच, चार, तीन, दो, एक!",
       "सही जवाब है — B, Hummingbird! यह इकलौता पक्षी है जो पीछे की ओर भी उड़ सकता है।",
       "तुम्हारा जवाब सही था? Comment में बताओ! Roz quiz ke liye follow karo!"],
   why="Peeche udne wala iklauta pakshi!"),
 dict(q="giraffe savanna",
   hook="Quiz Time!", qst="Sabse LAMBI gardan wala janwar kaunsa hai?", title="Sabse Lambi Gardan? Quiz",
   opts=["A. Haathi", "B. Oont (Camel)", "C. Giraffe", "D. Zebra"], ans=2, ans_txt="C. Giraffe",
   vo=["Quiz time! सबसे लंबी गर्दन वाला जानवर कौन सा है? A: हाथी। B: ऊँट। C: Giraffe। D: Zebra। सोचो... पाँच, चार, तीन, दो, एक!",
       "सही जवाब है — C, Giraffe! इसकी गर्दन ढाई metre तक लंबी होती है।",
       "Score kitna raha? Comment karo! Roz ek naya quiz — follow karo!"],
   why="Gardan 2.5 metre tak lambi!"),
 dict(q="great wall of china",
   hook="Quiz Time!", qst="Duniya ki sabse LAMBI deewar kaunsi hai?", title="Sabse Lambi Deewar? Quiz",
   opts=["A. Great Wall of China", "B. Berlin Wall", "C. Hadrian Wall", "D. Kumbhalgarh Wall"], ans=0, ans_txt="A. Great Wall of China",
   vo=["Quiz time! दुनिया की सबसे लंबी दीवार कौन सी है? A: Great Wall of China। B: Berlin Wall। C: Hadrian Wall। D: Kumbhalgarh Wall। सोचो... पाँच, चार, तीन, दो, एक!",
       "सही जवाब है — A, Great Wall of China! यह इक्कीस हज़ार kilometre से भी लंबी है।",
       "Sahi jawab diya tha? Comment mein A, B, C ya D likho! Follow karo!"],
   why="21,000 km se bhi zyada lambi!"),
 dict(q="honey bee flower",
   hook="Quiz Time!", qst="Ek madhumakkhi kitne pankh phadphadati hai (1 sec)?", title="Madhumakkhi Quiz",
   opts=["A. 20 baar", "B. 200 baar", "C. 2000 baar", "D. 2 baar"], ans=1, ans_txt="B. 200 baar",
   vo=["Quiz time! एक मधुमक्खी एक second में अपने पंख कितनी बार फड़फड़ाती है? A: बीस बार। B: दो सौ बार। C: दो हज़ार बार। D: दो बार। सोचो... पाँच, चार, तीन, दो, एक!",
       "सही जवाब है — B, दो सौ बार हर second! इसीलिए उसकी भिनभिनाहट इतनी तेज़ सुनाई देती है।",
       "Tum kitne sahi jawab de sakte ho? Roz quiz ke liye follow karo!"],
   why="200 baar/second = mashhoor bhinbhin!"),
]

STORY = [  # Model 3: Kids Story (character: Chintu khargosh; moral end me)
 dict(q="rabbit forest",
   hook="Ek chhota sa khargosh tha...", title="Chintu Khargosh Aur Jadui Gajar",
   parts=[("ek", "CHINTU KHARGOSH", "Ek tha Chintu khargosh — bahut tez daudta tha, par sabse peeche reh jata tha, kyunki woh rukta hi nahi tha!"),
          ("do", "JADUI GAJAR", "Ek din use ek chamakti hui JADUI GAJAR mili. Jo bhi use khaye, woh sabse tez ban jaye!"),
          ("teen", "ASLI JEET", "Par Chintu ne gajar apne bhooke dost Kachhue ko de di. Dost khush — aur wahi Chintu ki ASLI JEET thi!")],
   vo=["एक था Chintu खरगोश — बहुत तेज़ दौड़ता था, पर हमेशा पीछे रह जाता था, क्योंकि वह रुकता ही नहीं था!",
       "एक दिन उसे एक चमकती हुई जादुई गाजर मिली। जो भी उसे खाए, वह सबसे तेज़ बन जाए!",
       "पर Chintu ने गाजर अपने भूखे दोस्त कछुए को दे दी। दोस्त ख़ुश — और वही Chintu की असली जीत थी!"],
   moral="Seekh: Dost ki madad hi ASLI JEET hai!"),
 dict(q="little bird nest tree",
   hook="Chhoti si chidiya ki kahani", title="Chhoti Chidiya Ki Badi Udaan",
   parts=[("ek", "DARRI HUI CHIDIYA", "Pihu chidiya udne se bahut darti thi. Neeche dekhte hi uske pankh kaanp jate the!"),
          ("do", "TOOFAN KI RAAT", "Ek toofani raat, uska ghonsla hilne laga. Chhote bhai ko bachane ke liye, Pihu ko udna hi tha!"),
          ("teen", "PEHLI UDAAN", "Pihu ne aankhein band ki, pankh phailaye... aur woh UD GAYI! Dar ko hara kar hi hum aage badhte hain!")],
   vo=["Pihu चिड़िया उड़ने से बहुत डरती थी। नीचे देखते ही उसके पंख काँप जाते थे!",
       "एक तूफ़ानी रात, उसका घोंसला हिलने लगा। छोटे भाई को बचाने के लिए, Pihu को उड़ना ही था!",
       "Pihu ने आँखें बंद कीं, पंख फैलाए... और वह उड़ गई! डर को हराकर ही हम आगे बढ़ते हैं!"],
   moral="Seekh: Dar ko harao, UDAAN apne aap milegi!"),
 dict(q="elephant jungle",
   hook="Hathi aur chhoti chinti", title="Golu Hathi Aur Chhoti Chinti",
   parts=[("ek", "GOLU KA GHAMAND", "Golu hathi sabse bada tha, aur sabse zyada ghamand bhi use hi tha. Chhoti chinti ko woh dekh ta tak nahi tha!"),
          ("do", "MUSIBAT KA DIN", "Ek din Golu ke paon mein bada sa kaanta chubh gaya. Bada hathi, chhote kaante se haar gaya!"),
          ("teen", "CHINTI KI MADAD", "Wahi chhoti chinti aayi, kaanta nikala — aur dono dost ban gaye. Bada woh nahi jo bada hai, bada woh jo kaam aaye!")],
   vo=["Golu हाथी सबसे बड़ा था, और सबसे ज़्यादा घमंड भी उसे ही था। छोटी चींटी को वह देखता तक नहीं था!",
       "एक दिन Golu के पाँव में बड़ा सा काँटा चुभ गया। बड़ा हाथी, छोटे काँटे से हार गया!",
       "वही छोटी चींटी आई, काँटा निकाला — और दोनों दोस्त बन गए! बड़ा वह नहीं जो बड़ा है, बड़ा वह जो काम आए!"],
   moral="Seekh: Chhota ho ya bada, SAB kaam ke hote hain!"),
]

FACTMYTH = [  # Model 4: Fact or Myth (proved format v1 se)
 dict(q="goldfish aquarium", stmt="Goldfish ki yaad sirf 3 SECOND hoti hai!", fact=False,
   stmt_hi="Goldfish की याददाश्त सिर्फ़ तीन second होती है!", title="Goldfish ki 3 Second Yaad? FACT ya MYTH",
   vo=["Fact, ya Myth? Goldfish की याददाश्त सिर्फ़ तीन second होती है! क्या यह सच है? जल्दी सोचो...",
       "जवाब है... MYTH! Goldfish को चीज़ें महीनों तक याद रहती हैं। उसे घंटी बजाकर खाना खाना भी सिखाया जा सकता है।",
       "और सुनो — Goldfish अपने मालिक को पहचान भी सकती है! Aise hi Fact ya Myth ke liye follow karo, Educational bro!"],
   ex=["Yaad: mahino tak rehti hai", "Seekhne ki shakti bhi hai"], bo="Bonus: goldfish malik ko pehchanti hai!"),
 dict(q="banana fruit", stmt="Kele aur insaan ka 60% DNA ek jaisa!", fact=True,
   stmt_hi="केले और इंसान का साठ percent DNA एक जैसा होता है!", title="Kela = 60% Insaan? FACT ya MYTH",
   vo=["Fact, ya Myth? केले और इंसान का साठ percent DNA एक जैसा होता है! सोचो, सच होगा या झूठ...",
       "जवाब है... FACT! इंसान और केले के लगभग साठ percent genes एक जैसे हैं। इसीलिए वैज्ञानिक केले पर भी research करते हैं।",
       "मतलब हम, आधे से ज़्यादा, एक केले जैसे हैं! Pasand aaya? Follow karo, Educational bro!"],
   ex=["60% genes ek jaise", "Vigyaan ke liye upyogi"], bo="Bonus: hum aadhe se zyada 'kela' hain!"),
 dict(q="peacock feathers", stmt="Mor (Peacock) bilkul UDD nahi sakta!", fact=False,
   stmt_hi="मोर बिल्कुल उड़ नहीं सकता!", title="Mor Nahi Udd Sakta? FACT ya MYTH",
   vo=["Fact, ya Myth? मोर बिल्कुल उड़ नहीं सकता! क्या यह सच है? जल्दी सोचो...",
       "जवाब है... MYTH! मोर छोटी दूरी तक उड़ सकता है — पेड़ पर चढ़ने के लिए वह उड़ता ही है।",
       "और सुनो — मोर के पंख डेढ़ metre तक लंबे हो सकते हैं! Aise Fact ya Myth roz — follow karo!"],
   ex=["Chhoti doori tak udta hai", "Ped par uddkar chadhta hai"], bo="Bonus: pankh 1.5 metre lambe!"),
 dict(q="ocean underwater waves", stmt="Paani mein awaaz HAWA se TEZ chalti hai!", fact=True,
   stmt_hi="पानी में आवाज़, हवा से तेज़ चलती है!", title="Paani Mein Awaaz Tez? FACT ya MYTH",
   vo=["Fact, ya Myth? पानी में आवाज़, हवा से तेज़ चलती है! सोचो, सोचो...",
       "जवाब है... FACT! पानी में आवाज़ लगभग चार गुना तेज़ — चौदह सौ अस्सी metre per second चलती है।",
       "इसीलिए whale की आवाज़ समुद्र में दूर-दूर तक जाती है! Aur facts ke liye follow karo!"],
   ex=["Paani: 1480 m/s", "Hawa se lagbhag 4 guna tez"], bo="Bonus: whale ki awaaz samundar paar!"),
]

TOP5 = [  # Model 5: Top-5 Comparison (countdown 5->1)
 dict(q="largest planet solar system", title="Top 5 Sabse Bade Grah (Planets)",
   vo=["Top five! हमारे solar system के पाँच सबसे बड़े ग्रह, गिनती शुरू — नंबर पाँच!",
       "नंबर पाँच: Neptune। नंबर चार: Uranus। नंबर तीन: Saturn — अपनी ring के लिए मशहूर!",
       "नंबर दो: ...और नंबर एक, सबसे बड़ा: Jupiter! इसमें तेरह सौ पृथ्वी समा सकती हैं! कौन सा ग्रह तुम्हारा favourite है? Comment karo, aur follow karo!"],
   items=["5. Neptune — sabse thanda", "4. Uranus — tedha ghumta hai", "3. Saturn — ring wala raja", "2. — suspense...", "1. JUPITER — 1300 Earth samayein!"]),
 dict(q="fastest animals cheetah",
   title="Top 5 Sabse Tez Janwar",
   vo=["Top five! दुनिया के पाँच सबसे तेज़ जानवर — नंबर पाँच से शुरू!",
       "नंबर पाँच: Khargosh। नंबर चार: Hiran। नंबर तीन: Ghoda — साठ kilometre प्रति घंटा!",
       "नंबर दो: ...और नंबर एक: Cheetah! सौ kilometre प्रति घंटा — car से भी तेज़! Tumhara favourite kaunsa hai? Comment karo, follow karo!"],
   items=["5. Khargosh — chhota par tez", "4. Hiran — jungle ka racer", "3. Ghoda — 60 km/h", "2. — suspense...", "1. CHEETAH — 100 km/h!"]),
 dict(q="tallest mountains Himalaya",
   title="Top 5 Sabse Unchi Chotiyan",
   vo=["Top five! दुनिया की पाँच सबसे ऊँची चोटियाँ — नंबर पाँच से शुरू करते हैं!",
       "नंबर पाँच: Makalu। नंबर चार: Lhotse। नंबर तीन: Kangchenjunga — भारत की सबसे ऊँची!",
       "नंबर दो: K2... और नंबर एक: Mount Everest — आठ हज़ार आठ सौ अड़तालीस metre! Kya tum kabhi pahad chadhe ho? Comment karo, follow karo!"],
   items=["5. Makalu — 8,485 m", "4. Lhotse — 8,516 m", "3. Kangchenjunga — Bharat ki shaan", "2. K2 — sabse khatarnak", "1. EVEREST — 8,848 m!"]),
]

BANKS = {"fact": ("MODEL1", FACTS, (255, 190, 40)),
         "quiz": ("MODEL2", QUIZ, (120, 200, 255)),
         "story": ("MODEL3", STORY, (140, 230, 150)),
         "factmyth": ("MODEL4", FACTMYTH, (255, 150, 90)),
         "top5": ("MODEL5", TOP5, (220, 160, 255))}

# ============================ HELPERS ============================
TMP = "/tmp/shortsv2"
os.makedirs(TMP, exist_ok=True)
FB = "/usr/share/fonts/truetype/DejaVu/DejaVuSans-Bold.ttf"
FN2 = "/usr/share/fonts/truetype/DejaVu/DejaVuSans.ttf"
_FC = {}
def font(bold, size):
    path = FB if bold else FN2
    if not os.path.exists(path): path = FB if os.path.exists(FB) else FN2
    k = (path, size)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(path, size) if os.path.exists(path) else ImageFont.load_default()
    return _FC[k]

def seg(p, a, b): return max(0.0, min(1.0, (p - a) / (b - a))) if b > a else (1.0 if p >= b else 0.0)

def tc(d, text, cx, y, fnt, fill):
    d.text((cx, y), text, font=fnt, fill=fill, anchor="ma")

def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t_ = (cur + " " + wd).strip()
        if d.textlength(t_, font=fnt) <= maxw: cur = t_
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines[:3]

def dur(path):
    try:
        return float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip())
    except Exception:
        return 5.0

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

def fetch_image(query):
    try:
        r = requests.get("https://api.openverse.org/v1/images/",
                         params={"q": query, "page_size": 5}, timeout=25,
                         headers={"User-Agent": "EducationalBroBot/2.0"})
        for it in r.json().get("results", []):
            url = it.get("url")
            if not url: continue
            d = requests.get(url, timeout=25, headers={"User-Agent": "EducationalBroBot/2.0"})
            if d.status_code == 200 and len(d.content) > 20000:
                p = os.path.join(TMP, "img.jpg")
                open(p, "wb").write(d.content)
                Image.open(p).convert("RGB").save(p)
                print("image:", url[:90])
                return p
    except Exception as e:
        print("image fetch failed:", e)
    im = Image.new("RGB", (1000, 1000), (14, 30, 66))
    d = ImageDraw.Draw(im, "RGBA")
    for k in range(70):
        x, y = np.random.randint(0, 1000, 2); rr = np.random.randint(6, 26)
        d.ellipse([x-rr, y-rr, x+rr, y+rr], fill=(140, 200, 255, 70))
    p = os.path.join(TMP, "img.jpg"); im.save(p)
    return p

# ============================ FRAME ENGINE ============================
BANNERS = {"fact": "SCIENCE FACT!", "quiz": "QUIZ TIME!", "story": "KAHANI SUNO!",
           "factmyth": "FACT ya MYTH?", "top5": "TOP 5!"}

def make_frame(typ, item, photo):
    accent = BANKS[typ][2]
    def bg(zoom):
        s = max(W / photo.width, H / photo.height) * zoom
        r = photo.resize((int(photo.width * s) + 2, int(photo.height * s) + 2))
        x, y = (r.width - W) // 2, (r.height - H) // 2
        r = r.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(26))
        return Image.blend(r, Image.new("RGB", (W, H), (8, 10, 18)), 0.45)
    def card(zoom):
        cw, ch = 920, 660
        s = max(cw / photo.width, ch / photo.height) * zoom
        r = photo.resize((int(photo.width * s) + 2, int(photo.height * s) + 2))
        x, y = (r.width - cw) // 2, (r.height - ch) // 2
        r = r.crop((x, y, x + cw, y + ch))
        m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw, ch], 36, fill=255)
        return r, m
    def pill(d, cx, y, text, col, fsize=58):
        f = font(True, fsize)
        w_ = int(d.textlength(text, font=f)) + 90
        d.rounded_rectangle([cx - w_//2, y, cx + w_//2, y + 104], 52, fill=col + (255,))
        tc(d, text, cx, y + 22, f, (18, 18, 28))
        return w_
    def textbox(d, y, text, col, fsize=50):
        d.rounded_rectangle([60, y, 1020, y + 220], 28, fill=(8, 12, 22, 208))
        lines = wrap(d, text, font(True, fsize), 900)
        yy = y + (220 - len(lines) * int(fsize * 1.25)) // 2
        for ln in lines:
            tc(d, ln, W // 2, yy, font(True, fsize), col); yy += int(fsize * 1.25)
    def follow(d, p):
        if p > 0.35:
            f = font(True, 40); w_ = int(d.textlength("FOLLOW: EDUCATIONAL BRO", font=f)) + 110
            d.rounded_rectangle([(W-w_)//2, 1590, (W+w_)//2, 1700], 55, fill=(255, 190, 40, 255))
            tc(d, "FOLLOW: EDUCATIONAL BRO", W // 2, 1626, f, (18, 18, 28))
    def heart(d, cx, cy, s, col):
        d.ellipse([cx-s, cy-s, cx, cy], fill=col); d.ellipse([cx, cy-s, cx+s, cy], fill=col)
        d.polygon([(cx-s, cy-s//3), (cx+s, cy-s//3), (cx, cy + int(s*1.2))], fill=col)

    def frame(bi, p, tsec):
        tp = (bi + p) / 3.0
        img = bg(1.0 + 0.07 * tp)
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([0, 0, int(W * tp), 10], fill=(255, 209, 102, 255))
        pill(d, W // 2, 66, BANNERS[typ], accent)
        cp, mask = card(1.0 + 0.05 * tp)
        img.paste(cp, (80, 232), mask)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([80, 232, 1000, 892], 36, outline=(255, 255, 255, 200), width=4)

        if typ == "fact":
            if bi == 0:
                textbox(d, 950, item["big"], (255, 209, 102), 54)
                tc(d, item["hook"], W // 2, 1240, font(True, 46), (180, 220, 255))
            elif bi == 1:
                textbox(d, 950, item["pts"][1], (255, 255, 255), 48)
                tc(d, item["pts"][0], W // 2, 1240, font(True, 46), (160, 230, 190))
            else:
                textbox(d, 950, item["pts"][2], (120, 200, 255), 48)
                follow(d, p)
        elif typ == "quiz":
            if bi == 0:
                textbox(d, 940, item["qst"], (255, 209, 102), 46)
                for i, o in enumerate(item["opts"]):
                    y = 1200 + i * 92
                    ok = (i == item["ans"]) and p > 0.75
                    col = (60, 200, 100, 235) if ok else (30, 40, 70, 235)
                    d.rounded_rectangle([140, y, 940, y + 76], 18, fill=col)
                    tc(d, o, W // 2, y + 16, font(True, 40), (255, 255, 255))
                bw_ = int(700 * max(0.0, 1 - seg(p, 0.55, 0.98)))
                if p > 0.4:
                    d.rounded_rectangle([190, 1130, 890, 1174], 22, outline=(255, 255, 255, 150), width=3)
                    if bw_ > 8: d.rounded_rectangle([190, 1130, 190 + bw_, 1174], 22, fill=(255, 120, 90, 255))
            elif bi == 1:
                pill(d, W // 2, 980, "SAHI JAWAB ✓", (60, 220, 90), 50)
                textbox(d, 1130, item["ans_txt"], (255, 255, 255), 56)
                tc(d, item["why"], W // 2, 1420, font(True, 44), (160, 230, 190))
            else:
                textbox(d, 1000, "Tum sahi the? COMMENT karo!", (255, 209, 102), 50)
                follow(d, p)
        elif typ == "story":
            num, ttl, txt = item["parts"][bi]
            pill(d, W // 2, 940, f"BHAAG {num.upper()}: {ttl}", accent, 42)
            textbox(d, 1080, txt, (255, 255, 255), 44)
            if bi == 2:
                tc(d, item["moral"], W // 2, 1400, font(True, 46), (255, 209, 102))
                follow(d, p)
        elif typ == "factmyth":
            if bi == 0:
                textbox(d, 950, item["stmt"], (255, 209, 102), 52)
                tc(d, "Kya yeh sach hai? SOCHO...", W // 2, 1240, font(True, 46), (180, 220, 255))
                cw_ = int(760 * max(0.0, 1 - seg(p, 0.35, 0.97)))
                d.rounded_rectangle([160, 1330, 920, 1378], 24, outline=(255, 255, 255, 160), width=3)
                if cw_ > 8: d.rounded_rectangle([160, 1330, 160 + cw_, 1378], 24, fill=(255, 120, 90, 255))
                for i, (t_, col) in enumerate([("FACT ?", (46, 140, 70)), ("MYTH ?", (170, 60, 50))]):
                    x = 290 + i * 500
                    d.rounded_rectangle([x - 100, 1410, x + 100, 1494], 20, fill=col + (255,))
                    tc(d, t_, x, 1428, font(True, 44), (255, 255, 255))
            elif bi == 1:
                stamp_txt = "FACT ✓" if item["fact"] else "MYTH ✗"
                stamp_col = (60, 220, 90) if item["fact"] else (240, 90, 80)
                q = seg(p, 0.03, 0.28)
                if q > 0:
                    sc = (2.2 - 1.2 * q) * 0.9
                    st = Image.new("RGBA", (720, 300), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
                    sd.rounded_rectangle([10, 60, 710, 240], 24, outline=stamp_col + (255,), width=14)
                    sd.text((360, 150), stamp_txt, font=font(True, 104), fill=stamp_col + (255,), anchor="mm")
                    st = st.rotate(14, expand=True, resample=Image.BICUBIC)
                    st = st.resize((int(st.width * sc), int(st.height * sc)), Image.LANCZOS)
                    img.paste(st, (W // 2 - st.width // 2, 520 - st.height // 2), st)
                    d = ImageDraw.Draw(img, "RGBA")
                if p > 0.32:
                    if item["fact"]:
                        for i in range(3): heart(d, 380 + i * 160, 1240, 44, (240, 80, 90, 255))
                    tc(d, item["ex"][0], W // 2, 1330, font(True, 48), (255, 255, 255))
                    tc(d, item["ex"][1], W // 2, 1400, font(True, 48), (160, 230, 190))
            else:
                textbox(d, 1000, item["bo"], (120, 200, 255), 48)
                tc(d, "BONUS!", W // 2, 1290, font(True, 52), (255, 209, 102))
                follow(d, p)
        elif typ == "top5":
            n_show = [2, 4, 5][bi]
            for i in range(n_show):
                y = 950 + i * 128
                hot = (i == n_show - 1)
                col = (255, 190, 40, 245) if (hot and i == 4) else (35, 45, 80, 235)
                txtc = (18, 18, 28) if (hot and i == 4) else (255, 255, 255)
                pop = 1.0 + (0.10 * seg(p, 0.05, 0.4) if (bi > 0 and i == n_show - 1) else 0.0)
                d.rounded_rectangle([90, y, 990, y + 108], 22, fill=col)
                tc(d, item["items"][i], W // 2, y + 34, font(True, int(42 * pop)), txtc)
            if bi == 2: follow(d, p)
            if bi == 0: tc(d, "Countdown shuru! 5 se 1 tak...", W // 2, 1620, font(True, 44), (180, 220, 255))

        cap = (item.get("vo", [""])[bi] if typ != "story" else item["vo"][bi])
        d.rounded_rectangle([40, 1760, 1040, 1860], 18, fill=(0, 0, 0, 170))
        lines = wrap(d, cap, font(True, 36), 940)
        yy = 1792 - (len(lines) - 1) * 21
        for ln in lines[:2]:
            tc(d, ln, W // 2, yy, font(True, 36), (255, 255, 255)); yy += 42
        return img
    return frame

# ============================ MAIN ============================
def main():
    args = sys.argv[1:]
    typ = "fact"
    if "--type" in args: typ = args[args.index("--type") + 1].strip()
    if typ not in BANKS:
        print("type galat hai:", typ, "| sahi:", list(BANKS)); return
    name, bank, accent = BANKS[typ]
    idx = None
    if "--index" in args: idx = int(args[args.index("--index") + 1]) % len(bank)
    if idx is None:
        env = os.environ.get("SHORT_INDEX", "").strip()
        idx = int(env) % len(bank) if env.isdigit() else datetime.date.today().toordinal() % len(bank)
    item = bank[idx]
    print(f"{name} INDEX={idx} TITLE={item['title']}")
    img_path = fetch_image(item["q"])
    photo = Image.open(img_path).convert("RGB")
    clips = [synth(t, f"{typ}_c{i}.mp3") for i, t in enumerate(item["vo"])]
    durs = [dur(c) for c in clips]
    print("voice durations:", [round(x, 1) for x in durs])
    frame = make_frame(typ, item, photo)
    aud = os.path.join(TMP, "a.m4a"); lst = os.path.join(TMP, "list.txt")
    with open(lst, "w") as fh:
        for c in clips: fh.write(f"file '{c}'\n")
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", "apad=pad_dur=2", "-c:a", "aac", "-b:a", "160k", aud], check=True)
    out = os.path.join(BASE, "output", f"short_{typ}_{idx:02d}.mp4")
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
            frame(bi, 0.6, 0).save(os.path.join(TMP, "thumb.jpg"), quality=88)
    proc.stdin.close(); proc.wait()
    shutil.move(os.path.join(TMP, "v.mp4"), out)
    print("VIDEO:", out, f"{os.path.getsize(out)/1e6:.1f} MB", f"{dur(out):.1f}s")
    if "--upload" in args:
        sys.path.insert(0, BASE)
        from youtube_uploader import upload_to_youtube
        tagmap = {"fact": ["science facts hindi", "did you know", "hindi facts"],
                  "quiz": ["gk quiz hindi", "quiz shorts", "general knowledge"],
                  "story": ["kids story hindi", "moral story", "kahani"],
                  "factmyth": ["fact or myth", "myth vs fact", "hindi facts"],
                  "top5": ["top 5 hindi", "top 5 facts", "countdown"]}
        plan = {"title": f"{item['title']} 😱 #shorts",
                "description": f"{item['title']}\n\nRoz nayi Shorts — Science Facts, Quiz, Kahani, Fact ya Myth aur Top 5!\nEducational bro ko follow karo!\n#shorts #hindi #facts",
                "tags": tagmap[typ] + ["educational bro", "shorts", "hindi"]}
        vid = upload_to_youtube(out, os.path.join(TMP, "thumb.jpg"), plan, "shorts")
        print("YOUTUBE_VIDEO_ID:", vid)
        print("YOUTUBE_URL: https://youtube.com/watch?v=" + str(vid))

if __name__ == "__main__":
    main()
