# 📰 NaijaNews AI

<div align="center">

![NaijaNews AI Banner](https://img.shields.io/badge/NaijaNews-AI-green?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/Google-Gemini-blue?style=for-the-badge&logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**Nigerian News — Summarized & Read Aloud in Your Language 🇳🇬**

*Real news. Your language. Spoken aloud.* 🔊

[Live Demo](#) • [Report Bug](https://github.com/Santandave961/naijanews-ai/issues) • [Request Feature](https://github.com/Santandave961/naijanews-ai/issues)

</div>

---

## 📖 Table of Contents

- [About The Project](#about-the-project)
- [Features](#features)
- [News Sources](#news-sources)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Author](#author)

---

## 🎯 About The Project

NaijaNews AI is a real-time Nigerian news aggregator that **translates and reads the latest news aloud** in Igbo, Yoruba, Hausa, Pidgin or English — making Nigerian news accessible to every Nigerian regardless of their literacy level or preferred language.

### The Problem
Nigeria's top news outlets — Punch, Vanguard, Channels TV, Premium Times — publish exclusively in English. But millions of Nigerians across the North, East and West are more comfortable in their native languages. They miss out on important national news simply because of a language barrier.

### The Solution
NaijaNews AI scrapes live news from 6 major Nigerian outlets, uses Gemini AI to summarize each article into 3-4 clear sentences, translates the summary into the user's chosen language, and **reads it aloud** — just like a radio broadcaster, but in your language.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📰 **Live News** | Pulls real-time news from 6 Nigerian outlets via RSS |
| 🌍 **5 Languages** | Igbo, Yoruba, Hausa, Pidgin, English |
| 🔊 **Text-to-Speech** | Reads every article summary aloud |
| 🤖 **AI Summarization** | Gemini condenses articles to 3-4 clear sentences |
| 📂 **Category Filter** | Politics, Business, Sports, Tech, Health, Education |
| 🗞️ **Source Filter** | Filter by specific news outlet |
| 📢 **Read All Headlines** | Reads top 5 headlines in your language at once |
| ⚡ **Auto-Refresh** | News updates every 5 minutes automatically |
| 🆓 **100% Free** | Built entirely on free tiers |

---

## 🗞️ News Sources

| Source | Coverage |
|--------|----------|
| 🗞️ **Punch Nigeria** | General news, politics, business |
| 📺 **Channels TV** | Breaking news, politics, national affairs |
| 🌐 **Vanguard** | General news, economy, sports |
| 📱 **Premium Times** | Investigative journalism, politics |
| 🎙️ **The Nation** | Politics, business, lifestyle |
| 💼 **BusinessDay** | Economy, fintech, markets |

---

## 📂 News Categories

- 🏛️ **Politics** — Government, elections, presidency, governors
- 💰 **Business** — Economy, naira, CBN, banking, fintech
- ⚽ **Sports** — Football, Super Eagles, AFCON, Premier League
- 🔬 **Technology** — AI, startups, digital innovation
- 🏥 **Health** — Hospitals, diseases, public health
- 🎓 **Education** — Schools, universities, WAEC, JAMB

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Backend language |
| **Streamlit** | Web application framework |
| **Google Gemini 1.5 Flash** | AI summarization & translation |
| **gTTS** | Text-to-speech with Nigerian accent |
| **feedparser** | RSS feed parsing |
| **google-genai** | Official Gemini Python SDK |
| **requests** | HTTP requests |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))
- Internet connection

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Santandave961/naijanews-ai.git
cd naijanews-ai
```

**2. Install dependencies**
```bash
pip install streamlit google-genai gtts feedparser requests
```

**3. Run the app**
```bash
streamlit run app.py
```

**4. Get your free Gemini API key**
- Go to [aistudio.google.com](https://aistudio.google.com)
- Click **"Get API Key"** → **"Create API Key"**
- Copy the key (starts with `AIza...`)
- Paste it in the app sidebar

**5. Read your first article!**
- Select your language
- Choose a category
- Click **"🔊 Read"** on any article
- Hear it spoken in your language!

---

## ⚙️ How It Works

```
Nigerian News RSS Feeds (Punch, Vanguard, Channels TV...)
          ↓
    feedparser RSS Parser
    (Pulls latest headlines + summaries)
          ↓
    Category & Source Filter
    (Politics, Business, Sports etc.)
          ↓
    Google Gemini AI
    (Summarizes article in 3-4 sentences)
          ↓
    Gemini Translation
    (Translates to Igbo/Yoruba/Hausa/Pidgin)
          ↓
    gTTS Text-to-Speech
    (Nigerian accent audio generation)
          ↓
    Auto-plays in Browser + Audio Player
```

---

## 📁 Project Structure

```
naijanews-ai/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
└── .streamlit/
    └── secrets.toml      # API keys (NOT committed to git)
```

---

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"**
4. Select `Santandave961/naijanews-ai` → `master` → `app.py`
5. Click **"Advanced settings"** and add:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```
6. Click **"Deploy"**

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

---

## 🗺️ Roadmap

- [ ] Add more Nigerian news sources (Sahara Reporters, Daily Trust)
- [ ] Full Hausa and Yoruba TTS voice support
- [ ] WhatsApp news digest integration
- [ ] Daily news summary email in chosen language
- [ ] Offline reading mode
- [ ] Mobile app version

---

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/add-hausa-tts`)
3. Commit your changes (`git commit -m 'Add Hausa TTS support'`)
4. Push to the branch (`git push origin feature/add-hausa-tts`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License.

---

## 👤 Author

**Wisdom Okparaji**
*Data Scientist & ML Engineer*

[![GitHub](https://img.shields.io/badge/GitHub-Santandave961-black?style=flat&logo=github)](https://github.com/Santandave961)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Wisdom_Okparaji-blue?style=flat&logo=linkedin)](https://linkedin.com/in/wisdom-okparaji-680550246)
[![Twitter](https://img.shields.io/badge/X-@WOkparaji74619-black?style=flat&logo=x)](https://x.com/WOkparaji74619)
[![Portfolio](https://img.shields.io/badge/Portfolio-santandave961.github.io-green?style=flat)](https://santandave961.github.io)

---

## 🙏 Acknowledgements

- [Google Gemini](https://deepmind.google/technologies/gemini/) for AI summarization
- [gTTS](https://gtts.readthedocs.io/) for text-to-speech
- [Streamlit](https://streamlit.io/) for the app framework
- [feedparser](https://feedparser.readthedocs.io/) for RSS parsing
- Punch, Vanguard, Channels TV and all Nigerian news outlets

---

<div align="center">

**If this project resonates with you, abeg give am a ⭐ on GitHub!**

*Every Nigerian deserves news in their language* 🇳🇬

</div>
