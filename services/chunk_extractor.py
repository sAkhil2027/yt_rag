import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript_api() -> YouTubeTranscriptApi:
    proxy_url = os.getenv("YOUTUBE_PROXY") or os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
    if proxy_url:
        try:
            from youtube_transcript_api.proxies import GenericProxyConfig
            proxy_config = GenericProxyConfig(http_url=proxy_url, https_url=proxy_url)
            return YouTubeTranscriptApi(proxy_config=proxy_config)
        except Exception as pe:
            print(f"[WARN] Failed to configure proxy: {pe}")
    return YouTubeTranscriptApi()

def extract_video_id(url: str) -> str:
    pattern = r"(?:v=|\/embed\/|youtu\.be\/|\/v\/|^)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    if len(url.strip()) == 11:
        return url.strip()
    raise ValueError(f"Could not extract a valid 11-character YouTube video ID from URL: {url}")

def chunk_extractor(url: str) -> dict:
    video_id = extract_video_id(url)
    api = get_transcript_api()
    fetched_data = api.fetch(video_id, languages=['en', 'hi'])
    response_text = " ".join(line.text if hasattr(line, 'text') else line['text'] for line in fetched_data)
    return {"text": response_text, "video_id": video_id}
