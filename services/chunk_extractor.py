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

def chunk_extractor(url: str) -> dict:
    try:
        video_id = extract_video_id(url)
        
        # Robust transcript extraction using youtube_transcript_api v0.6+
        try:
            transcript_list = api.list(video_id)
            try:
                transcript = transcript_list.find_manually_created_transcript(['en', 'hi', 'es', 'fr', 'de'])
            except Exception:
                transcript = transcript_list.find_generated_transcript(['en', 'hi', 'es', 'fr', 'de'])
            fetched_data = transcript.fetch()
        except Exception:
            fetched_data = api.fetch(video_id, languages=['en', 'hi'])

        response_text = " ".join(line.text if hasattr(line, 'text') else line['text'] for line in fetched_data)
        print(f"[SUCCESS] Extracted full transcript for video_id: {video_id} ({len(response_text)} chars, {len(response_text.split())} words)")
        
        return {
            "text": response_text,
            "video_id": video_id
        }

    except Exception as e:
        print(f"Error extracting transcript: {e}")
        raise Exception(f"Failed to extract transcript for video: {e}")

if __name__ == "__main__":
    result = chunk_extractor("https://www.youtube.com/watch?v=4JofSJIrjwU")
    print(result)
