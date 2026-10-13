# 📱 100% Mobile Setup Guide — YouTube AI Automation (Bina Laptop/PC Ke!)

Kyunki aapke paas **sirf Mobile Phone** hai, maine is poore setup ko aisa bana diya hai ki aap **sirf apne Phone ke Chrome Browser** se 100% setup kar sakte hain! Kahin bhi Laptop ya PC ki zaroorat nahi padegi.

---

## 🟢 STEP 1: Free Gemini AI Key Nikalna (Mobile Se — 2 Minute)

1. Apne phone ke Chrome browser mein ye link kholein:
   👉 **[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Apne Google (Gmail) account se Sign In karein.
3. Neeche/Upar नीले (Blue) rang ka **"Create API key"** button dikhega, uspar tap karein.
4. Ek lamba code aayega (jo `AIzaSy...` se shuru hota hai) — **"Copy"** par tap karke use apne WhatsApp ya Notes mein save kar lein.
   - Iska naam hai: **`GEMINI_API_KEY`**

---

## 🟡 STEP 2: Mobile Se YouTube `CLIENT_ID`, `CLIENT_SECRET` aur `REFRESH_TOKEN` Nikalna (5 Minute)

### Part A: Google Cloud Console Setup (Mobile Browser Mein)
1. Phone mein ye link kholein: 👉 **[https://console.cloud.google.com/](https://console.cloud.google.com/)**
2. Upar project dropdown par tap karke **"New Project"** banayein (Naam: `YouTubeBot`) aur **Create** dabayein.
3. Menu (☰) kholein -> **APIs & Services** -> **Library** mein jayein.
4. Search box mein **`YouTube Data API v3`** likhein, uspar tap karein aur **ENABLE** button daba dein.
5. Menu (☰) -> **APIs & Services** -> **OAuth consent screen** par jayein:
   - User Type mein **External** chunein -> **Create** dabayein.
   - App Name mein `YouTubeBot` likhein, User support email aur Developer email mein apna Gmail daal kar **Save and Continue** karein.
   - **Test users** wale page par **"+ ADD USERS"** dabayein aur **apne YouTube channel wala Gmail ID** daal kar Save kar dein.
6. Menu (☰) -> **APIs & Services** -> **Credentials** par jayein:
   - Upar **"+ CREATE CREDENTIALS"** -> **"OAuth client ID"** par tap karein.
   - **Application type** mein **"Web application"** chunein (Mobile se token nikalne ke liye Web application sabse aasan hai!).
   - Neeche **"Authorized redirect URIs"** mein **"+ ADD URI"** par tap karein aur ye exact link paste karein:
     `https://developers.google.com/oauthplayground`
   - **Create** button dabayein!
   - Ab screen par aapko **Client ID** aur **Client Secret** dikhenge — dono ko copy karke apne Notes mein save kar lein!

### Part B: Mobile Se `REFRESH_TOKEN` Nikalna (Bina Laptop Ke!)
1. Apne phone mein ye official Google link kholein:
   👉 **[https://developers.google.com/oauthplayground](https://developers.google.com/oauthplayground)**
2. Upar right corner mein **⚙️ (Settings Gear icon)** par tap karein:
   - ✅ **"Use your own OAuth credentials"** par tick lagayein.
   - **OAuth Client ID** mein apna Client ID paste karein.
   - **OAuth Client secret** mein apna Client Secret paste karein aur Close दबा dein.
3. Left side (Step 1) mein neeche **"Input your own scopes"** box mein ye paste karein:
   `https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube`
4. **"Authorize APIs"** button par tap karein -> Apna YouTube channel select karein -> **"Continue / Allow"** dabayein.
5. Ab Step 2 khul jayega -> **"Exchange authorization code for tokens"** नीले button par tap karein.
6. Wahan **`Refresh token`** (`1//0g...` se shuru hone wala code) mil jayega! Use copy karke save kar lein.

---

## 🔵 STEP 3: GitHub Par Automatic Bot Chalu Karna (Mobile Se — 5 Minute)

1. Phone mein **[https://github.com](https://github.com)** kholein aur Sign Up / Login karein.
2. **New Repository** banayein -> Naam rakhein `youtube-ai-bot` -> **Private** select karein -> **"Add a README file"** par tick lagayein -> **Create repository** dabayein.
3. Mobile Chrome mein menu (⋮) se **"Desktop site"** on kar lein -> **"Add file" -> "Upload files"** par tap karke humari files upload kar dein.
4. Ab Repo ke **Settings -> Secrets and variables -> Actions** mein jaakar **"New repository secret"** se ye 4 secrets daal dein:
   - `GEMINI_API_KEY`
   - `YOUTUBE_CLIENT_ID`
   - `YOUTUBE_CLIENT_SECRET`
   - `YOUTUBE_REFRESH_TOKEN`
5. **Actions** tab mein jaakar workflow ko Enable/Run kar dein!
