"""
NaijaNews AI — Nigerian News Summarizer in Local Languages
Scrapes Nigerian news and reads summaries in Igbo, Yoruba, Hausa & Pidgin.
Powered by Google Gemini + gTTS + RSS feeds
"""

import streamlit as st
from google import genai
from gtts import gTTS
import base64
import tempfile
import os
import requests
import feedparser
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="NaijaNews AI",
    page_icon="📰",
    layout="wide"
)

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    .news-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        cursor: pointer;
        transition: border-color 0.2s;
    }
    .news-card:hover { border-color: #58a6ff; }
    .category-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .translation-box {
        background: #0d1117;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        font-size: 1.1rem;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style='text-align:center;padding:16px 0'>
    <h1>📰 NaijaNews AI</h1>
    <p style='color:#888'>Nigerian News — Summarized & Read in Your Language 🇳🇬</p>
</div>
""", unsafe_allow_html=True)
st.divider()

# --- Config ---
LANGUAGES = {
    "🟢 Igbo": {"code": "ig", "tld": "com", "color": "#00cc66", "name": "Igbo"},
    "🟡 Yoruba": {"code": "yo", "tld": "com", "color": "#ffd700", "name": "Yoruba"},
    "🔵 Hausa": {"code": "ha", "tld": "com", "color": "#4499ff", "name": "Hausa"},
    "🟠 Pidgin": {"code": "en", "tld": "com.ng", "color": "#ff8c00", "name": "Pidgin"},
    "🇬🇧 English": {"code": "en", "tld": "com", "color": "#ffffff", "name": "English"},
}

# Nigerian news RSS feeds
NEWS_SOURCES = {
    "🗞️ Punch": "https://punchng.com/feed/",
    "📺 Channels TV": "https://www.channelstv.com/feed/",
    "🌐 Vanguard": "https://www.vanguardngr.com/feed/",
    "📱 Premium Times": "https://www.premiumtimesng.com/feed/",
    "🎙️ The Nation": "https://thenationonlineng.net/feed/",
    "💼 BusinessDay": "https://businessday.ng/feed/",
}

CATEGORIES = {
    "🏠 All News": None,
    "🏛️ Politics": ["politics", "government", "election", "president", "governor"],
    "💰 Business": ["business", "economy", "naira", "CBN", "bank", "fintech"],
    "⚽ Sports": ["football", "sport", "Super Eagles", "AFCON", "premier league"],
    "🔬 Technology": ["tech", "AI", "startup", "digital", "innovation"],
    "🏥 Health": ["health", "hospital", "disease", "COVID", "malaria"],
    "🎓 Education": ["education", "school", "university", "WAEC", "JAMB"],
}


@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_news(source_url: str, limit: int = 10) -> list:
    """Fetch news from RSS feed."""
    try:
        feed = feedparser.parse(source_url)
        articles = []
        for entry in feed.entries[:limit]:
            articles.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", entry.get("description", ""))[:500],
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": feed.feed.get("title", ""),
            })
        return articles
    except Exception:
        return []


def fetch_all_news() -> list:
    """Fetch from all sources."""
    all_articles = []
    for source_name, source_url in NEWS_SOURCES.items():
        articles = fetch_news(source_url, limit=5)
        for a in articles:
            a["source_name"] = source_name
        all_articles.extend(articles)
    return all_articles


def filter_by_category(articles: list, category: str) -> list:
    """Filter articles by category keywords."""
    if category == "🏠 All News" or CATEGORIES[category] is None:
        return articles
    keywords = CATEGORIES[category]
    filtered = []
    for a in articles:
        text = (a["title"] + " " + a["summary"]).lower()
        if any(kw.lower() in text for kw in keywords):
            filtered.append(a)
    return filtered if filtered else articles[:5]


def summarize_and_translate(article: dict, language: dict, api_key: str) -> tuple:
    """Summarize news article and translate."""
    client = genai.Client(api_key=api_key)

    # Summarize
    summary_prompt = f"""You are NaijaNews AI. Summarize this Nigerian news article in 3-4 clear sentences.
Focus on: What happened? Who was involved? Why does it matter to Nigerians?
Keep it simple and factual.

Title: {article['title']}
Content: {article['summary']}

Return ONLY the summary."""

    summary_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=summary_prompt
    )
    english_summary = summary_response.text.strip()

    if language["name"] == "English":
        return english_summary, english_summary

    # Translate
    if language["name"] == "Pidgin":
        translate_prompt = f"""Translate this Nigerian news summary to Nigerian Pidgin English.
Use authentic Pidgin. Keep names and places as they are.
Pidgin words: dey, wetin, dem, e don happen, na so, e be like say, 
according to, abi, shey you know, e serious o.

Summary:
{english_summary}

Return ONLY the Pidgin translation."""
    else:
        translate_prompt = f"""Translate this Nigerian news summary to {language['name']} language.
Keep names and places as they are.
Return ONLY the {language['name']} translation.

Summary:
{english_summary}"""

    translated = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=translate_prompt
    )

    return english_summary, translated.text.strip()


def speak_text(text: str, lang_code: str, tld: str) -> bytes:
    clean = text.replace("*", "").replace("#", "").replace("_", "")
    try:
        tts = gTTS(text=clean, lang=lang_code, tld=tld, slow=False)
    except Exception:
        tts = gTTS(text=clean, lang="en", slow=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        with open(f.name, "rb") as af:
            audio = af.read()
    os.unlink(f.name)
    return audio


def autoplay(audio: bytes):
    b64 = base64.b64encode(audio).decode()
    st.markdown(
        f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
        unsafe_allow_html=True
    )


# --- API Key ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("✅ API Key loaded!")
except Exception:
    api_key = st.sidebar.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="AIza..."
    )

st.sidebar.markdown("---")
st.sidebar.markdown("**📰 News Sources:**")
for source in NEWS_SOURCES:
    st.sidebar.markdown(f"- {source}")
st.sidebar.markdown("---")
st.sidebar.markdown(f"🕐 Last updated: {datetime.now().strftime('%H:%M')}")
st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Wisdom Okparaji**")

# --- Controls ---
col1, col2, col3 = st.columns(3)
with col1:
    selected_lang_name = st.selectbox("🗣️ Language:", list(LANGUAGES.keys()))
with col2:
    selected_category = st.selectbox("📂 Category:", list(CATEGORIES.keys()))
with col3:
    selected_source = st.selectbox("📰 Source:", ["All Sources"] + list(NEWS_SOURCES.keys()))

selected_lang = LANGUAGES[selected_lang_name]

# --- Fetch News ---
with st.spinner("Fetching latest Nigerian news..."):
    if selected_source == "All Sources":
        all_articles = fetch_all_news()
    else:
        all_articles = fetch_news(NEWS_SOURCES[selected_source], limit=15)
        for a in all_articles:
            a["source_name"] = selected_source

    filtered_articles = filter_by_category(all_articles, selected_category)

st.markdown(f"### 📰 {len(filtered_articles)} Articles — {selected_category}")
st.caption(f"Click any article to hear it in {selected_lang_name}")
st.divider()

# --- Display Articles ---
if not filtered_articles:
    st.warning("No articles found. Try a different source or category.")
else:
    for i, article in enumerate(filtered_articles[:12]):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"""
            <div class='news-card'>
                <span class='category-badge' style='background:#1a3a1a;color:#3fb950'>
                    {article.get('source_name', '📰')}
                </span>
                <h4 style='margin:4px 0;color:#fff'>{article['title']}</h4>
                <p style='color:#888;font-size:0.85rem;margin:4px 0'>
                    {article['summary'][:150]}...
                </p>
                <a href='{article["link"]}' target='_blank' 
                   style='color:#58a6ff;font-size:0.8rem'>Read full article →</a>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if st.button(f"🔊 Read", key=f"read_{i}", use_container_width=True):
                st.session_state["selected_article"] = article
                st.session_state["article_index"] = i

    # --- Show Selected Article ---
    if "selected_article" in st.session_state:
        article = st.session_state["selected_article"]

        st.divider()
        st.markdown(f"### 🔊 Reading: {article['title']}")

        if not api_key:
            st.error("Please enter your Gemini API key!")
        else:
            with st.spinner(f"Summarizing and translating to {selected_lang_name}..."):
                try:
                    english_summary, translated_summary = summarize_and_translate(
                        article, selected_lang, api_key
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class='translation-box' style='border:1px solid #30363d'>
                            <p style='color:#888;font-size:0.8rem;margin:0'>📖 English Summary:</p>
                            <p style='color:#fff;margin:8px 0'>{english_summary}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class='translation-box' 
                             style='border:2px solid {selected_lang["color"]}'>
                            <p style='color:#888;font-size:0.8rem;margin:0'>
                                🗣️ {selected_lang_name}:
                            </p>
                            <p style='color:{selected_lang["color"]};margin:8px 0'>
                                {translated_summary}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                    audio = speak_text(
                        translated_summary,
                        selected_lang["code"],
                        selected_lang["tld"]
                    )
                    autoplay(audio)
                    st.audio(audio, format="audio/mp3")
                    st.success(f"🔊 Reading in {selected_lang_name}!")

                    # Read all headlines
                    if st.button("📢 Read All Headlines", use_container_width=True):
                        headlines = " ... ".join(
                            [a["title"] for a in filtered_articles[:5]]
                        )
                        with st.spinner("Preparing headlines..."):
                            _, translated_headlines = summarize_and_translate(
                                {"title": "Today's Headlines", "summary": headlines},
                                selected_lang, api_key
                            )
                            audio = speak_text(
                                translated_headlines,
                                selected_lang["code"],
                                selected_lang["tld"]
                            )
                            autoplay(audio)
                            st.audio(audio, format="audio/mp3")

                except Exception as e:
                    st.error(f"Error: {e}")

# --- Footer ---
st.divider()
st.markdown(
    "<center><small>NaijaNews AI v1.0 | Built by Wisdom Okparaji | "
    "Nigerian News in Your Language 📰🇳🇬</small></center>",
    unsafe_allow_html=True
)