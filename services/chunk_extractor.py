import os
import re
import json
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import IpBlocked, RequestBlocked, CouldNotRetrieveTranscript

def get_transcript_api() -> YouTubeTranscriptApi:
    proxy_url = os.getenv("YOUTUBE_PROXY") or os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
    if proxy_url:
        try:
            from youtube_transcript_api.proxies import GenericProxyConfig
            proxy_config = GenericProxyConfig(http_url=proxy_url, https_url=proxy_url)
            return YouTubeTranscriptApi(proxy_config=proxy_config)
        except Exception as pe:
            print(f"[WARN] Failed to configure proxy: {pe}, falling back to direct client")
    return YouTubeTranscriptApi()

def extract_video_id(url: str) -> str:
    pattern = r"(?:v=|\/embed\/|\/shorts\/|youtu\.be\/|\/v\/|^)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    if len(url.strip()) == 11:
        return url.strip()
    raise ValueError(f"Could not extract a valid 11-character YouTube video ID from URL: {url}")

def fetch_via_invidious(video_id: str) -> str:
    mirror_instances = [
        "https://inv.nadeko.net",
        "https://invidious.nerdvpn.de",
        "https://yewtu.be",
        "https://invidious.jing.rocks"
    ]
    for base_url in mirror_instances:
        try:
            api_url = f"{base_url}/api/v1/captions/{video_id}"
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                captions = data.get("captions", [])
                if not captions:
                    continue
                chosen = next((c for c in captions if c.get("languageCode") in ["en", "hi", "es", "fr", "de"]), captions[0])
                req_cap = urllib.request.Request(f"{base_url}{chosen.get('url')}", headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req_cap, timeout=4) as cap_resp:
                    raw_content = cap_resp.read().decode("utf-8", errors="ignore")
                    clean_lines = [l.strip() for l in raw_content.splitlines() if l.strip() and "-->" not in l and not l.startswith("WEBVTT") and not l.isdigit()]
                    cleaned_text = " ".join(clean_lines)
                    if len(cleaned_text) > 80:
                        return cleaned_text
        except Exception:
            continue
    return ""

def chunk_extractor(url: str) -> dict:
    video_id = extract_video_id(url)
    api = get_transcript_api()
    target_languages = ['en', 'hi', 'es', 'fr', 'de']
    try:
        transcript_list = api.list(video_id)
        try:
            transcript = transcript_list.find_manually_created_transcript(target_languages)
        except Exception:
            transcript = transcript_list.find_generated_transcript(target_languages)
        fetched_data = transcript.fetch()
    except Exception:
        fetched_data = api.fetch(video_id, languages=target_languages)
    response_text = " ".join(line.text if hasattr(line, 'text') else line['text'] for line in fetched_data)
    return {"text": response_text, "video_id": video_id}
