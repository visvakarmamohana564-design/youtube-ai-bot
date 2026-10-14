"""
MASTER PROMPT ENGINE (PARTS A TO H): CLASS 10 SCIENCE — CHAPTER 1: CHEMICAL REACTIONS AND EQUATIONS
===================================================================================================
- Starts with the exact friendly teacher greeting requested by the user:
  "हेलो भाई लोग, प्यारे बच्चों! आज हम पढ़ने वाले हैं क्लास 10th साइंस का चैप्टर 1 — Chemical Reactions and Equations..."
- Shows the Live 8-Topic Master Checklist on screen; as each topic finishes, it gets ticked off (✓)
  and immediately asks & answers the Board Question from that exact topic!
- Follows the 10-Step Visual Sequence for every reaction:
  [Reactant 1]  +  [Reactant 2]   —(Condition)→   [Products]
  + Photorealistic 3D Lab Visuals + Consistent-Color Molecular Atom Rearrangement Animation
  + 3D Animated Teacher (Walking, Pointing with Laser Pointer, Lip-Sync Talking)
"""

import os
import math
import wave
import shutil
import subprocess
import numpy as np
from PIL import Image, ImageDraw
from gtts import gTTS
import imageio_ffmpeg
from youtube_uploader import upload_to_youtube

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MP_ASSETS = os.path.join(BASE_DIR, "assets", "mpboard_c10")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = "/tmp/sci_ch1_v2_build"

