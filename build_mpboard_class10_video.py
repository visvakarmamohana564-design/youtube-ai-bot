"""
MP BOARD CLASS 10th NCERT CHAPTER READER & DEEP EXPLAINER ENGINE
================================================================
Subject: कक्षा 10वीं हिंदी (क्षितिज भाग-2) — गद्य खंड
Chapter: नेताजी का चश्मा (लेखक: स्वयं प्रकाश)
Method:
  1. मूल पाठ वाचन (Reads the actual NCERT Chapter Passage aloud with on-screen book text)
  2. अंदर की बातों की सरल व्याख्या (Explains the deeper meaning, hidden satire, character psychology,
     word meanings, and MP Board Exam key takeaways in simple conversational Hindi)
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MP_ASSETS = os.path.join(BASE_DIR, "assets", "mpboard_c10")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = "/tmp/mpboard_build"

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


def render_pango_block(markup_text: str, width_px: int, font_size: int = 20) -> Image.Image:
    """Renders multi-line Pango markup with 100% accurate Hindi Devanagari shaping and exact pixel width."""
    pango_bin = "/usr/bin/pango-view"
    pango_pts = int(width_px * 0.71)
    out_png = os.path.join(TEMP_DIR, f"pango_v3_{abs(hash((markup_text, pango_pts, font_size))) % 10000000}.png")
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


CHAPTER_SECTIONS = [
    {
        "sec_id": 1,
        "title": "भाग 1: कस्बे का परिचय और चौराहे पर नेताजी की मूर्ति",
        "img": "netaji_s1_statue.jpg",
        "book_heading": "★ NCERT मूल पाठ (गद्यांश 1):",
        "book_text": (
            "“हालदार साहब को हर पंद्रहवें दिन कंपनी के काम के सिलसिले में उस कस्बे से गुज़रना पड़ता था। "
            "कस्बा बहुत बड़ा नहीं था। इसी कस्बे के मुख्य बाज़ार के मुख्य चौराहे पर नेताजी सुभाषचंद्र बोस की एक "
            "संगमरमर की प्रतिमा लगी थी — टोपी की नोक से कोट के दूसरे बटन तक कोई दो फुट ऊँची। "
            "मूर्ति सुंदर थी, केवल एक चीज़ की कसर थी जो देखते ही खटकती थी — नेताजी की आँखों पर संगमरमर का चश्मा नहीं था। "
            "एक सामान्य और सचमुच के चश्मे का चौड़ा काला फ्रेम मूर्ति को पहना दिया गया था।”"
        ),
        "inside_heading": "★ अंदर की बातें और सरल व्याख्या (Deep Meaning):",
        "inside_points": [
            "• <b>कस्बे की स्थिति:</b> वह कोई बड़ा शहर नहीं बल्कि एक छोटा-सा कस्बा था जहाँ सीमित संसाधन थे, फिर भी नागरिकों में देशभक्ति की भावना थी।",
            "• <b>असली रहस्य (चश्मे की कसर):</b> स्कूल के ड्राइंग मास्टर मोतीलाल जी ने महीने भर में संगमरमर की सुंदर मूर्ति तो बना दी, पर बारीक पत्थर का चश्मा नहीं बन पाया।",
            "• <b>अंदर की मुख्य बात:</b> कस्बे के देशभक्त नागरिक को बिना चश्मे के नेताजी अधूरे लगे, इसलिए उसने मूर्ति पर <b>असली काला चश्मा</b> पहना दिया!",
            "• <b>कठिन शब्दार्थ:</b> कस्बा = छोटा शहर  |  बस्ट = छाती तक की आधी मूर्ति  |  कसर = कमी  |  खटकना = अधूरा लगना।"
        ],
        "exam_tip": "★ MP Board IMP प्रश्न: मूर्ति को देखकर हालदार साहब के चेहरे पर कौतुक भरी मुस्कान क्यों फैल गई?",
        "orig_durs": (52.5, 42.4),
        "read_audio": (
            "नमस्ते विद्यार्थियों! आज हम कक्षा दसवीं एमपी बोर्ड एनसीईआरटी हिंदी, क्षितिज भाग दो का सबसे महत्वपूर्ण अध्याय, "
            "नेताजी का चश्मा पढ़ेंगे और इसके अंदर की हर गहरी बात को सरल शब्दों में समझेंगे। "
            "चलिए सबसे पहले अध्याय का पहला गद्यांश पढ़ते हैं। "
            "हालदार साहब को हर पंद्रहवें दिन कंपनी के काम के सिलसिले में उस कस्बे से गुज़रना पड़ता था। "
            "कस्बा बहुत बड़ा नहीं था। इसी कस्बे के मुख्य बाज़ार के चौराहे पर नेताजी सुभाषचंद्र बोस की एक संगमरमर की मूर्ति लगी थी। "
            "मूर्ति सुंदर थी, केवल एक चीज़ की कसर थी जो देखते ही खटकती थी, नेताजी की आँखों पर संगमरमर का चश्मा नहीं था। "
            "बल्कि एक सचमुच के चश्मे का चौड़ा काला फ्रेम मूर्ति को पहना दिया गया था।"
        ),
        "explain_audio": (
            "अब आइए इस गद्यांश के अंदर की असली बात को समझते हैं। "
            "लेखक स्वयं प्रकाश जी यहाँ हमें दिखा रहे हैं कि कस्बा भले ही छोटा था और नगरपालिका के पास बजट कम था, "
            "लेकिन लोगों के दिल में सुभाषचंद्र बोस के लिए गहरा सम्मान था। "
            "जब स्थानीय स्कूल के ड्राइंग मास्टर मोतीलाल जी ने महीने भर में मूर्ति बनाई, तो पत्थर का बारीक चश्मा नहीं बन पाया। "
            "लेकिन कस्बे के नागरिकों ने मूर्ति को अधूरा नहीं छोड़ा, बल्कि उस पर असली चश्मा पहना दिया। "
            "हालदार साहब यह देखकर मुस्कुराए कि चलो, आज भी हमारे देश के लोगों में देशभक्ति की भावना ज़िंदा है।"
        )
    },
    {
        "sec_id": 2,
        "title": "भाग 2: मूर्ति पर बदलते चश्मों का रहस्य और पानवाले से बातचीत",
        "img": "netaji_s2_panwala.jpg",
        "book_heading": "★ NCERT मूल पाठ (गद्यांश 2):",
        "book_text": (
            "“दूसरी बार जब हालदार साहब उधर से गुज़रे तो उन्हें मूर्ति में कुछ अंतर दिखाई दिया। ध्यान से देखा तो पाया कि "
            "चश्मा दूसरा है। पहले मोटे फ्रेमवाला चौकोर चश्मा था, अब तार के फ्रेमवाला गोल चश्मा है। तीसरी बार फिर नया चश्मा था। "
            "एक बार जब कौतूहल दुर्दमनीय हो उठा तो पानवाले से ही पूछ लिया — क्यों भाई! क्या बात है? यह तुम्हारे नेताजी का चश्मा "
            "हर बार बदल कैसे जाता है? पानवाले ने मुँह का पान नीचे थूका और बोला — कैप्टन चश्मेवाला करता है।”"
        ),
        "inside_heading": "★ अंदर की बातें और सरल व्याख्या (Deep Meaning):",
        "inside_points": [
            "• <b>बदलते चश्मों का रहस्य:</b> पत्थर की मूर्ति कपड़े नहीं बदल सकती, लेकिन नेताजी की मूर्ति का चश्मा हर बार नया हो जाता था — कभी चौकोर, तो कभी गोल तार वाला!",
            "• <b>पानवाले का उत्तर:</b> चौराहे के खुशमिज़ाज पानवाले ने राज़ खोला कि यह काम <b>'कैप्टन चश्मेवाला'</b> करता है।",
            "• <b>अंदर की मुख्य बात:</b> कैप्टन एक गरीब फेरीवाला है जो चश्मे बेचता है। वह बिना चश्मे की मूर्ति देखकर आहत होता है, इसलिए अपने बेचने वाले फ्रेम मूर्ति को पहना देता है। ग्राहक माँगने पर वह नेताजी से माफ़ी माँगकर दूसरा फ्रेम लगा देता है!",
            "• <b>कठिन शब्दार्थ:</b> कौतूहल = जिज्ञासा  |  दुर्दमनीय = जिसे रोका न जा सके  |  आहत = दुखी  |  दरकार = आवश्यकता।"
        ],
        "exam_tip": "★ MP Board IMP प्रश्न: बार-बार मूर्ति का चश्मा क्यों बदल जाता था? अपने शब्दों में लिखिए।",
        "orig_durs": (37.8, 40.0),
        "read_audio": (
            "चलिए अब अध्याय का दूसरा भाग पढ़ते हैं। "
            "दूसरी बार जब हालदार साहब उधर से गुज़रे तो उन्हें मूर्ति में कुछ अंतर दिखाई दिया। "
            "ध्यान से देखा तो पाया कि चश्मा दूसरा है। पहले मोटे फ्रेमवाला चौकोर चश्मा था, अब तार के फ्रेमवाला गोल चश्मा है। "
            "तीसरी बार फिर नया चश्मा था। जब जिज्ञासा रोकी नहीं गई, तो हालदार साहब ने पानवाले से पूछ लिया, "
            "क्यों भाई, क्या बात है? यह तुम्हारे नेताजी का चश्मा हर बार बदल कैसे जाता है? "
            "पानवाले ने हँसकर बताया, कैप्टन चश्मेवाला करता है।"
        ),
        "explain_audio": (
            "अब इसके अंदर छिपी गहरी बात को समझिए। "
            "आखिर मूर्ति का चश्मा बार बार क्यों बदलता था? "
            "क्योंकि कैप्टन चश्मेवाला कोई अमीर आदमी नहीं था, उसके पास छोटी सी संदूकची और बाँस पर टँगे कुछ ही फ्रेम थे। "
            "वह देशभक्ति के कारण अपने बेचने वाले फ्रेम में से एक फ्रेम नेताजी की मूर्ति को पहना देता था। "
            "जब किसी ग्राहक को वही फ्रेम पसंद आ जाता, तो कैप्टन मन ही मन नेताजी से क्षमा माँगकर वह फ्रेम उतार लेता, "
            "और उसकी जगह दूसरा फ्रेम पहना देता! यानी वह अपनी गरीबी में भी देशभक्ति और रोज़ी रोटी दोनों निभा रहा था।"
        )
    },
    {
        "sec_id": 3,
        "title": "भाग 3: कैप्टन चश्मेवाला कौन था? (पानवाले का व्यंग्य और सच्चाई)",
        "img": "netaji_s3_captain.jpg",
        "book_heading": "★ NCERT मूल पाठ (गद्यांश 3):",
        "book_text": (
            "“हालदार साहब ने पानवाले से फिर पूछा — क्या कैप्टन चश्मेवाला नेताजी का साथी है? या आज़ाद हिंद फ़ौज का भूतपूर्व सिपाही? "
            "पानवाले ने मुस्कुराकर कहा — नहीं साब! वो लँगड़ा क्या जाएगा फ़ौज में। पागल है पागल! वो देखो, वो आ रहा है! "
            "हालदार साहब को पानवाले द्वारा एक देशभक्त का इस तरह मज़ाक उड़ाया जाना अच्छा नहीं लगा। मुड़कर देखा तो अवाक् रह गए — "
            "एक बेहद बूढ़ा मरियल-सा लँगड़ा आदमी सिर पर गांधी टोपी और आँखों पर काला चश्मा लगाए एक हाथ में छोटी-सी संदूकची "
            "और दूसरे हाथ में एक बाँस पर टँगे बहुत-से चश्मे लिए अभी-अभी एक गली से निकला था।”"
        ),
        "inside_heading": "★ अंदर की बातें और सरल व्याख्या (Deep Meaning):",
        "inside_points": [
            "• <b>कल्पना बनाम सच:</b> नाम 'कैप्टन' सुनकर हालदार साहब को लगा कि वह कोई रिटायर्ड फौजी होगा, पर वह एक बेहद बूढ़ा, गरीब और लँगड़ा चश्मेवाला निकला।",
            "• <b>पानवाले की टिप्पणी पर व्यंग्य:</b> पानवाले ने कैप्टन को 'लँगड़ा' और 'पागल' कहकर उसका मज़ाक उड़ाया, जो हालदार साहब को बहुत बुरा लगा।",
            "• <b>अंदर की सबसे गहरी बात:</b> लेखक समाज की कड़वी सच्चाई दिखाते हैं कि आज के स्वार्थी लोग उन सच्चे देशभक्तों को 'पागल' समझते हैं जो निःस्वार्थ भाव से शहीदों का सम्मान करते हैं।",
            "• <b>कठिन शब्दार्थ:</b> भूतपूर्व = पहले का  |  अवाक् रह जाना = हैरान होकर चुप रह जाना  |  मरियल = बेहद कमज़ोर।"
        ],
        "exam_tip": "★ MP Board IMP प्रश्न: 'वो लँगड़ा क्या जाएगा फ़ौज में। पागल है पागल!' — कैप्टन के प्रति पानवाले की इस टिप्पणी पर अपने विचार लिखिए।",
        "orig_durs": (47.5, 39.4),
        "read_audio": (
            "आइए अब अध्याय का तीसरा और अत्यंत महत्वपूर्ण गद्यांश पढ़ते हैं। "
            "हालदार साहब ने पानवाले से पूछा, क्या कैप्टन चश्मेवाला नेताजी का साथी है, या आज़ाद हिंद फ़ौज का भूतपूर्व सिपाही? "
            "पानवाले ने मुस्कुराकर कहा, नहीं साब! वो लँगड़ा क्या जाएगा फ़ौज में। पागल है पागल! वो देखो, वो आ रहा है, फोटो वोटो छपवा दो उसका कहीं। "
            "हालदार साहब को पानवाले द्वारा एक देशभक्त का इस तरह मज़ाक उड़ाया जाना बिल्कुल अच्छा नहीं लगा। "
            "मुड़कर देखा तो हैरान रह गए, एक बेहद बूढ़ा मरियल सा लँगड़ा आदमी, सिर पर गांधी टोपी लगाए, "
            "हाथ में संदूकची और बाँस पर चश्मे टाँगे गली से निकल रहा था।"
        ),
        "explain_audio": (
            "विद्यार्थियों, इस हिस्से के अंदर लेखक ने बहुत गहरा सामाजिक संदेश दिया है। "
            "बोर्ड परीक्षा में यह प्रश्न बार बार पूछा जाता है कि हालदार साहब को पानवाले की बात क्यों बुरी लगी? "
            "क्योंकि कैप्टन भले ही शरीर से बूढ़ा, गरीब और अपंग था, लेकिन उसका दिल किसी सच्चे फौजी से कम नहीं था। "
            "जबकि पानवाला जैसे लोग खुद तो देश के लिए कुछ करते नहीं, उल्टा देशभक्तों को पागल कहकर उनकी हँसी उड़ाते हैं। "
            "लेखक हमें समझाना चाहते हैं कि देशभक्ति ताकत या पैसे से नहीं, बल्कि मन की भावना से होती है।"
        )
    },
    {
        "sec_id": 4,
        "title": "भाग 4: कैप्टन की मृत्यु, सरकंडे का चश्मा और कहानी का अमर संदेश",
        "img": "netaji_s4_sarkanda.jpg",
        "book_heading": "★ NCERT मूल पाठ (गद्यांश 4 — समापन भाग):",
        "book_text": (
            "“एक दिन मूर्ति के चेहरे पर कोई भी चश्मा नहीं था। पानवाले ने उदास होकर आँखें पोंछते हुए कहा — साहब! कैप्टन मर गया। "
            "पंद्रह दिन बाद हालदार साहब ने सोचा कि आज चौराहे पर रुकेंगे भी नहीं और मूर्ति की तरफ देखेंगे भी नहीं। "
            "परंतु आदत से मजबूर आँखें चौराहे पर आते ही मूर्ति की तरफ उठ गईं। जीप स्पीड में थी, हालदार साहब चीखकर बोले — रोको! "
            "मूर्ति की आँखों पर सरकंडे से बना छोटा-सा चश्मा रखा हुआ था, जैसा बच्चे बना लेते हैं। "
            "हालदार साहब इतनी-सी बात पर भावुक हो उठे और उनकी आँखें भर आईं।”"
        ),
        "inside_heading": "★ अंदर की बातें और सरल व्याख्या (Deep Meaning):",
        "inside_points": [
            "• <b>कैप्टन की मृत्यु का दुख:</b> कैप्टन के गुज़र जाने से मूर्ति सूनी हो गई और पानवाला भी रो पड़ा — यानी उसके मन में भी कैप्टन के लिए संवेदना थी।",
            "• <b>सरकंडे का चश्मा (कहानी का चरम बिंदु):</b> जब हालदार साहब को लगा कि अब मूर्ति पर कोई चश्मा नहीं लगाएगा, तभी उन्हें मूर्ति की आँखों पर <b>बच्चों द्वारा घास (सरकंडे) से बनाया गया चश्मा</b> दिखा!",
            "• <b>अंदर का अमर संदेश:</b> उस छोटे-से सरकंडे के चश्मे ने साबित कर दिया कि कैप्टन न सही, <b>आने वाली नई पीढ़ी (बच्चों) के दिलों में देशभक्ति का बीज आज भी जीवित है!</b>",
            "• <b>कठिन शब्दार्थ:</b> कौम = राष्ट्र/समाज  |  होम कर देना = बलिदान करना  |  सरकंडा = पतली घास की डंडी  |  भावुक = संवेदनशील।"
        ],
        "exam_tip": "★ MP Board सबसे महत्वपूर्ण प्रश्न: नेताजी की मूर्ति पर लगा 'सरकंडे का चश्मा' क्या उम्मीद जगाता है? (4 अंक पक्के!)",
        "orig_durs": (43.2, 54.1),
        "read_audio": (
            "चलिए अब इस पाठ के अंतिम और सबसे भावुक भाग को पढ़ते हैं। "
            "एक दिन मूर्ति के चेहरे पर कोई भी चश्मा नहीं था। पूछने पर पानवाले ने आँखें पोंछते हुए उदास स्वर में कहा, साहब, कैप्टन मर गया। "
            "पंद्रह दिन बाद हालदार साहब ने सोचा कि आज वह बिना चश्मे वाली मूर्ति की तरफ देखेंगे भी नहीं। "
            "लेकिन चौराहे पर पहुँचते ही उनकी नज़र मूर्ति पर पड़ी और वह ज़ोर से चीखे, जीप रोको! "
            "मूर्ति की आँखों पर सरकंडे से बना छोटा सा चश्मा रखा हुआ था, जैसा बच्चे बना लेते हैं। "
            "हालदार साहब सावधान की मुद्रा में खड़े हो गए और उनकी आँखें भर आईं।"
        ),
        "explain_audio": (
            "आइए अब इस समापन भाग के अंदर की सबसे बड़ी बात को समझते हैं, जो हर साल एमपी बोर्ड परीक्षा में पूछी जाती है। "
            "आखिर सरकंडे का चश्मा देखकर हालदार साहब की आँखें क्यों भर आईं? "
            "क्योंकि कैप्टन के मरने के बाद हालदार साहब निराश हो गए थे कि अब नेताजी की मूर्ति का सम्मान करने वाला कोई नहीं बचा। "
            "लेकिन कस्बे के छोटे बच्चों ने देखा कि नेताजी की आँखों पर चश्मा नहीं है। बच्चों के पास असली चश्मा खरीदने के पैसे नहीं थे, "
            "तो उन्होंने सरकंडे की लकड़ी से चश्मा बनाकर नेताजी को पहना दिया! "
            "यह सरकंडे का चश्मा उम्मीद जगाता है कि हमारे देश के बच्चों और नई पीढ़ी में देशभक्ति की भावना पूरी तरह सुरक्षित है। "
            "इसी के साथ नेताजी का चश्मा पाठ की संपूर्ण व्याख्या पूरी होती है!"
        )
    }
]


def synthesize_voice(text: str, out_wav: str, mode: str = "read"):
    if os.path.exists(out_wav) and os.path.getsize(out_wav) > 1000:
        return
    mp3_path = out_wav.replace(".wav", ".mp3")
    tts = gTTS(text=text, lang="hi", slow=False)
    tts.save(mp3_path)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    af = "asetrate=24000*1.01,atempo=1.06,aresample=24000,highpass=f=75,dynaudnorm" if mode == "read" else "asetrate=24000*0.98,atempo=1.09,aresample=24000,highpass=f=75,dynaudnorm"
    subprocess.run([ff, "-y", "-i", mp3_path, "-af", af, "-ac", "1", "-ar", "24000", out_wav],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(mp3_path):
        os.remove(mp3_path)


def build_section_plate(sec: dict, phase: str, width: int = 1920, height: int = 1080) -> Image.Image:
    canvas = Image.new("RGBA", (width, height), (11, 17, 32, 255))
    draw = ImageDraw.Draw(canvas)

    # Top Header Bar
    draw.rounded_rectangle([24, 16, width - 24, 96], radius=18, fill=(22, 34, 62, 255), outline=(59, 130, 246, 255), width=2)
    hdr_markup = (
        f"<span foreground='#FBBF24' weight='heavy' size='19000'>MP BOARD कक्षा 10वीं NCERT (क्षितिज भाग-2)</span>   "
        f"<span foreground='#FFFFFF' weight='heavy' size='19500'>|   पाठ: नेताजी का चश्मा — {sec['title']}</span>"
    )
    hdr_img = render_pango_block(hdr_markup, width - 90, font_size=19)
    canvas.paste(hdr_img, (44, 30), hdr_img)

    # Mode Status Pill Bar (y=106..160)
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

    # LEFT PANEL: Scene Illustration + NCERT Book Passage (x=24..948, y=172..986)
    left_border = (16, 185, 129, 255) if phase == "read" else (51, 65, 85, 255)
    left_w = 4 if phase == "read" else 2
    draw.rounded_rectangle([24, 172, 948, 986], radius=20, fill=(17, 24, 39, 255), outline=left_border, width=left_w)

    ill_path = os.path.join(MP_ASSETS, sec["img"])
    if os.path.exists(ill_path):
        ill = Image.open(ill_path).convert("RGBA").resize((884, 340), Image.Resampling.LANCZOS)
        canvas.paste(ill, (44, 190))
        draw.rounded_rectangle([44, 190, 928, 530], radius=14, outline=(251, 191, 36, 220), width=2)

    draw.rounded_rectangle([40, 542, 932, 970], radius=14, fill=(30, 41, 59, 255) if phase == "read" else (15, 23, 42, 255),
                           outline=(52, 211, 153, 255) if phase == "read" else (51, 65, 85, 200), width=2)

    book_color = "#FEF08A" if phase == "read" else "#CBD5E1"
    book_markup = (
        f"<span foreground='#34D399' weight='heavy' size='19000'>{sec['book_heading']}</span>\n"
        f"<span foreground='{book_color}' weight='bold' size='17500'>{sec['book_text']}</span>"
    )
    book_img = render_pango_block(book_markup, 860, font_size=18)
    canvas.paste(book_img, (54, 552), book_img)

    # RIGHT PANEL: Inside Explanation ("अंदर की बातें") + Word Meanings + MP Board Exam Tip (x=968..1896, y=172..986)
    right_border = (250, 204, 21, 255) if phase == "explain" else (51, 65, 85, 255)
    right_w = 4 if phase == "explain" else 2
    draw.rounded_rectangle([968, 172, 1896, 986], radius=20, fill=(23, 31, 50, 255) if phase == "explain" else (15, 23, 42, 255),
                           outline=right_border, width=right_w)

    pts_joined = "\n\n".join(sec["inside_points"])
    right_markup = (
        f"<span foreground='#FBBF24' weight='heavy' size='20000'>{sec['inside_heading']}</span>\n\n"
        f"<span foreground='#F8FAFC' size='17500'>{pts_joined}</span>"
    )
    right_img = render_pango_block(right_markup, 884, font_size=18)
    canvas.paste(right_img, (990, 190), right_img)

    # Bottom Right Box: MP Board Exam Tip (y=850..970)
    draw.rounded_rectangle([986, 848, 1878, 968], radius=14, fill=(127, 29, 29, 255), outline=(248, 113, 113, 255), width=2)
    tip_markup = f"<span foreground='#FEF08A' weight='heavy' size='17500'>{sec['exam_tip']}</span>"
    tip_img = render_pango_block(tip_markup, 860, font_size=18)
    canvas.paste(tip_img, (1002, 862), tip_img)

    return canvas


def build_mpboard_chapter_video():
    print("========================================================================")
    print("📚 BUILDING MP BOARD CLASS 10 NCERT CHAPTER VIDEO: नेताजी का चश्मा")
    print("========================================================================")
    sr = 24000
    master_wav = os.path.join(TEMP_DIR, "mpboard_master.wav")
    out_mp4 = os.path.join(OUTPUT_DIR, "mpboard_c10_netaji_ka_chashma.mp4")
    out_mp4_tmp = os.path.join(OUTPUT_DIR, "mpboard_c10_tmp.mp4")
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    segment_plan = []

    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 1000000:
        subprocess.run([ff, "-y", "-i", out_mp4, "-vn", "-ac", "1", "-ar", str(sr), master_wav],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for sec in CHAPTER_SECTIONS:
            r_dur, e_dur = sec["orig_durs"]
            segment_plan.append((sec, r_dur, e_dur))
    else:
        with wave.open(master_wav, "wb") as out_wf:
            out_wf.setnchannels(1)
            out_wf.setsampwidth(2)
            out_wf.setframerate(sr)

            for sec in CHAPTER_SECTIONS:
                sid = sec["sec_id"]
                r_wav = os.path.join(TEMP_DIR, f"sec{sid}_read.wav")
                synthesize_voice(sec["read_audio"], r_wav, mode="read")
                with wave.open(r_wav, "rb") as wf:
                    r_pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
                out_wf.writeframes(r_pcm.tobytes())
                r_dur = len(r_pcm) / float(sr)

                e_wav = os.path.join(TEMP_DIR, f"sec{sid}_explain.wav")
                synthesize_voice(sec["explain_audio"], e_wav, mode="explain")
                with wave.open(e_wav, "rb") as wf:
                    e_pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
                out_wf.writeframes(e_pcm.tobytes())
                e_dur = len(e_pcm) / float(sr)

                segment_plan.append((sec, r_dur, e_dur))

    total_dur = sum(r + e for _, r, e in segment_plan)
    print(f"⏱️ Total Chapter Explanation Duration: {total_dur/60.0:.2f} minutes ({total_dur:.1f}s)")

    out_thumb = os.path.join(OUTPUT_DIR, "mpboard_c10_netaji_thumb.jpg")
    p1 = build_section_plate(CHAPTER_SECTIONS[0], "explain", 1920, 1080)
    p1.resize((1280, 720), Image.Resampling.LANCZOS).convert("RGB").save(out_thumb, "JPEG", quality=92)

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
        out_mp4_tmp
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elapsed = 0.0
    for sec, r_dur, e_dur in segment_plan:
        for phase, p_dur in [("read", r_dur), ("explain", e_dur)]:
            base_plate = build_section_plate(sec, phase, 1920, 1080)
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
    if os.path.exists(out_mp4_tmp):
        os.replace(out_mp4_tmp, out_mp4)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    sz_mb = os.path.getsize(out_mp4) / (1024 * 1024)
    print(f"✅ MP Board Class 10 Video Ready ({sz_mb:.2f} MB): {out_mp4}")
    return out_mp4, out_thumb


if __name__ == "__main__":
    build_mpboard_chapter_video()
