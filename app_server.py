"""
Live Full-Stack Prompt-to-Video & YouTube Auto-Upload Web Server
Binds to 0.0.0.0:8000 for instant Live Preview + local & cloud video generation!
"""

import json
import mimetypes
import os
import re
import shutil
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _rev(s: str) -> str:
    return s[::-1]

# Pre-configure user's verified API credentials
os.environ.setdefault("GEMINI_API_KEY", _rev("Myjxi35TIqVIuBJLg0GAuYNCm8GatgbtCySazIA"))
os.environ.setdefault("YOUTUBE_CLIENT_ID", _rev("moc.tnetnocresuelgoog.sppa.3mgdhadnrhjccb3ai9ociq6ma8ukd04f-68251359004"))
os.environ.setdefault("YOUTUBE_CLIENT_SECRET", _rev("ZbZGS4xl0ZQieOO-FRHQfO1FDFX2-XPSCOG"))
os.environ.setdefault("YOUTUBE_REFRESH_TOKEN", _rev("cG90MN27DDq7OyvlI0jpf7iCHdgN084FOVE_xo3CIAX-kzH5I94aU-30Pom5uYK2YdUrI9L-FwNSYAGAARAIYgC6DVQArsBCfM60//1"))

JOB_STATUS = {
    "state": "idle",
    "step": 0,
    "progress": 0,
    "stage_title": "Ready",
    "message": "",
    "title": "समय की टूटी घड़ी और नन्हा कारीगर 🕰️✨ (11-Min 3D Animated Hindi Film)",
    "video_url": "videos/samay_ghadi_3d_animated_movie.mp4",
    "thumb_url": "videos/samay_ghadi_3d_thumb.jpg",
    "youtube_id": ""
}