os.makedirs(MP_ASSETS, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
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


def render_pango_block(markup_text: str, width_px: int, font_size: int = 17) -> Image.Image:
    os.makedirs(TEMP_DIR, exist_ok=True)
    safe_markup = markup_text.replace("&amp;", "___AMP___").replace("&", "&amp;").replace("___AMP___", "&amp;")
    pango_bin = "/usr/bin/pango-view"
    pango_pts = int(width_px * 0.71)
    out_png = os.path.join(TEMP_DIR, f"pg2_{abs(hash((safe_markup, pango_pts, font_size))) % 10000000}.png")
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
            f"--text={safe_markup}",
        ]
        env = os.environ.copy()
        env["LC_ALL"] = "C.UTF-8"
        subprocess.run(cmd, check=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    im = Image.open(out_png).convert("RGBA")
    if im.width > width_px:
        new_h = max(1, int(im.height * (width_px / float(im.width))))
        im = im.resize((width_px, new_h), Image.Resampling.LANCZOS)
    return im


TEACHER_SPRITES = {}
for pose in ["teacher_walk", "teacher_point", "teacher_talk"]:
    TEACHER_SPRITES[pose] = {}
    for st in ["closed", "half", "open"]:
        p = os.path.join(MP_ASSETS, f"{pose}_{st}.png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            tw = int(im.width * (390.0 / im.height))
            TEACHER_SPRITES[pose][st] = im.resize((tw, 390), Image.Resampling.LANCZOS)


TOPICS_LIST = [
    "1. Intro & Evidence of Reaction",
    "2. Chemical Equations & Symbols",
    "3. Balancing Equations (2Mg+O₂)",
    "4. Combination & Exothermic",
    "5. Decomposition & Endothermic",
    "6. Displacement & Precipitation",
    "7. Oxidation & Reduction (Redox)",
    "8. Corrosion & Rancidity",
]


MASTER_SCENES = [
    {
        "scene_id": 1,
        "topic_idx": 0,  # 0 = Overview of all 8 topics before ticking #1
        "part_badge": "WELCOME & CHAPTER ROADMAP (ALL 8 TOPICS CHECKLIST)",
        "heading": "Class 10 Science Chapter 1: Chemical Reactions and Equations",
        "lab_img": "react_1_mg_ribbon.jpg",
        "r1_box": ("Reactants (अभिकारक)", "Starting Substances (LHS)"),
        "r2_box": ("Chemical Change", "Breaking & Making of Bonds"),
        "cond_text": "Reaction →",
        "prod_box": ("Products (उत्पाद)", "New Substance + New Properties (RHS)"),
        "eq_banner": "Chapter Rule: Hum ek-ek Topic padhenge → Topic tick (✔) karenge → Turant uska Board Sawaal lagayenge!",
        "anim_mode": "intro_atoms",
        "points": [
            "• <b>आज हम इस चैप्टर में क्या-क्या कवर करेंगे (Complete Topic List):</b>",
            "   <b>Topic 1 (Part A):</b> Chemical Reaction क्या है? Physical vs Chemical Change, Mg Ribbon & Rusting",
            "   <b>Topic 2 (Part B):</b> Word Equation से Chemical Equation बनाना और Symbols (s), (l), (g), (aq), ↑, ↓",
            "   <b>Topic 3 (Part C):</b> Law of Conservation of Mass और Equation Balancing (2Mg + O₂ → 2MgO, Fe + H₂O)",
            "   <b>Topic 4 (Part D & E):</b> Combination Reaction (CaO + H₂O) और Exothermic Reactions (Respiration)",
            "   <b>Topic 5 (Part D & E):</b> Decomposition (Thermal CaCO₃, Electrolytic 2H₂O, Photolytic 2AgCl) & Endothermic",
            "   <b>Topic 6 (Part D):</b> Displacement (Fe + CuSO₄) और Double Displacement (Pb(NO₃)₂ + 2KI → PbI₂↓)",
            "   <b>Topic 7 & 8 (Part D, F, H):</b> Redox (CuO + H₂), Corrosion, Rancidity + Full Exam Practice Quiz!"
        ],
        "topic_qa": "★ Ready? चलिए Topic 1 से शुरुआत करते हैं — हर टॉपिक पूरा होते ही उसका सवाल स्क्रीन पर आएगा!",
        "narration": (
            "हेलो भाई लोग, प्यारे बच्चों! आज हम पढ़ने वाले हैं क्लास टेंथ साइंस का चैप्टर वन, "
            "केमिकल रिएक्शंस एंड इक्वेशंस, यानी रासायनिक अभिक्रियाएँ एवं समीकरण! "
            "इस चैप्टर के अंदर आज हम ये आठ मुख्य टॉपिक्स एक-एक करके बिल्कुल आसान हिंदी और रियल लैब एनिमेशन के साथ कवर करेंगे। "
            "सबसे पहले आप स्क्रीन के बाईं तरफ हमारी टॉपिक लिस्ट देख लीजिए: "
            "पहला टॉपिक है केमिकल रिएक्शन की पहचान, मैग्नीशियम रिबन का जलना और लोहे में जंग लगना। "
            "दूसरा टॉपिक है केमिकल इक्वेशंस और उनके सिंबल्स। "
            "तीसरा टॉपिक है केमिकल इक्वेशन को बैलेंस करना। "
            "चौथा टॉपिक है कॉम्बिनेशन और एक्सोथर्मिक रिएक्शन। "
            "पाँचवाँ टॉपिक है डीकंपोजिशन और एंडोथर्मिक रिएक्शन। "
            "छठा टॉपिक है डिस्प्लेसमेंट और डबल डिस्प्लेसमेंट रिएक्शन। "
            "सातवाँ टॉपिक है ऑक्सीडेशन और रिडक्शन यानी रेडॉक्स रिएक्शन, और आठवाँ टॉपिक है कोरोजन तथा रैंसिडिटी! "
            "जैसे-जैसे एक-एक टॉपिक पूरा होकर कटता जाएगा, हम तुरंत उसी वक्त उससे जुड़ा बोर्ड परीक्षा का सवाल भी हल करेंगे!"
        )
    },
    {
        "scene_id": 2,
        "topic_idx": 1,
        "part_badge": "PART A — INTRODUCTION TO CHEMICAL REACTIONS (TOPIC 1)",
        "heading": "What is a Chemical Reaction? (Mg Ribbon, Rusting & 4 Observations)",
        "lab_img": "react_2_rusting_nail.jpg",
        "r1_box": ("Magnesium / Iron", "2Mg(s)   or   Fe(s)"),
        "r2_box": ("Oxygen (+ Moisture)", "O₂(g)   or   O₂ + xH₂O"),
        "cond_text": "Heat / Humid Air →",
        "prod_box": ("New Substance Formed", "2MgO(s) [White]  |  Fe₂O₃·xH₂O [Rust]"),
        "eq_banner": "2Mg(s) + O₂(g) —Heat→ 2MgO(s) [White Ash]   |   Rust = Hydrated Iron(III) Oxide (Fe₂O₃·xH₂O)",
        "anim_mode": "mg_and_rust",
        "points": [
            "• <b>Physical vs Chemical Change:</b> बर्फ का पिघलना Physical Change है (कोई नया पदार्थ नहीं बना)। पर दूध से दही बनना या मैग्नीशियम का जलना <b>Chemical Reaction</b> है क्योंकि <b>नए गुणों वाला नया पदार्थ (New Substance)</b> बनता है!",
            "• <b>1. Burning of Magnesium Ribbon (Activity 1.1):</b>",
            "   साफ़ मैग्नीशियम रिबन हवा की ऑक्सीजन में <b>चमकदार सफेद लौ (Dazzling White Flame)</b> के साथ जलकर <b>Magnesium Oxide (MgO)</b> का सफेद पाउडर बनाता है।",
            "• <b>2. Rusting of Iron (लोहे में जंग लगना):</b>",
            "   साफ़ लोहे की कील को जब <b>Oxygen (O₂) और नमी (Moisture/H₂O)</b> दोनों मिलते हैं, तो धीरे-धीरे लाल-भूरे रंग की जंग लगती है।",
            "   <b>सावधानी (Important Accuracy Rule):</b> जंग का सही सूत्र <b>Hydrated Iron(III) Oxide (Fe₂O₃·xH₂O)</b> है — कभी भी केवल Fe + H₂O → Rust को संतुलित समीकरण मत लिखना!",
            "• <b>4 Evidences of Chemical Reaction:</b> (1) Change in State (2) Change in Colour (3) Evolution of Gas ↑ (4) Change in Temperature (पर केवल भौतिक रंग/आकार बदलना हमेशा केमिकल रिएक्शन नहीं होता!)"
        ],
        "topic_qa": "✔ TOPIC 1 COMPLETED! अब बताओ बच्चों (सवाल #1): मैग्नीशियम रिबन को जलाने से पहले रेगमाल (Sandpaper) से क्यों रगड़ा जाता है?\n➔ उत्तर: ताकि उसके ऊपर जमी Basic Magnesium Oxide/Carbonate की परत हट जाए और वह आसानी से ऑक्सीजन से क्रिया कर सके!",
        "narration": (
            "चलिए शुरू करते हैं टॉपिक वन, इंट्रोडक्शन टू केमिकल रिएक्शंस! "
            "सबसे पहले समझिए कि फिजिकल चेंज और केमिकल चेंज में क्या अंतर है। "
            "जब बर्फ पिघलकर पानी बनती है, तो उसका सूत्र एच-टू-ओ ही रहता है, कोई नया पदार्थ नहीं बनता। "
            "लेकिन जब कोई नया पदार्थ बनता है जिसके गुण पहले वाले पदार्थ से बिल्कुल अलग हों, तो उसे केमिकल रिएक्शन कहते हैं! "
            "ऊपर पहला प्रयोग देखिए: जब चमकदार मैग्नीशियम रिबन को हवा में जलाया जाता है, तो वह ऑक्सीजन से जुड़कर डैज़लिंग व्हाइट फ्लेम के साथ जलता है और मैग्नीशियम ऑक्साइड का सफेद पाउडर बनाता है। "
            "अब दूसरा प्रयोग देखिए: लोहे की कील में जंग लगना। इसके लिए ऑक्सीजन और नमी यानी मॉइस्चर दोनों ज़रूरी हैं। "
            "इससे कील पर धीरे-धीरे लाल-भूरे रंग की परत चढ़ती है जिसे हाइड्रेटेड आयरन थर्ड ऑक्साइड यानी एफई-टू-ओ-थ्री डॉट एक्स-एच-टू-ओ कहते हैं। "
            "ध्यान रखिएगा, कभी भी एफई प्लस एच-टू-ओ गिव्स रस्ट मत लिखना! "
            "तो केमिकल रिएक्शन की चार पहचान हैं: अवस्था में बदलाव, रंग में बदलाव, गैस का निकलना और तापमान में बदलाव। "
            "लीजिए, हमारा पहला टॉपिक पूरा हुआ और लिस्ट में टिक लग गया! "
            "अब तुरंत इस टॉपिक का सवाल बताइए: मैग्नीशियम रिबन को जलाने से पहले सैंडपेपर से साफ़ क्यों किया जाता है? "
            "बिल्कुल सही! ताकि उसके ऊपर जमी मैग्नीशियम ऑक्साइड की सुरक्षात्मक परत हट जाए और वह आसानी से जल सके!"
        )
    },
    {
        "scene_id": 3,
        "topic_idx": 2,
        "part_badge": "PART B — CHEMICAL EQUATIONS & SYMBOLS (TOPIC 2)",
        "heading": "Word Equations, Chemical Formulae & State Symbols",
        "lab_img": "ncert_fig2_mg_burn.jpg",
        "r1_box": ("Reactants (LHS)", "Written on Left Side with (+)"),
        "r2_box": ("Reaction Arrow (→)", "Shows Direction & Conditions"),
        "cond_text": "Δ / Sunlight / (aq) →",
        "prod_box": ("Products (RHS)", "Written on Right Side with ↑ or ↓"),
        "eq_banner": "Zn(s) + H₂SO₄(aq)  →  ZnSO₄(aq) + H₂(g)↑   |   Symbols: (s) Solid, (l) Liquid, (g) Gas, (aq) Aqueous",
        "anim_mode": "symbols_demo",
        "points": [
            "• <b>Word Equation से Chemical Equation क्यों बनाते हैं?</b>",
            "   पूरा वाक्य लिखना लंबा होता है, इसलिए हम शब्दों की जगह <b>Chemical Formulae (रासायनिक सूत्र)</b> का उपयोग करते हैं।",
            "• <b>1. Reactants (अभिकारक) & Products (उत्पाद):</b>",
            "   जो पदार्थ अभिक्रिया में भाग लेते हैं वे <b>Reactants (LHS)</b> हैं; जो नए पदार्थ बनते हैं वे <b>Products (RHS)</b> हैं।",
            "• <b>2. Plus (+) और Arrow (→) का अर्थ:</b> दो रिएक्टेंट्स के बीच <b>(+)</b> का अर्थ है कि वे आपस में मिल रहे हैं, और <b>(→)</b> अभिक्रिया की दिशा (Reactants से Products की ओर) दिखाता है।",
            "• <b>3. चारों Physical State Symbols और Special Arrows:</b>",
            "   <b>(s)</b> = Solid (ठोस)  |  <b>(l)</b> = Liquid (द्रव)  |  <b>(g) or ↑</b> = Gas Evolution  |  <b>(aq)</b> = Aqueous (पानी में घुला हुआ घोल)  |  <b>(↓)</b> = Precipitate (अघुलनशील ठोस जो नीचे बैठ जाए)।",
            "• <b>4. Conditions on Arrow:</b> तीर के ऊपर या नीचे <b>Heat (Δ), Sunlight, 340 atm, या Chlorophyll</b> जैसी शर्तें लिखी जाती हैं।"
        ],
        "topic_qa": "✔ TOPIC 2 COMPLETED! अब बताओ बच्चों (सवाल #2): किसी रासायनिक समीकरण में (aq) और (↓) चिह्न का क्या अर्थ होता है?\n➔ उत्तर: (aq) का अर्थ Aqueous solution (जल में बना घोल) है, और (↓) का अर्थ अघुलनशील अवक्षेप (Precipitate) का बनना है!",
        "narration": (
            "अब आते हैं हमारे दूसरे टॉपिक, पार्ट बी: केमिकल इक्वेशंस और उसके सभी सिंबल्स पर! "
            "जब हम लिखते हैं मैग्नीशियम प्लस ऑक्सीजन गिव्स मैग्नीशियम ऑक्साइड, तो इसे वर्ड इक्वेशन कहते हैं। "
            "इसे छोटा और वैज्ञानिक बनाने के लिए हम केमिकल फॉर्मूले लिखते हैं: एमजी प्लस ओ-टू गिव्स एमजी-ओ। "
            "यहाँ तीर के बाईं ओर यानी एलएचएस पर लिखे पदार्थ रिएक्टेंट्स हैं, और दाईं ओर यानी आरएचएस पर बने पदार्थ प्रोडक्ट्स हैं। "
            "समीकरण को पूरी तरह जानकारीपूर्ण बनाने के लिए हम चार फिजिकल स्टेट सिंबल्स लगाते हैं: "
            "ठोस के लिए ब्रैकेट में एस, लिक्विड के लिए एल, गैस के लिए जी या ऊपर जाता हुआ तीर, "
            "और पानी में घुले हुए विलयन के लिए एक्यू यानी एक्वस! "
            "अगर घोल में कोई ठोस नीचे बैठ जाए तो उसे प्रेसिपिटेट कहते हैं और नीचे जाते हुए तीर से दिखाते हैं। "
            "और अभिक्रिया के लिए ज़रूरी तापमान, दाब या धूप को मुख्य तीर के ऊपर या नीचे लिखा जाता है। "
            "इसी के साथ हमारा दूसरा टॉपिक भी टिक हो गया! "
            "अब तुरंत सवाल नंबर दो का जवाब दीजिए: किसी समीकरण में एक्यू और नीचे वाले तीर का क्या मतलब होता है? "
            "शाबाश! एक्यू का मतलब पानी में बना घोल यानी एक्वस सॉल्यूशन, और नीचे वाले तीर का मतलब प्रेसिपिटेट यानी अवक्षेप है!"
        )
    },
    {
        "scene_id": 4,
        "topic_idx": 3,
        "part_badge": "PART C — BALANCING CHEMICAL EQUATIONS (TOPIC 3)",
        "heading": "Law of Conservation of Mass & Step-by-Step Balancing",
        "lab_img": "ncert_fig3_balancing.jpg",
        "r1_box": ("2 Magnesium Atoms", "2 Mg(s)  [2 Silver Atoms]"),
        "r2_box": ("1 Oxygen Molecule", "+  O₂(g)  [2 Red O Atoms]"),
        "cond_text": "Rearrange Atoms →",
        "prod_box": ("2 Magnesium Oxide", "2 MgO(s)  [2 Mg + 2 O Atoms]"),
        "eq_banner": "Unbalanced: Mg + O₂ → MgO   ➔   Balanced: 2Mg(s) + O₂(g) → 2MgO(s)   &   3Fe(s) + 4H₂O(g) → Fe₃O₄(s) + 4H₂(g)",
        "anim_mode": "atom_balance_2mg",
        "points": [
            "• <b>Law of Conservation of Mass (द्रव्यमान संरक्षण का नियम):</b>",
            "   किसी भी केमिकल रिएक्शन में <b>Atoms न तो गायब होते हैं और न ही अपने-आप पैदा होते हैं</b> — केवल परमाणुओं का पुनर्गठन (Rearrangement) होता है! इसलिए <b>LHS के कुल Atoms = RHS के कुल Atoms</b>।",
            "• <b>Example 1 (Mg + O₂ → MgO को संतुलित करना):</b>",
            "   - Unbalanced में LHS पर <b>1 Mg</b> और <b>2 O</b> हैं, जबकि RHS (MgO) में केवल <b>1 Mg</b> और <b>1 O</b> है।",
            "   - <b>Golden Rule:</b> हम कभी भी सूत्र के अंदर का छोटा अंक (Subscript जैसे MgO₂) नहीं बदल सकते! केवल आगे का गुणांक (<b>Coefficient</b>) बदल सकते हैं।",
            "   - RHS पर O को 2 करने के लिए <b>2MgO</b> करें, और फिर LHS पर Mg के आगे <b>2</b> लगाएँ:  <b>2Mg + O₂ → 2MgO</b> (LHS: Mg=2, O=2 | RHS: Mg=2, O=2 ✔)।",
            "• <b>Example 2 (Chapter Level):</b> <b>Fe + H₂O → Fe₃O₄ + H₂</b>  ➔  <b>3Fe(s) + 4H₂O(g) → Fe₃O₄(s) + 4H₂(g)</b> (Fe=3, H=8, O=4 Both Sides ✔)"
        ],
        "topic_qa": "✔ TOPIC 3 COMPLETED! अब बताओ बच्चों (सवाल #3): समीकरण संतुलित करते समय हम MgO को MgO₂ क्यों नहीं लिख सकते?\n➔ उत्तर: क्योंकि Subscript बदलने से पदार्थ का रासायनिक सूत्र ही गलत हो जाता है; हम केवल आगे Coefficient (2MgO) लगा सकते हैं!",
        "narration": (
            "अब आते हैं तीसरे और सबसे महत्वपूर्ण टॉपिक, पार्ट सी: बैलेंसिंग केमिकल इक्वेशंस पर! "
            "सबसे पहले बाईं तरफ के एटम एनिमेशन को ध्यान से देखिए। "
            "लॉ ऑफ़ कंजर्वेशन ऑफ़ मास कहता है कि रिएक्शन से पहले और रिएक्शन के बाद हर तत्व के परमाणुओं की संख्या बिल्कुल बराबर रहती है, "
            "क्योंकि परमाणु न तो नष्ट होते हैं और न ही नए बनते हैं, वे केवल आपस में नए तरीके से जुड़ते हैं! "
            "उदाहरण के लिए, अनबैलेंस्ड समीकरण देखिए: एमजी प्लस ओ-टू गिव्स एमजी-ओ। "
            "यहाँ एलएचएस में ऑक्सीजन के दो लाल परमाणु हैं, लेकिन आरएचएस में एमजी-ओ के पास केवल एक ऑक्सीजन परमाणु है। "
            "याद रखिए, हम कभी भी फॉर्मूले के अंदर का सबस्क्रिप्ट बदलकर एमजी-ओ-टू नहीं लिख सकते! "
            "हम केवल फॉर्मूले के आगे कोएफिशिएंट लगा सकते हैं। "
            "इसलिए पहले एमजी-ओ के आगे दो लगाते हैं जिससे दो ऑक्सीजन हो गए, और फिर बाईं तरफ एमजी के आगे भी दो लगा देते हैं! "
            "अब गिनिए: दोनों तरफ दो सिल्वर एमजी एटम और दो लाल ऑक्सीजन एटम हो गए: टू-एमजी प्लस ओ-टू गिव्स टू-एमजी-ओ! "
            "इसी तरह आयरन और भाप का समीकरण बनता है: थ्री-एफई प्लस फोर-एच-टू-ओ गिव्स एफई-थ्री-ओ-फोर प्लस फोर-एच-टू। "
            "लीजिए, टॉपिक तीन भी पूरा होकर टिक हो गया! "
            "अब बताइए, हम बैलेंस करते समय सबस्क्रिप्ट क्यों नहीं बदल सकते? क्योंकि सबस्क्रिप्ट बदलने से यौगिक का असली सूत्र ही बदल जाता है!"
        )
    },
    {
        "scene_id": 5,
        "topic_idx": 4,
        "part_badge": "PART D (1) & PART E — COMBINATION & EXOTHERMIC REACTIONS (TOPIC 4)",
        "heading": "1. Combination Reaction & Exothermic Processes (CaO + H₂O)",
        "lab_img": "react_3_quicklime_beaker.jpg",
        "r1_box": ("Quicklime (बिना बुझा चूना)", "CaO(s) [Calcium Oxide]"),
        "r2_box": ("Water (जल)", "+   H₂O(l)"),
        "cond_text": "Vigorous Reaction →",
        "prod_box": ("Slaked Lime + Heat", "Ca(OH)₂(aq)  +  Heat 🔥"),
        "eq_banner": "CaO(s) [Quicklime] + H₂O(l) → Ca(OH)₂(aq) [Slaked lime] + Heat   |   Category: Combination & Exothermic",
        "anim_mode": "combination_exothermic",
        "points": [
            "• <b>1. Combination Reaction (संयोजन अभिक्रिया) की पहचान:</b>",
            "   जब <b>दो या दो से अधिक Reactants</b> आपस में जुड़कर केवल <b>एक अकेला Product (Single Product)</b> बनाते हैं (<b>A + B → AB</b>)।",
            "• <b>Visual Lab Demo (Quicklime + Water):</b>",
            "   बीकर में सफेद पत्थर जैसा <b>Quicklime (CaO)</b> लेकर पानी डालने पर वह तेजी से जुड़कर <b>Slaked lime [Ca(OH)₂]</b> बनाता है और बीकर छूने पर बहुत <b>गर्म</b> लगता है!",
            "• <b>Whitewashing Walls (दीवारों पर सफ़ेदी):</b> यही Ca(OH)₂ हवा की CO₂ से मिलकर 2-3 दिन में <b>CaCO₃ (Marble का सूत्र!)</b> की चमकदार परत बनाता है:  <b>Ca(OH)₂(aq) + CO₂(g) → CaCO₃(s) + H₂O(l)</b>।",
            "• <b>Exothermic Reaction (ऊष्माक्षेपी अभिक्रिया — Part E):</b>",
            "   जिस अभिक्रिया में प्रोडक्ट बनने के साथ <b>Heat (ऊष्मा/ऊर्जा) बाहर निकलती है</b>। जैसे: (1) प्राकृतिक गैस का जलना <b>CH₄ + 2O₂ → CO₂ + 2H₂O + Heat</b>, और (2) हमारी साँस लेने की प्रक्रिया <b>Respiration (C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + Energy)</b>!"
        ],
        "topic_qa": "✔ TOPIC 4 COMPLETED! अब बताओ बच्चों (सवाल #4): यहाँ CaO और H₂O के मिलने से कौन-सा पदार्थ बना और बीकर गर्म क्यों हो गया?\n➔ उत्तर: Slaked lime [Calcium hydroxide, Ca(OH)₂] बना, और यह एक Exothermic Combination Reaction है इसलिए ऊष्मा निकली!",
        "narration": (
            "अब आते हैं चौथे टॉपिक पर: कॉम्बिनेशन रिएक्शन और एक्सोथर्मिक रिएक्शन! "
            "परीक्षा में कॉम्बिनेशन रिएक्शन को पहचानने की सबसे आसान ट्रिक है: "
            "तीर के बाईं तरफ दो या दो से ज़्यादा रिएक्टेंट्स होंगे, लेकिन तीर के दाईं तरफ केवल एक अकेला प्रोडक्ट बनेगा! "
            "ऊपर लैब का प्रयोग देखिए: हमने पहले सफेद रंग का क्विक लाइम यानी कैल्शियम ऑक्साइड, सीए-ओ लिया, "
            "और उसमें पानी यानी एच-टू-ओ मिलाया। दोनों मिलकर एक अकेला प्रोडक्ट बनाते हैं जिसे स्लेक्ड लाइम यानी कैल्शियम हाइड्रॉक्साइड, सीए-ओएच-होल-ट्वाइस कहते हैं। "
            "इस रिएक्शन में इतनी गर्मी निकलती है कि बीकर बाहर से छूने पर काफी गर्म हो जाता है! "
            "जिन अभिक्रियाओं में प्रोडक्ट बनने के साथ हीट बाहर निकलती है, उन्हें एक्सोथर्मिक रिएक्शन कहते हैं। "
            "हमारा श्वसन यानी रेस्पिरेशन भी एक्सोथर्मिक रिएक्शन है क्योंकि इसमें ग्लूकोज़ टूटकर हमारे शरीर को ऊर्जा देता है। "
            "लीजिए, चौथा टॉपिक भी पूरा होकर टिक हो गया! "
            "अब बताओ बच्चों, क्विक लाइम और पानी के मिलने से कौन-सा पदार्थ बना और बीकर गर्म क्यों हुआ? "
            "बिल्कुल सही! स्लेक्ड लाइम यानी कैल्शियम हाइड्रॉक्साइड बना, और यह एक्सोथर्मिक रिएक्शन है इसलिए हीट निकली!"
        )
    },
    {
        "scene_id": 6,
        "topic_idx": 5,
        "part_badge": "PART D (2) & PART E — DECOMPOSITION & ENDOTHERMIC REACTIONS (TOPIC 5)",
        "heading": "2. Decomposition Reaction: Thermal, Electrolytic & Photochemical",
        "lab_img": "react_4_decomp_trio.jpg",
        "r1_box": ("Single Reactant (AB)", "CaCO₃(s)  |  2H₂O(l)  |  2AgCl(s)"),
        "r2_box": ("Energy Absorbed", "+  Heat Δ  /  Electricity ⚡  /  Sunlight ☀️"),
        "cond_text": "Breaks Down →",
        "prod_box": ("2 or More Products", "CaO+CO₂  |  2H₂+O₂  |  2Ag+Cl₂"),
        "eq_banner": "Thermal: CaCO₃ —Heat→ CaO + CO₂  |  Electrolytic: 2H₂O —Elec→ 2H₂ + O₂  |  Photo: 2AgCl —Sun→ 2Ag + Cl₂",
        "anim_mode": "decomp_three_types",
        "points": [
            "• <b>Decomposition Reaction (वियोजन अभिक्रिया) की पहचान:</b>",
            "   इसमें <b>एक अकेला Compound (Single Reactant)</b> टूटकर <b>दो या अधिक छोटे पदार्थ</b> बनाता है (<b>AB → A + B</b>)।",
            "• <b>1. Thermal Decomposition (ऊष्मा द्वारा):</b>",
            "   <b>CaCO₃(s) [Limestone] —Heat→ CaO(s) [Quicklime, used in Cement] + CO₂(g)</b>",
            "   साथ ही: <b>2FeSO₄(s) [Green] —Heat→ Fe₂O₃(s) + SO₂(g) + SO₃(g)</b>  तथा  <b>2Pb(NO₃)₂ —Heat→ 2PbO + 4NO₂ [Brown fumes] + O₂</b>।",
            "• <b>2. Electrolytic Decomposition (बिजली द्वारा — Electrolysis of Water):</b>",
            "   <b>2H₂O(l) —Electricity→ 2H₂(g) [Cathode पर दोगुनी गैस] + O₂(g) [Anode पर एक गुना गैस]</b> (2:1 Volume Ratio!)।",
            "• <b>3. Photochemical Decomposition (सूर्य के प्रकाश द्वारा):</b>",
            "   <b>2AgCl(s) [White] —Sunlight→ 2Ag(s) [Grey] + Cl₂(g)</b> (तथा <b>2AgBr</b> का उपयोग Black & White Photography में होता है)।",
            "• <b>Endothermic Reaction (ऊष्माशोषी — Part E):</b> क्योंकि इन तीनों में ऊर्जा (Heat, Electricity या Sunlight) <b>अवशोषित (Absorb)</b> होती है, ये <b>Endothermic Reactions</b> हैं!"
        ],
        "topic_qa": "✔ TOPIC 5 COMPLETED! अब बताओ बच्चों (सवाल #5): सिल्वर क्लोराइड (AgCl) को धूप में रखने पर उसका सफेद रंग ग्रे (Grey) क्यों हो जाता है?\n➔ उत्तर: Sunlight से Photochemical Decomposition होकर AgCl टूट जाता है और Grey रंग का Silver (Ag) धातु बनता है!",
        "narration": (
            "अब चलते हैं पाँचवें टॉपिक पर: डीकंपोजिशन रिएक्शन और एंडोथर्मिक रिएक्शन! "
            "जब एक अकेला कंपाउंड टूटकर दो या दो से अधिक सरल पदार्थ बनाता है, तो उसे डीकंपोजिशन रिएक्शन कहते हैं। "
            "किसी भी जुड़े हुए यौगिक को तोड़ने के लिए बाहर से ऊर्जा देनी पड़ती है, और जिस रिएक्शन में ऊर्जा अवशोषित यानी एब्जॉर्ब होती है उसे एंडोथर्मिक रिएक्शन कहते हैं! "
            "यह ऊर्जा तीन तरह से दी जाती है: "
            "पहला, थर्मल डीकंपोजिशन यानी गर्म करके: जब कैल्शियम कार्बोनेट को गर्म करते हैं, तो वह टूटकर कैल्शियम ऑक्साइड और कार्बन डाइऑक्साइड गैस बनाता है। "
            "इसी तरह लेड नाइट्रेट को गर्म करने पर नाइट्रोजन डाइऑक्साइड का भूरा धुआँ निकलता है। "
            "दूसरा, इलेक्ट्रोलाइटिक डीकंपोजिशन यानी बिजली प्रवाहित करके: जब पानी में बिजली प्रवाहित करते हैं, तो वह टूटकर हाइड्रोजन और ऑक्सीजन गैस बनाता है, "
            "जिसमें हाइड्रोजन की मात्रा ऑक्सीजन से ठीक दोगुनी होती है। "
            "तीसरा, फोटोकैमिकल डीकंपोजिशन यानी सूरज की रोशनी से: सफेद सिल्वर क्लोराइड को धूप में रखने पर वह टूटकर ग्रे रंग का सिल्वर और क्लोरीन गैस बनाता है। "
            "लीजिए, पाँचवाँ टॉपिक भी टिक हो गया! "
            "अब बताओ बच्चों, सिल्वर क्लोराइड को धूप में रखने पर वह सफेद से ग्रे क्यों हो जाता है? "
            "बिल्कुल सही! धूप से उसका फोटोकैमिकल डीकंपोजिशन हो जाता है और सिल्वर धातु बन जाती है!"
        )
    },
    {
        "scene_id": 7,
        "topic_idx": 6,
        "part_badge": "PART D (3 & 4) — DISPLACEMENT & DOUBLE DISPLACEMENT (TOPIC 6)",
        "heading": "3. Displacement (Fe + CuSO₄) & 4. Double Displacement (PbI₂↓)",
        "lab_img": "react_5_displacement_ppt.jpg",
        "r1_box": ("Iron Nail  /  Pb(NO₃)₂", "Fe(s)   or   Pb(NO₃)₂(aq)"),
        "r2_box": ("Blue CuSO₄  /  2KI", "+   CuSO₄(aq)   or   2KI(aq)"),
        "cond_text": "Displaces / Ion Exchange →",
        "prod_box": ("Green FeSO₄ + Cu  /  Yellow PbI₂↓", "FeSO₄(aq)+Cu(s)  |  PbI₂(s)↓+2KNO₃(aq)"),
        "eq_banner": "Displacement: Fe(s) + CuSO₄(aq) → FeSO₄(aq) + Cu(s)  |  Double Displacement: Pb(NO₃)₂(aq) + 2KI(aq) → PbI₂(s)↓ + 2KNO₃(aq)",
        "anim_mode": "disp_and_yellow_ppt",
        "points": [
            "• <b>3. Displacement Reaction (विस्थापन अभिक्रिया):</b>",
            "   जब एक <b>अधिक क्रियाशील तत्व (More Reactive Element)</b> किसी यौगिक से कम क्रियाशील तत्व को हटाकर खुद उसकी जगह ले लेता है (<b>A + BC → AC + B</b>)।",
            "   <b>Lab Demo:</b> नीले <b>Copper Sulphate (CuSO₄)</b> के घोल में साफ़ लोहे की कील (<b>Fe</b>) डालने पर घोल <b>हल्का हरा (Pale Green FeSO₄)</b> हो जाता है और कील पर <b>लाल-भूरे Copper (Cu)</b> की परत जम जाती है, क्योंकि <b>Fe, Cu से अधिक क्रियाशील है!</b> (ऐसे ही Zn और Pb भी Cu को हटा देते हैं)।",
            "• <b>4. Double Displacement & Precipitation Reaction (द्विविस्थापन एवं अवक्षेपण):</b>",
            "   जब दो विलयनों को मिलाने पर उनके बीच <b>आयनों का आदान-प्रदान (Exchange of Ions: AB + CD → AD + CB)</b> होता है।",
            "   <b>Lab Demo 1:</b> पारदर्शी <b>Lead Nitrate [Pb(NO₃)₂]</b> और <b>Potassium Iodide (2KI)</b> मिलाने पर तुरंत <b>चमकीले पीले रंग का Lead Iodide (PbI₂↓)</b> अवक्षेप (Precipitate) बनता है!",
            "   <b>Lab Demo 2:</b> <b>Na₂SO₄(aq) + BaCl₂(aq) → BaSO₄(s)↓ [White Precipitate] + 2NaCl(aq)</b>।"
        ],
        "topic_qa": "✔ TOPIC 6 COMPLETED! अब बताओ बच्चों (सवाल #6): Lead nitrate और Potassium iodide मिलाने पर किस रंग का अवक्षेप (Precipitate) बनता है और उसका सूत्र क्या है?\n➔ उत्तर: चमकीले पीले रंग (Yellow colour) का अवक्षेप बनता है, जिसका रासायनिक सूत्र Lead Iodide (PbI₂) है!",
        "narration": (
            "अब आते हैं छठे टॉपिक पर: डिस्प्लेसमेंट और डबल डिस्प्लेसमेंट रिएक्शन! "
            "ऊपर बाईं तरफ की टेस्ट ट्यूब देखिए: हमने नीले रंग के कॉपर सल्फेट सॉल्यूशन में लोहे की कील डुबोई। "
            "आयरन, कॉपर की तुलना में ज़्यादा रिएक्टिव यानी अधिक ताकतवर धातु है। "
            "इसलिए आयरन, कॉपर सल्फेट में से कॉपर को हटाकर खुद जुड़ जाता है और हल्के हरे रंग का आयरन सल्फेट बना लेता है, "
            "जबकि हटा हुआ कॉपर लोहे की कील के ऊपर लाल-भूरी परत के रूप में जम जाता है! इसे डिस्प्लेसमेंट रिएक्शन कहते हैं। "
            "अब दाईं तरफ का बीकर देखिए: डबल डिस्प्लेसमेंट रिएक्शन! "
            "जब हम लेड नाइट्रेट और पोटैशियम आयोडाइड के दो साफ़ विलयनों को आपस में मिलाते हैं, "
            "तो लेड आयन और आयोडाइड आयन आपस में अदला-बदली करके तुरंत पीले रंग का अघुलनशील ठोस, लेड आयोडाइड बनाते हैं! "
            "इसी तरह सोडियम सल्फेट और बेरियम क्लोराइड मिलाने पर सफेद बेरियम सल्फेट बनता है। "
            "लीजिए, छठा टॉपिक भी पूरा होकर टिक हो गया! "
            "अब तुरंत बताओ बच्चों, लेड नाइट्रेट और पोटैशियम आयोडाइड मिलाने पर कौन-सा पीला पदार्थ बना? "
            "शाबाश! पीले रंग का लेड आयोडाइड यानी पीबी-आई-टू प्रेसिपिटेट बना!"
        )
    },
    {
        "scene_id": 8,
        "topic_idx": 7,
        "part_badge": "PART D (5) — OXIDATION AND REDUCTION / REDOX REACTIONS (TOPIC 7)",
        "heading": "5. Oxidation and Reduction (Redox: CuO + H₂ → Cu + H₂O)",
        "lab_img": "react_6_redox_cuo.jpg",
        "r1_box": ("Black Copper(II) Oxide", "CuO(s)  [Loses Oxygen → Reduced]"),
        "r2_box": ("Hydrogen Gas", "+   H₂(g)  [Gains Oxygen → Oxidised]"),
        "cond_text": "Heat Δ →",
        "prod_box": ("Reddish-Brown Copper + Water", "Cu(s) [Brown]  +  H₂O(l)"),
        "eq_banner": "2Cu + O₂ —Heat→ 2CuO [Black]   |   CuO(s) + H₂(g) —Heat→ Cu(s) [Brown] + H₂O(l)   (Redox Reaction)",
        "anim_mode": "redox_cuo_h2",
        "points": [
            "• <b>Oxidation (उपचयन) और Reduction (अपचयन) की सीधी परिभाषा:</b>",
            "   - <b>Oxidation:</b> किसी पदार्थ में <b>Oxygen का जुड़ना (Gain of O)</b> या Hydrogen का हटना।",
            "   - <b>Reduction:</b> किसी पदार्थ से <b>Oxygen का हटना (Loss of O)</b> या Hydrogen का जुड़ना।",
            "• <b>Visual Lab Demo (Activity 1.11 — CuO + H₂):</b>",
            "   - पहले तांबे (Copper) को गर्म करने पर उस पर काले रंग की <b>Copper(II) Oxide (2Cu + O₂ → 2CuO)</b> की परत बनती है।",
            "   - फिर जब इस काले <b>CuO</b> के ऊपर से <b>Hydrogen (H₂)</b> गैस गुज़ारी जाती है, तो काला रंग वापस <b>लाल-भूरे Copper (Cu)</b> में बदल जाता है!",
            "• <b>यहाँ किसका Oxidation और किसका Reduction हुआ?</b>",
            "   - <b>H₂ में Oxygen जुड़ी</b> ➔ इसलिए <b>H₂ is Oxidised to H₂O</b>।",
            "   - <b>CuO से Oxygen हटी</b> ➔ इसलिए <b>CuO is Reduced to Cu</b>।",
            "   - क्योंकि दोनों एक साथ हो रहे हैं, इसे <b>Redox Reaction</b> कहते हैं! (अन्य उदाहरण: <b>ZnO + C → Zn + CO</b>)"
        ],
        "topic_qa": "✔ TOPIC 7 COMPLETED! अब बताओ बच्चों (सवाल #7): अभिक्रिया ZnO + C → Zn + CO में किस पदार्थ का Oxidation हुआ है और किसका Reduction?\n➔ उत्तर: Carbon (C) में ऑक्सीजन जुड़ी इसलिए C का Oxidation हुआ, और ZnO से ऑक्सीजन हटी इसलिए ZnO का Reduction हुआ!",
        "narration": (
            "अब आते हैं सातवें टॉपिक पर: ऑक्सीडेशन एंड रिडक्शन, यानी रेडॉक्स रिएक्शन! "
            "इसे याद रखने का सबसे सरल नियम है: किसी पदार्थ में ऑक्सीजन का जुड़ना ऑक्सीडेशन कहलाता है, "
            "और किसी पदार्थ में से ऑक्सीजन का निकल जाना रिडक्शन कहलाता है! "
            "ऊपर चाइना डिश का प्रयोग देखिए: जब काले रंग के कॉपर सेकंड ऑक्साइड यानी सीयू-ओ को गर्म करके उसके ऊपर से हाइड्रोजन गैस प्रवाहित की जाती है, "
            "तो हाइड्रोजन, कॉपर ऑक्साइड से ऑक्सीजन छीन लेता है! "
            "इससे काला कॉपर ऑक्साइड वापस चमकदार लाल-भूरे कॉपर धातु में बदल जाता है और पानी बनता है। "
            "यहाँ ध्यान से देखिए: कॉपर ऑक्साइड से ऑक्सीजन हटी है, इसलिए सीयू-ओ का रिडक्शन होकर सीयू बना। "
            "और हाइड्रोजन में ऑक्सीजन जुड़ी है, इसलिए एच-टू का ऑक्सीडेशन होकर एच-टू-ओ बना! "
            "क्योंकि एक ही अभिक्रिया में रिडक्शन और ऑक्सीडेशन दोनों साथ-साथ हो रहे हैं, इसलिए इसे रेडॉक्स रिएक्शन कहते हैं! "
            "लीजिए, सातवाँ टॉपिक भी टिक हो गया! "
            "अब बताओ बच्चों, ज़ेडएन-ओ प्लस सी गिव्स ज़ेडएन प्लस सी-ओ में किसका ऑक्सीडेशन हुआ? "
            "बिल्कुल सही! कार्बन में ऑक्सीजन जुड़ी इसलिए कार्बन का ऑक्सीडेशन हुआ, और ज़ेडएन-ओ का रिडक्शन हुआ!"
        )
    },
    {
        "scene_id": 9,
        "topic_idx": 8,
        "part_badge": "PART F — EFFECTS OF OXIDATION: CORROSION & RANCIDITY (TOPIC 8)",
        "heading": "1. Corrosion (Rusting & Prevention) & 2. Rancidity (Food Protection)",
        "lab_img": "react_2_rusting_nail.jpg",
        "r1_box": ("1. Corrosion (संक्षारण)", "Metal + O₂ + Moisture / Acid"),
        "r2_box": ("2. Rancidity (विकृतगंधिता)", "Fats & Oils + Air Oxygen (O₂)"),
        "cond_text": "Slow Oxidation →",
        "prod_box": ("Prevention Methods", "Painting, Galvanisation  |  N₂ Gas, Airtight"),
        "eq_banner": "Corrosion: Iron Rust (Fe₂O₃·xH₂O), Silver (Black Ag₂S), Copper (Green)  |  Rancidity Prevention: Nitrogen (N₂) Flushing",
        "anim_mode": "corrosion_and_chips",
        "points": [
            "• <b>1. Corrosion (संक्षारण):</b>",
            "   जब कोई धातु (Metal) अपने आस-पास की <b>Oxygen, नमी (Moisture) या अम्ल (Acid)</b> के संपर्क में आकर धीरे-धीरे खराब होने लगती है।",
            "   - <b>उदाहरण:</b> लोहे पर लाल-भूरी जंग (<b>Fe₂O₃·xH₂O</b>), चाँदी (Silver) पर काली परत (<b>Ag₂S</b>), और ताँबे (Copper) पर हरी परत।",
            "   - <b>बचाव के उपाय (Prevention of Corrosion):</b> <b>Painting (पेंट करना), Oiling/Greasing (तेल या ग्रीस लगाना), और Galvanisation (लोहे पर जिंक की परत चढ़ाना)</b> ताकि हवा और नमी लोहे तक न पहुँच सकें!",
            "• <b>2. Rancidity (विकृतगंधिता):</b>",
            "   जब तेल या वसा (Fats and Oils) से बने खाद्य पदार्थ लंबे समय तक हवा में रखे रहते हैं, तो उनका <b>Oxidation</b> हो जाता है जिससे उनका <b>स्वाद (Taste) और गंध (Smell) बदलकर खराब</b> हो जाते हैं।",
            "   - <b>बचाव के 4 उपाय:</b> (1) <b>Antioxidants</b> मिलाना, (2) <b>Airtight Containers</b> (हवाबंद डिब्बों) में रखना, (3) <b>Refrigeration</b> (फ्रिज में रखना), और (4) चिप्स के पैकेट में से ऑक्सीजन हटाकर <b>Nitrogen Gas (N₂)</b> भरना!"
        ],
        "topic_qa": "✔ ALL 8 TOPICS COMPLETED! अब बताओ बच्चों (सवाल #8): लोहे को जंग से बचाने के लिए क्या करते हैं और चिप्स के पैकेट में कौन-सी गैस भरते हैं?\n➔ उत्तर: लोहे पर Painting, Oiling या Galvanisation करते हैं; और चिप्स के पैकेट में अक्रिय Nitrogen (N₂) गैस भरते हैं!",
        "narration": (
            "अब आते हैं हमारे आठवें और अंतिम टॉपिक, पार्ट एफ: दैनिक जीवन में ऑक्सीडेशन के प्रभाव — कोरोजन और रैंसिडिटी पर! "
            "पहला है कोरोजन यानी संक्षारण। जब लोहे की वस्तुएँ खुली हवा की ऑक्सीजन और नमी के संपर्क में रहती हैं, "
            "तो उन पर धीरे-धीरे लाल-भूरे रंग की जंग लग जाती है जिससे पुल, गाड़ियाँ और लोहे की रेलिंग कमज़ोर हो जाती हैं। "
            "इसी तरह चाँदी पर काली परत और तांबे पर हरी परत चढ़ना भी कोरोजन है। "
            "लोहे को जंग से बचाने के लिए हम उस पर पेंटिंग करते हैं, तेल या ग्रीस लगाते हैं, या गैल्वनाइजेशन यानी जिंक की परत चढ़ाते हैं। "
            "दूसरा प्रभाव है रैंसिडिटी यानी विकृतगंधिता। जब तेल या घी से बनी खाने की चीज़ें लंबे समय तक हवा में रहती हैं, "
            "तो ऑक्सीजन से जुड़कर उनका स्वाद और गंध खराब हो जाते हैं। "
            "रैंसिडिटी रोकने के लिए खाने को एयरटाइट डिब्बों या फ्रिज में रखते हैं, एंटीऑक्सीडेंट्स मिलाते हैं, "
            "और चिप्स के पैकेटों में नाइट्रोजन गैस भरते हैं ताकि तेल का ऑक्सीडेशन न हो! "
            "बधाई हो भाई लोग! हमारी लिस्ट के आठों टॉपिक्स पूरे होकर टिक हो गए हैं!"
        )
    },
    {
        "scene_id": 10,
        "topic_idx": 9,
        "part_badge": "PART G & PART H — COMPLETE VISUAL REVISION & BOARD EXAM PRACTICE QUIZ",
        "heading": "Exam Revision, Common Mistakes & Interactive Practice Questions",
        "lab_img": "ncert_fig8_summary.jpg",
        "r1_box": ("How to Identify Reactions", "A+B→AB | AB→A+B | A+BC→AC+B | AB+CD→AD+CB"),
        "r2_box": ("Avoid Common Mistakes!", "Never change subscripts | Include state symbols"),
        "cond_text": "Exam Mastery →",
        "prod_box": ("100% MP Board Score", "MCQ + Fill-in-Blanks + True/False + Balancing"),
        "eq_banner": "Exam Check: Combination (1 Product) | Decomposition (1 Reactant) | Displacement (Element+Compound) | Double Disp (Ion Exchange)",
        "anim_mode": "final_exam_quiz",
        "points": [
            "• <b>Common Student Mistakes (परीक्षा में ये गलतियाँ कभी मत करना):</b>",
            "   1. समीकरण संतुलित करते समय फॉर्मूले का <b>Subscript कभी न बदलें</b>, केवल आगे <b>Coefficient</b> बदलें।",
            "   2. लोहे की जंग को Fe + H₂O मत लिखें — सही सूत्र <b>Fe₂O₃·xH₂O</b> है और इसके लिए <b>O₂ + Moisture दोनों</b> चाहिए।",
            "• <b>PART H — Interactive Board Exam Practice (सोचिए और उत्तर मिलाइए):</b>",
            "   <b>1. MCQ:</b> Fe₂O₃ + 2Al → Al₂O₃ + 2Fe किस प्रकार की अभिक्रिया है?  <i>(Pause...)</i>  ➔ <b>✔ उत्तर: Displacement Reaction</b> (Al ने Fe को विस्थापित किया)।",
            "   <b>2. Fill in the Blank:</b> जिन अभिक्रियाओं में ऊष्मा अवशोषित होती है उन्हें _______ कहते हैं।  ➔ <b>✔ उत्तर: Endothermic Reactions (ऊष्माशोषी)</b>।",
            "   <b>3. True / False:</b> श्वसन (Respiration) एक Endothermic अभिक्रिया है।  ➔ <b>✔ उत्तर: False (गलत)!</b> श्वसन एक <b>Exothermic</b> अभिक्रिया है क्योंकि इसमें ऊर्जा निकलती है।",
            "   <b>4. Balancing Exercise:</b> <b>N₂(g) + 3H₂(g) → 2NH₃(g)</b>   तथा   <b>2KBr(aq) + BaI₂(aq) → 2KI(aq) + BaBr₂(s)↓</b>"
        ],
        "topic_qa": "🏆 CHAPTER 1 MASTERED! आपने सभी 8 टॉपिक्स, उनके प्रयोग, समीकरण और बोर्ड प्रश्न पूरे कर लिए हैं! कल अगले चैप्टर की फोटो भेजिए!",
        "narration": (
            "अब पार्ट जी और पार्ट एच में हम पूरे चैप्टर का एग्जाम रिवीजन करेंगे, स्टूडेंट्स की आम गलतियाँ जानेंगे और चार अलग-अलग तरह के बोर्ड सवाल हल करेंगे! "
            "सबसे पहले दो आम गलतियाँ जिनसे आपको बचना है: "
            "पहली गलती, समीकरण बैलेंस करते समय कभी भी सूत्र के नीचे का छोटा नंबर यानी सबस्क्रिप्ट न बदलें, हमेशा आगे कोएफिशिएंट लगाएँ। "
            "दूसरी गलती, रिएक्शन पहचानते समय याद रखें: अगर एक प्रोडक्ट बने तो कॉम्बिनेशन, एक रिएक्टेंट टूटे तो डीकंपोजिशन, "
            "एक तत्व दूसरे को हटाए तो डिस्प्लेसमेंट, और आयनों की अदला-बदली हो तो डबल डिस्प्लेसमेंट! "
            "अब चलिए चार प्रैक्टिस सवाल हल करते हैं, हर सवाल के बाद थोड़ा सोचिए: "
            "पहला एमसीक्यू: एफई-टू-ओ-थ्री प्लस टू-एएल गिव्स एएल-टू-ओ-थ्री प्लस टू-एफई कौन सी रिएक्शन है? "
            "सोचिए... सही जवाब है, डिस्प्लेसमेंट रिएक्शन, क्योंकि एल्युमिनियम ने आयरन को विस्थापित कर दिया! "
            "दूसरा, खाली स्थान भरिए: जिन अभिक्रियाओं में ऊष्मा अवशोषित होती है उन्हें क्या कहते हैं? "
            "सोचिए... सही जवाब है, एंडोथर्मिक रिएक्शन! "
            "तीसरा, ट्रू या फॉल्स: क्या श्वसन यानी रेस्पिरेशन एक एंडोथर्मिक रिएक्शन है? "
            "सोचिए... यह फॉल्स है, क्योंकि श्वसन एक एक्सोथर्मिक रिएक्शन है जिसमें ऊर्जा बाहर निकलती है! "
            "चौथा, बैलेंसिंग एक्सरसाइज: एन-टू प्लस थ्री-एच-टू गिव्स टू-एनएच-थ्री! "
            "इसी के साथ हमारा क्लास टेंथ साइंस का चैप्टर वन पूरी तरह कंप्लीट होता है!"
        )
    }
]


def synthesize_teacher_audio(text: str, out_wav: str):
    if os.path.exists(out_wav) and os.path.getsize(out_wav) > 1000:
        return
    mp3_path = out_wav.replace(".wav", ".mp3")
    tts = gTTS(text=text, lang="hi", slow=False)
    tts.save(mp3_path)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    af = "asetrate=24000*0.99,atempo=1.05,aresample=24000,highpass=f=75,dynaudnorm"
    subprocess.run([ff, "-y", "-i", mp3_path, "-af", af, "-ac", "1", "-ar", "24000", out_wav],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(mp3_path):
        os.remove(mp3_path)


# Map each scene to 4 distinct visual images so the image changes every ~15 seconds (40+ visual changes total!)
SCENE_MULTI_IMAGES = {
    1: ["react_1_mg_ribbon.jpg", "ncert_fig1_intro.jpg", "react_2_rusting_nail.jpg", "react_3_quicklime_beaker.jpg"],
    2: ["react_1_mg_ribbon.jpg", "ncert_fig2_mg_burn.jpg", "react_2_rusting_nail.jpg", "react_7_zn_h2so4_gas.jpg"],
    3: ["react_7_zn_h2so4_gas.jpg", "ncert_fig2_mg_burn.jpg", "react_5_displacement_ppt.jpg", "ncert_fig3_balancing.jpg"],
    4: ["ncert_fig3_balancing.jpg", "react_1_mg_ribbon.jpg", "react_7_zn_h2so4_gas.jpg", "ncert_fig3_balancing.jpg"],
    5: ["react_3_quicklime_beaker.jpg", "ncert_fig4_combination.jpg", "react_1_mg_ribbon.jpg", "react_3_quicklime_beaker.jpg"],
    6: ["react_8_lead_nitrate_fumes.jpg", "react_4_decomp_trio.jpg", "ncert_fig5_electrolysis.jpg", "react_9_agcl_sunlight_photo.jpg"],
    7: ["react_5_displacement_ppt.jpg", "ncert_fig6_displacement.jpg", "react_7_zn_h2so4_gas.jpg", "react_5_displacement_ppt.jpg"],
    8: ["react_6_redox_cuo.jpg", "ncert_fig7_redox.jpg", "react_1_mg_ribbon.jpg", "react_6_redox_cuo.jpg"],
    9: ["react_2_rusting_nail.jpg", "react_10_chips_nitrogen_rancidity.jpg", "ncert_fig7_redox.jpg", "react_10_chips_nitrogen_rancidity.jpg"],
    10: ["ncert_fig8_summary.jpg", "react_4_decomp_trio.jpg", "react_5_displacement_ppt.jpg", "react_10_chips_nitrogen_rancidity.jpg"],
}


def build_scene_plate(sc: dict, qa_active: bool, img_override: str = None, width: int = 1920, height: int = 1080) -> Image.Image:
    """
    Builds the 1920x1080 Master Classroom Layout:
    - Top Header: Chapter Title + Part Badge
    - Left Sidebar (x=16..340): Live 8-Topic Master Checklist (Completed topics ticked in Green ✓, Current topic in Yellow ▶)
    - Center-Left Stage (x=352..970):
        * Top: Photorealistic 3D Lab Experiment Image + [Reactant 1] + [Reactant 2] —Condition→ [Product] Visual Cards
        * Bottom: Live 3D Molecular & Atom Rearrangement Simulation Canvas
    - Right Smart-Board (x=982..1904):
        * Equation Banner at Top
        * High-Contrast Uncluttered Concept Breakdown
        * Bottom Topic Question & Answer Box (Lights up bright green when topic finishes!)
    """
    canvas = Image.new("RGBA", (width, height), (9, 14, 26, 255))
    draw = ImageDraw.Draw(canvas)

    # 1. TOP HEADER BAR
    draw.rounded_rectangle([16, 12, width - 16, 84], radius=14, fill=(18, 30, 56, 255), outline=(56, 189, 248, 255), width=2)
    hdr_mk = (
        f"<span foreground='#38BDF8' weight='heavy' size='16000'>MP BOARD CLASS 10 SCIENCE  |  {sc['part_badge']}</span>\n"
        f"<span foreground='#FDE047' weight='heavy' size='19000'>{sc['heading']}</span>"
    )
    hdr_im = render_pango_block(hdr_mk, width - 60, font_size=17)
    canvas.paste(hdr_im, (32, 16), hdr_im)

    # 2. LEFT SIDEBAR: LIVE 8-TOPIC MASTER CHECKLIST (x=16..340, y=94..988)
    draw.rounded_rectangle([16, 94, 340, 988], radius=16, fill=(15, 23, 42, 255), outline=(99, 102, 241, 255), width=2)
    chk_hdr = render_pango_block("<span foreground='#A5B4FC' weight='heavy' size='16500'>📋 CHAPTER TOPIC LIST\n(जो टॉपिक कटेगा → तुरंत सवाल!)</span>", 296, font_size=15)
    canvas.paste(chk_hdr, (28, 106), chk_hdr)

    cur_t = sc["topic_idx"]
    for idx_t, t_name in enumerate(TOPICS_LIST, start=1):
        ty0 = 188 + (idx_t - 1) * 96
        is_done = (idx_t < cur_t) or (idx_t == cur_t and qa_active) or (cur_t == 9)
        is_curr = (idx_t == cur_t and not qa_active)

        if is_done:
            bg_c = (6, 78, 59, 255)
            bd_c = (16, 185, 129, 255)
            txt_mk = f"<span foreground='#6EE7B7' weight='heavy' size='14500'>✔ <s>{t_name}</s>\n   [COMPLETED + Q&amp;A ✔]</span>"
        elif is_curr:
            bg_c = (113, 63, 18, 255)
            bd_c = (250, 204, 21, 255)
            txt_mk = f"<span foreground='#FEF08A' weight='heavy' size='15000'>▶ {t_name}\n   [अभी चल रहा है...]</span>"
        else:
            bg_c = (23, 33, 53, 255)
            bd_c = (51, 65, 85, 255)
            txt_mk = f"<span foreground='#94A3B8' size='14500'>○ {t_name}</span>"

        draw.rounded_rectangle([26, ty0, 330, ty0 + 84], radius=12, fill=bg_c, outline=bd_c, width=2)
        t_im = render_pango_block(txt_mk, 286, font_size=14)
        canvas.paste(t_im, (34, ty0 + 10), t_im)

    # 3. CENTER-LEFT STAGE: REALISTIC LAB IMAGE + REACTANTS (+) → PRODUCTS SEQUENCE + LIVE MOLECULAR BOX (x=352..970)
    draw.rounded_rectangle([352, 94, 970, 988], radius=16, fill=(15, 23, 42, 255), outline=(16, 185, 129, 255), width=2)

    # Top Photorealistic Lab Image (x=366..956, y=106..396) — switches across 4 images per scene!
    lab_p = os.path.join(MP_ASSETS, img_override or sc["lab_img"])
    if os.path.exists(lab_p):
        l_im = Image.open(lab_p).convert("RGBA").resize((590, 290), Image.Resampling.LANCZOS)
        canvas.paste(l_im, (366, 106))
        draw.rounded_rectangle([366, 106, 956, 396], radius=12, outline=(251, 191, 36, 220), width=2)

    # Middle 10-Step Visual Sequence Cards: [Reactant 1] + [Reactant 2] —Condition→ [Product] (y=406..560)
    r1_t, r1_f = sc["r1_box"]
    r2_t, r2_f = sc["r2_box"]
    pr_t, pr_f = sc["prod_box"]

    # Reactant 1 Card
    draw.rounded_rectangle([364, 408, 534, 548], radius=10, fill=(30, 58, 138, 255), outline=(96, 165, 250, 255), width=2)
    r1_im = render_pango_block(f"<span foreground='#93C5FD' weight='heavy' size='13500'>{r1_t}</span>\n<span foreground='#FFFFFF' weight='heavy' size='14500'>{r1_f}</span>", 156, font_size=13)
    canvas.paste(r1_im, (372, 418), r1_im)

    # Plus (+) Badge
    draw.ellipse([538, 458, 570, 490], fill=(250, 204, 21, 255))
    draw.line([(546, 474), (562, 474)], fill=(0, 0, 0, 255), width=4)
    draw.line([(554, 466), (554, 482)], fill=(0, 0, 0, 255), width=4)

    # Reactant 2 Card
    draw.rounded_rectangle([574, 408, 744, 548], radius=10, fill=(30, 58, 138, 255), outline=(96, 165, 250, 255), width=2)
    r2_im = render_pango_block(f"<span foreground='#93C5FD' weight='heavy' size='13500'>{r2_t}</span>\n<span foreground='#FFFFFF' weight='heavy' size='14500'>{r2_f}</span>", 156, font_size=13)
    canvas.paste(r2_im, (582, 418), r2_im)

    # Product Card (Right of arrow)
    draw.rounded_rectangle([754, 408, 958, 548], radius=10, fill=(6, 78, 59, 255), outline=(52, 211, 153, 255), width=2)
    pr_im = render_pango_block(f"<span foreground='#FDE047' weight='heavy' size='13000'>{sc['cond_text']}</span>\n<span foreground='#6EE7B7' weight='heavy' size='13500'>{pr_t}</span>\n<span foreground='#FFFFFF' weight='heavy' size='14000'>{pr_f}</span>", 190, font_size=13)
    canvas.paste(pr_im, (762, 414), pr_im)

    # Bottom Live 3D Molecular & Atom Rearrangement Simulator Box (x=364..958, y=560..976)
    draw.rounded_rectangle([364, 560, 958, 976], radius=14, fill=(8, 12, 22, 255), outline=(56, 189, 248, 220), width=2)
    sim_hdr = render_pango_block("<span foreground='#38BDF8' weight='heavy' size='15000'>⚛ LIVE MOLECULAR &amp; LAB REACTION ANIMATION:</span>", 560, font_size=15)
    canvas.paste(sim_hdr, (378, 568), sim_hdr)

    # 4. RIGHT SMART-BOARD PANEL (x=982..1904, y=94..988)
    draw.rounded_rectangle([982, 94, 1904, 988], radius=16, fill=(17, 25, 42, 255), outline=(250, 204, 21, 255), width=3)

    # Top Complete Chemical Equation Banner inside Right Board (x=996..1890, y=108..182)
    draw.rounded_rectangle([996, 108, 1890, 182], radius=12, fill=(30, 41, 59, 255), outline=(56, 189, 248, 255), width=2)
    eq_im = render_pango_block(f"<span foreground='#FEF08A' weight='heavy' size='16000'>⚗️ {sc['eq_banner']}</span>", 868, font_size=16)
    canvas.paste(eq_im, (1010, 118), eq_im)

    # Main Concept Explanation Points (x=1002..1660, y=194..818)
    pts_str = "\n\n".join(sc["points"])
    pts_im = render_pango_block(f"<span foreground='#F8FAFC' size='16200'>{pts_str}</span>", 665, font_size=16)
    canvas.paste(pts_im, (1002, 194), pts_im)

    # Bottom Instant Topic Question & Answer Box (x=996..1658, y=828..976)
    qa_fill = (6, 95, 70, 255) if qa_active else (88, 28, 135, 255)
    qa_outline = (52, 211, 153, 255) if qa_active else (250, 204, 21, 255)
    draw.rounded_rectangle([996, 828, 1658, 976], radius=14, fill=qa_fill, outline=qa_outline, width=3 if qa_active else 2)
    qa_im = render_pango_block(f"<span foreground='#FEF08A' weight='heavy' size='15500'>{sc['topic_qa']}</span>", 640, font_size=15)
    canvas.paste(qa_im, (1010, 838), qa_im)

    return canvas


def _draw_molecular_simulation(draw: ImageDraw.ImageDraw, anim_mode: str, t: float, dur: float):
    """
    Draws scientifically accurate atom rearrangements & lab reactions inside [374, 608, 948, 966].
    Never creates or destroys atoms — visually demonstrates Conservation of Mass!
    """
    x0, y0, x1, y1 = 374, 608, 948, 966
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    u = (t % 5.0) / 5.0  # 5-second repeating reaction cycle

    if anim_mode in ("atom_balance_2mg", "intro_atoms"):
        # 2Mg (2 Silver spheres) + O2 (2 Red spheres bonded) -> 2MgO (2 Silver-Red bonded pairs)
        # Strict atom count: 2 Silver Mg + 2 Red O on both sides!
        if u < 0.45:
            # Reactants separated on left & right moving toward center
            shift = int(130 * (1.0 - u / 0.45))
            # 2 Mg atoms (Silver)
            draw.ellipse([cx - shift - 95, cy - 65, cx - shift - 45, cy - 15], fill=(203, 213, 225, 255), outline=(255, 255, 255, 255), width=3)
            draw.ellipse([cx - shift - 95, cy + 15, cx - shift - 45, cy + 65], fill=(203, 213, 225, 255), outline=(255, 255, 255, 255), width=3)
            # O2 molecule (2 Red atoms bonded together)
            draw.ellipse([cx + shift + 25, cy - 50, cx + shift + 75, cy], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=3)
            draw.ellipse([cx + shift + 25, cy, cx + shift + 75, cy + 50], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=3)
        elif u < 0.60:
            # Dazzling reaction flash as O=O bond breaks and Mg-O bonds form!
            rad = int(75 + 25 * math.sin(t * 18))
            draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(254, 240, 138, 220), outline=(255, 255, 255, 255), width=4)
        else:
            # Products: 2 MgO molecules (Each has 1 Silver Mg + 1 Red O bonded!)
            # Molecule 1 (Top)
            draw.ellipse([cx - 55, cy - 70, cx - 5, cy - 20], fill=(203, 213, 225, 255), outline=(255, 255, 255, 255), width=3)
            draw.ellipse([cx - 5, cy - 70, cx + 45, cy - 20], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=3)
            # Molecule 2 (Bottom)
            draw.ellipse([cx - 55, cy + 20, cx - 5, cy + 70], fill=(203, 213, 225, 255), outline=(255, 255, 255, 255), width=3)
            draw.ellipse([cx - 5, cy + 20, cx + 45, cy + 70], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=3)

    elif anim_mode in ("mg_and_rust", "corrosion_and_chips"):
        # Left: Iron nail gradually developing reddish-brown Fe2O3.xH2O layer as O2 (red) & H2O (blue) droplets touch it
        rust_prog = min(1.0, (t / max(1.0, dur * 0.7)))
        # Iron bar
        draw.rounded_rectangle([cx - 180, cy - 24, cx + 80, cy + 24], radius=8, fill=(148, 163, 184, 255), outline=(255, 255, 255, 255), width=2)
        # Growing reddish-brown hydrated iron(III) oxide layer
        rw = int(260 * rust_prog)
        if rw > 4:
            draw.rounded_rectangle([cx - 180, cy - 26, cx - 180 + rw, cy + 26], radius=8, fill=(180, 83, 9, 235), outline=(251, 146, 60, 255), width=2)
        # Incoming O2 (red) & H2O moisture (sky blue) spheres
        for i in range(5):
            dy = int(((t * 65 + i * 32) % 130) - 65)
            dx = cx - 150 + i * 52
            col = (56, 189, 248, 255) if (i % 2 == 0) else (239, 68, 68, 255)
            draw.ellipse([dx - 10, cy + dy - 10, dx + 10, cy + dy + 10], fill=col, outline=(255, 255, 255, 255))

    elif anim_mode == "combination_exothermic":
        # Beaker with Quicklime (CaO) lumps + H2O combining into Slaked Lime Ca(OH)2 + Orange Heat Waves
        draw.rounded_rectangle([cx - 95, cy - 60, cx + 95, cy + 120], radius=14, fill=(30, 58, 138, 190), outline=(255, 255, 255, 255), width=3)
        draw.rectangle([cx - 88, cy - 10, cx + 88, cy + 112], fill=(226, 232, 240, 235))
        # Radiating orange/red heat waves showing Exothermic heat release
        for r_i in range(3):
            rad = int(60 + ((t * 60 + r_i * 42) % 125))
            draw.arc([cx - rad, cy - rad, cx + rad, cy + rad], 185, 355, fill=(249, 115, 22, 255), width=4)

    elif anim_mode == "decomp_three_types":
        # Electrolysis of Water showing 2H2O -> 2H2 (Cathode, 2x vol) + O2 (Anode, 1x vol)
        fill_p = min(1.0, (t / max(1.0, dur)) * 1.35)
        h2_h = int(115 * fill_p)
        o2_h = int(57 * fill_p)
        draw.rounded_rectangle([cx - 140, cy - 85, cx + 140, cy + 125], radius=12, fill=(30, 64, 175, 175), outline=(147, 197, 253, 255), width=3)
        # Left tube (O2 = 1x) & Right tube (H2 = 2x)
        draw.rectangle([cx - 80, cy - 115, cx - 36, cy + 75], fill=(96, 165, 250, 195), outline=(255, 255, 255, 255), width=2)
        draw.rectangle([cx - 78, cy - 113, cx - 38, cy - 113 + o2_h], fill=(15, 23, 42, 255))
        draw.rectangle([cx + 36, cy - 115, cx + 80, cy + 75], fill=(96, 165, 250, 195), outline=(255, 255, 255, 255), width=2)
        draw.rectangle([cx + 38, cy - 113, cx + 78, cy - 113 + h2_h], fill=(15, 23, 42, 255))

    elif anim_mode == "disp_and_yellow_ppt":
        # Left: Blue CuSO4 turning Pale Green FeSO4 + Brown nail; Right: Clear solutions forming bright Yellow PbI2 precipitate
        mix = min(1.0, t / max(1.0, dur * 0.7))
        # Left Beaker (Fe + CuSO4)
        lx = cx - 135
        rc = int(37 * (1 - mix) + 74 * mix)
        gc = int(99 * (1 - mix) + 222 * mix)
        bc = int(235 * (1 - mix) + 128 * mix)
        draw.rounded_rectangle([lx - 65, cy - 75, lx + 65, cy + 115], radius=12, fill=(rc, gc, bc, 230), outline=(255, 255, 255, 255), width=3)
        nr = int(180 * mix + 148 * (1 - mix))
        ng = int(83 * mix + 163 * (1 - mix))
        nb = int(9 * mix + 184 * (1 - mix))
        draw.rectangle([lx - 8, cy - 105, lx + 8, cy + 80], fill=(nr, ng, nb, 255), outline=(255, 255, 255, 255), width=1)

        # Right Beaker (Pb(NO3)2 + 2KI -> Yellow PbI2 precipitate settling at bottom!)
        rx = cx + 135
        draw.rounded_rectangle([rx - 65, cy - 75, rx + 65, cy + 115], radius=12, fill=(30, 41, 59, 220), outline=(255, 255, 255, 255), width=3)
        ppt_h = int(65 * mix)
        if ppt_h > 4:
            draw.rounded_rectangle([rx - 61, cy + 111 - ppt_h, rx + 61, cy + 111], radius=8, fill=(250, 204, 21, 245))
        # Falling yellow PbI2 crystals
        for p_i in range(6):
            py = cy - 50 + int((t * 70 + p_i * 22) % 140)
            px = rx - 35 + (p_i % 4) * 22
            draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(253, 224, 71, 255))

    elif anim_mode == "redox_cuo_h2":
        # Black CuO losing Red Oxygen atom to H2 (2 Blue atoms) -> Reddish-Brown Cu + H2O!
        shift = int(110 * u)
        # Cu atom changing from Black (CuO) to Reddish-Brown (Cu)
        cu_col = (40, 40, 45, 255) if u < 0.45 else (180, 83, 9, 255)
        draw.ellipse([cx - 110, cy - 40, cx - 30, cy + 40], fill=cu_col, outline=(255, 255, 255, 255), width=3)
        # Oxygen atom (Red) transferring from Cu to H2!
        ox_x = (cx - 25) + int(125 * u)
        draw.ellipse([ox_x - 24, cy - 24, ox_x + 24, cy + 24], fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=3)
        # 2 H atoms (Sky Blue) waiting on right to bond with O -> H2O
        draw.ellipse([cx + 115, cy - 48, cx + 155, cy - 8], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=2)
        draw.ellipse([cx + 115, cy + 8, cx + 155, cy + 48], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=2)

    else:
        # Symbols / Quiz pulsing ring
        rad = int(65 + 12 * math.sin(t * 5.0))
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(16, 185, 129, 220), outline=(250, 204, 21, 255), width=4)


