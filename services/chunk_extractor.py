import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()

def extract_video_id(url: str) -> str:
    """
    Extracts 11-character YouTube video ID from various URL formats including:
    - https://www.youtube.com/watch?v=VIDEO_ID&list=...
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - VIDEO_ID
    """
    pattern = r"(?:v=|\/embed\/|youtu\.be\/|\/v\/|^)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    if len(url.strip()) == 11:
        return url.strip()
    raise ValueError(f"Could not extract a valid 11-character YouTube video ID from URL: {url}")