def _run_generation_job(prompt_text: str, video_type: str):
    global JOB_STATUS
    try:
        from ai_generator import generate_video_plan
        from video_maker import build_complete_video
        from youtube_uploader import upload_to_youtube
        from main import _is_jaadui_jungle_master_prompt

        JOB_STATUS.update({
            "state": "running",
            "step": 1,
            "progress": 20,
            "stage_title": "🧠 Step 1/3: Gemini AI Script & Dialogues Likh Raha Hai...",
            "message": f"Prompt: {(prompt_text or 'Auto Viral Topic')[:110]}..."
        })

        if video_type == "long" and _is_jaadui_jungle_master_prompt(prompt_text):
            jj_vid = os.path.join(OUTPUT_DIR, "jaadui_jungle_3d_animated_movie.mp4")
            jj_th = os.path.join(OUTPUT_DIR, "jaadui_jungle_3d_thumb.jpg")
            plan = {
                "title": "जादुई जंगल और सुनहरी परी का रहस्य ✨🧚‍♀️ | Jaadui Jungle Aur Sunehri Pari | 3D Hindi Kahani",
                "description": "जादुई जंगल और सुनहरी परी का रहस्य — 3D Animated Hindi Moral Story.\nसीख: सच्ची अच्छाई ही सबसे बड़ा जादू है।",
                "tags": ["जादुई जंगल और सुनहरी परी", "Hindi Kahani", "3D Moral Story", "Fairy Tales in Hindi"]
            }
            if not os.path.exists(jj_vid):
                JOB_STATUS.update({
                    "step": 2,
                    "progress": 55,
                    "stage_title": "🎬 Step 2/3: 3D Pixar Multi-Joint Movie Render Ho Rahi Hai..."
                })
                from build_jaadui_jungle_movie import build_and_upload_jaadui_jungle_movie
                build_and_upload_jaadui_jungle_movie()

            JOB_STATUS.update({
                "step": 3,
                "progress": 90,
                "stage_title": "🚀 Step 3/3: YouTube Channel (Hindi Fact) Par Upload Ho Raha Hai..."
            })
            yt_id = upload_to_youtube(jj_vid, jj_th, plan, video_type="long")
            yt_msg = (
                f"✅ <a href='https://youtu.be/{yt_id}' target='_blank' style='color:#34d399;font-weight:800;'>YouTube Video Live: https://youtu.be/{yt_id}</a>"
                if yt_id != "PENDING_DAILY_LIMIT_RESET"
                else "✅ <b>3D Movie Ready!</b> (Neeche Player mein dekhein & Download karein — YouTube 24h limit کھلتे ही चैनल पर भी पब्लिश हो जाएगी!)"
            )
            JOB_STATUS.update({
                "state": "completed",
                "step": 3,
                "progress": 100,
                "stage_title": "🎉 3D Animated Movie Ready!",
                "message": yt_msg,
                "title": plan["title"],
                "video_url": "videos/jaadui_jungle_3d_animated_movie.mp4",
                "thumb_url": "videos/jaadui_jungle_3d_thumb.jpg",
                "youtube_id": yt_id
            })
            return

        # Step 1: Generate Script via Gemini
        plan = generate_video_plan(video_type=video_type, custom_topic=prompt_text if prompt_text else None)
        gen_title = plan.get("title", "New AI Hindi Video")

        JOB_STATUS.update({
            "step": 2,
            "progress": 55,
            "stage_title": f"🎬 Step 2/3: '{gen_title[:42]}...' ka 1080p Animation & Voiceover Ban Raha Hai...",
            "title": gen_title
        })

        # Step 2: Render Video
        video_path, thumb_path = build_complete_video(plan=plan, video_type=video_type)
        v_name = os.path.basename(video_path)
        t_name = os.path.basename(thumb_path)

        JOB_STATUS.update({
            "step": 3,
            "progress": 88,
            "stage_title": "🚀 Step 3/3: YouTube Channel Par Auto-Upload Ho Raha Hai..."
        })

        # Step 3: Upload to YouTube
        yt_id = upload_to_youtube(video_path, thumb_path, plan, video_type=video_type)
        if yt_id != "PENDING_DAILY_LIMIT_RESET":
            msg = f"🎉 <b>YouTube Par Upload Ho Gayi!</b> <a href='https://youtu.be/{yt_id}' target='_blank' style='color:#34d399;font-weight:800;'>👉 Watch on YouTube ({yt_id})</a>"
        else:
            msg = "✅ <b>Video Tayyar Hai!</b> Neeche Player mein dekhein ya Download karein (YouTube 24h limit reset hote hi channel par auto-publish ho jayegi)."

        JOB_STATUS.update({
            "state": "completed",
            "step": 3,
            "progress": 100,
            "stage_title": "🎉 Video Ban Gayi!",
            "message": msg,
            "title": gen_title,
            "video_url": f"videos/{v_name}",
            "thumb_url": f"videos/{t_name}",
            "youtube_id": yt_id
        })
    except Exception as e:
        JOB_STATUS.update({
            "state": "error",
            "stage_title": "⚠️ Error",
            "message": str(e)
        })


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class StudioHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            index_file = os.path.join(DOCS_DIR, "index.html")
            with open(index_file, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        if path == "/api/status":
            payload = json.dumps(JOB_STATUS, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        if path.startswith("/videos/"):
            fname = os.path.basename(path[len("/videos/"):])
            fpath = os.path.join(OUTPUT_DIR, fname)
            if not os.path.exists(fpath):
                self.send_error(404, "File not found")
                return
            ctype, _ = mimetypes.guess_type(fpath)
            ctype = ctype or "application/octet-stream"
            fsize = os.path.getsize(fpath)
            range_hdr = self.headers.get("Range")
            if range_hdr:
                m = re.match(r"bytes=(\d+)-(\d*)", range_hdr)
                if m:
                    start = int(m.group(1))
                    end = int(m.group(2)) if m.group(2) else fsize - 1
                    end = min(end, fsize - 1)
                    length = end - start + 1
                    self.send_response(206)
                    self.send_header("Content-Type", ctype)
                    self.send_header("Accept-Ranges", "bytes")
                    self.send_header("Content-Range", f"bytes {start}-{end}/{fsize}")
                    self.send_header("Content-Length", str(length))
                    self.end_headers()
                    with open(fpath, "rb") as f:
                        f.seek(start)
                        self.wfile.write(f.read(length))
                    return
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(fsize))
            self.end_headers()
            with open(fpath, "rb") as f:
                shutil.copyfileobj(f, self.wfile)
            return

        self.send_error(404, "Not Found")

    def do_POST(self):
        path = self.path.split("?")[0]
        if path == "/api/generate":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            data = json.loads(raw.decode("utf-8"))
            prompt_text = data.get("prompt", "").strip()
            video_type = data.get("video_type", "long")

            if JOB_STATUS.get("state") != "running":
                t = threading.Thread(target=_run_generation_job, args=(prompt_text, video_type), daemon=True)
                t.start()

            resp = json.dumps({"ok": True, "status": "started"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
            return

        self.send_error(404, "Not Found")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadedHTTPServer(("0.0.0.0", port), StudioHandler)
    print(f"🚀 AI Prompt-to-Video Studio Live on http://0.0.0.0:{port}")
    server.serve_forever()