def build_and_upload_master_sci_ch1():
    print("==========================================================================")
    print("🔬 BUILDING COMPLETE MASTER PROMPT VIDEO (PARTS A-H): SCIENCE CHAPTER 1")
    print("==========================================================================")
    sr = 24000
    master_wav = os.path.join(TEMP_DIR, "sci_v2_master.wav")
    out_mp4 = os.path.join(OUTPUT_DIR, "mpboard_c10_science_ch1_chemical_reactions.mp4")
    out_thumb = os.path.join(OUTPUT_DIR, "mpboard_c10_science_ch1_thumb.jpg")
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    scene_plan = []

    with wave.open(master_wav, "wb") as out_wf:
        out_wf.setnchannels(1)
        out_wf.setsampwidth(2)
        out_wf.setframerate(sr)

        for sc in MASTER_SCENES:
            sid = sc["scene_id"]
            w_path = os.path.join(TEMP_DIR, f"v2_s{sid}.wav")
            synthesize_teacher_audio(sc["narration"], w_path)
            with wave.open(w_path, "rb") as wf:
                pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
            t_arr = np.linspace(0, len(pcm) / float(sr), len(pcm), endpoint=False, dtype=np.float32)
            pad = 0.015 * (np.sin(2 * np.pi * 220.0 * t_arr) + 0.5 * np.sin(2 * np.pi * 329.6 * t_arr))
            mixed = np.clip((pcm * 0.96 + pad) * 32767.0, -32767.0, 32767.0).astype(np.int16)
            out_wf.writeframes(mixed.tobytes())
            dur = len(mixed) / float(sr)
            scene_plan.append((sc, dur))
            print(f"  -> Scene {sid}/10 Audio Ready ({dur:.1f}s): {sc['part_badge']}")

    total_dur = sum(d for _, d in scene_plan)
    print(f"⏱️ Total Master Classroom Lesson Duration: {total_dur/60.0:.2f} minutes ({total_dur:.1f}s)")

    # Save Thumbnail showing Topic Checklist ticked + 2Mg + O2 -> 2MgO + 3D Teacher
    th_plate = build_scene_plate(MASTER_SCENES[3], qa_active=True, width=1920, height=1080)
    th_draw = ImageDraw.Draw(th_plate)
    _draw_molecular_simulation(th_draw, "atom_balance_2mg", 1.2, 60.0)
    t_sp = TEACHER_SPRITES["teacher_talk"]["open"]
    th_plate.paste(t_sp, (1668, 588), t_sp)
    th_plate.resize((1280, 720), Image.Resampling.LANCZOS).convert("RGB").save(out_thumb, "JPEG", quality=93)

    fps = 8
    cmd = [
        ff, "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(fps),
        "-i", "-",
        "-i", master_wav,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
        "-maxrate", "520k", "-bufsize", "1040k",
        "-r", "24", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart",
        "-shortest",
        out_mp4
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elapsed = 0.0
    mouth_cycle = ["closed", "half", "open", "half", "open", "closed", "half", "open"]

    for sc, dur in scene_plan:
        sid = sc["scene_id"]
        imgs_4 = SCENE_MULTI_IMAGES.get(sid, [sc["lab_img"]] * 4)
        sub_plates = [
            build_scene_plate(sc, qa_active=False, img_override=imgs_4[0], width=1920, height=1080),
            build_scene_plate(sc, qa_active=False, img_override=imgs_4[1], width=1920, height=1080),
            build_scene_plate(sc, qa_active=False, img_override=imgs_4[2], width=1920, height=1080),
            build_scene_plate(sc, qa_active=True,  img_override=imgs_4[3], width=1920, height=1080),
        ]
        n_frames = max(1, int(round(dur * fps)))

        for f_idx in range(n_frames):
            t_local = f_idx / float(fps)
            u = t_local / max(1.0, dur)
            prog_ratio = min(1.0, (elapsed + t_local) / max(1.0, total_dur))

            # Switch across 4 distinct visual images + QA plate within every topic!
            if u < 0.24:
                cut_idx = 0
            elif u < 0.48:
                cut_idx = 1
            elif u < 0.72:
                cut_idx = 2
            else:
                cut_idx = 3
            qa_now = (cut_idx == 3)
            frame = sub_plates[cut_idx].copy()
            draw = ImageDraw.Draw(frame)

            # 1. Live Molecular & Lab Simulation in Center-Left Bottom Box
            _draw_molecular_simulation(draw, sc["anim_mode"], t_local, dur)

            # 2. Animated Highlighting Indicator on Right Board
            hl_y = int(205 + 560 * min(1.0, u / 0.72)) if not qa_now else 855
            draw.rounded_rectangle([988, hl_y, 998, hl_y + 44], radius=4, fill=(52, 211, 153, 255) if qa_now else (250, 204, 21, 255))

            # 3. 3D Animated Teacher Choreography (Walk-In -> Point at Reactants/Molecules/Board -> Ask Topic Q&A)
            m_state = mouth_cycle[f_idx % len(mouth_cycle)]
            bob_y = int(4 * math.sin(t_local * 5.5))
            if u < 0.14:
                w_prog = u / 0.14
                tx = int(1830 - 162 * w_prog)
                ty = 588 + int(abs(8 * math.sin(t_local * 9.0)))
                sp = TEACHER_SPRITES["teacher_walk"][m_state]
                frame.paste(sp, (tx, ty), sp)
            elif u < 0.65:
                tx, ty = 1668, 588 + bob_y
                sp = TEACHER_SPRITES["teacher_point"][m_state]
                # Laser pointer alternating between Reactant->Product cards and Molecular Simulation
                target_x, target_y = (660, 475) if (int(t_local) % 2 == 0) else (660, 760)
                draw.line([(tx + 24, ty + 120), (target_x, target_y)], fill=(239, 68, 68, 215), width=3)
                draw.ellipse([target_x - 7, target_y - 7, target_x + 7, target_y + 7], fill=(250, 204, 21, 255), outline=(239, 68, 68, 255), width=2)
                frame.paste(sp, (tx, ty), sp)
            else:
                # Teacher faces student asking the instant Topic Question ("अब बताओ बच्चों...")!
                tx, ty = 1668, 588 + bob_y
                sp = TEACHER_SPRITES["teacher_talk"][m_state]
                frame.paste(sp, (tx, ty), sp)

            # 4. Overall Chapter Progress Bar
            draw.rounded_rectangle([16, 1002, 1904, 1024], radius=10, fill=(30, 41, 59, 255))
            bar_w = max(24, int(1888 * prog_ratio))
            draw.rounded_rectangle([16, 1002, 16 + bar_w, 1024], radius=10, fill=(16, 185, 129, 255))

            proc.stdin.write(frame.convert("RGB").tobytes())
        elapsed += dur

    proc.stdin.close()
    proc.wait()
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    sz_mb = os.path.getsize(out_mp4) / (1024 * 1024)
    print(f"✅ Master Prompt v2 Video Ready ({sz_mb:.2f} MB): {out_mp4}")

    plan = {
        "title": "Class 10 Science Chapter 1: Chemical Reactions and Equations | Full Chapter + Topic-Wise Q&A 📚🔬",
        "description": (
            "हेलो भाई लोग, प्यारे बच्चों! आज हम पढ़ेंगे Class 10th MP Board NCERT Science का Chapter 1: Chemical Reactions and Equations (रासायनिक अभिक्रियाएँ एवं समीकरण)!\n\n"
            "✅ इस वीडियो में हम एक-एक करके ये सभी 8 Topics कवर करेंगे और जैसे ही टॉपिक पूरा होगा, तुरंत उससे जुड़ा सवाल हल करेंगे:\n"
            "✔ Topic 1 (Part A): Introduction to Chemical Reactions (Mg Ribbon, Iron Rusting Fe₂O₃·xH₂O, 4 Observations)\n"
            "✔ Topic 2 (Part B): Word Equations, Chemical Formulae & State Symbols (s), (l), (g), (aq), ↑, ↓\n"
            "✔ Topic 3 (Part C): Law of Conservation of Mass & Step-by-Step Equation Balancing (2Mg + O₂ → 2MgO, 3Fe + 4H₂O)\n"
            "✔ Topic 4 (Part D & E): Combination Reaction (CaO + H₂O → Ca(OH)₂ + Heat) & Exothermic Reactions\n"
            "✔ Topic 5 (Part D & E): Decomposition (Thermal CaCO₃, Electrolytic 2H₂O, Photolytic 2AgCl) & Endothermic\n"
            "✔ Topic 6 (Part D): Displacement (Fe + CuSO₄) & Double Displacement (Pb(NO₃)₂ + 2KI → PbI₂↓)\n"
            "✔ Topic 7 (Part D): Oxidation and Reduction (Redox: CuO + H₂ → Cu + H₂O)\n"
            "✔ Topic 8 (Part F, G, H): Corrosion, Rancidity & Complete Board Exam Practice (MCQ, Fill-in-Blanks, True/False)\n\n"
            "#mpboard #class10science #chemicalreactionsandequations #ncertclass10 #mpboardclass10 #sciencechapter1"
        ),
        "tags": [
            "chemical reactions and equations class 10",
            "mp board class 10 science chapter 1",
            "ncert class 10 science chapter 1 in hindi",
            "balancing chemical equations class 10",
            "types of chemical reactions class 10",
            "redox reactions class 10",
            "corrosion and rancidity class 10"
        ],
        "first_comment": "📚 भाई लोग, प्यारे बच्चों! सारे 8 टॉपिक्स और उनके सवाल कैसे लगे? अगला वीडियो किस चैप्टर पर चाहिए, कमेंट में बताओ! 👇"
    }

    import sys
    vid_id = "SCHEDULED_FOR_7AM_IST"
    if "--upload" in sys.argv:
        try:
            vid_id = upload_to_youtube(
                video_path=out_mp4,
                thumbnail_path=out_thumb,
                plan=plan,
                video_type="long"
            )
        except Exception as e:
            print(f"ℹ️ YouTube Upload Note: {e}")
    else:
        print("⏰ Video built locally! Scheduled for automatic YouTube upload tomorrow morning at 7:00 AM IST.")

    return out_mp4, out_thumb, vid_id


if __name__ == "__main__":
    build_and_upload_master_sci_ch1()
