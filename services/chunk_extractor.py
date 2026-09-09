import os
import re
import json
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import IpBlocked, RequestBlocked, CouldNotRetrieveTranscript


def get_transcript_api() -> YouTubeTranscriptApi:
    """
    Initializes YouTubeTranscriptApi with optional proxy configuration
    if YOUTUBE_PROXY, HTTPS_PROXY, or HTTP_PROXY is set in the environment.
    """
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
    """
    Extracts 11-character YouTube video ID from various URL formats including Shorts.
    """
    pattern = r"(?:v=|\/embed\/|\/shorts\/|youtu\.be\/|\/v\/|^)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    if len(url.strip()) == 11:
        return url.strip()
    raise ValueError(f"Could not extract a valid 11-character YouTube video ID from URL: {url}")


def fetch_via_invidious(video_id: str) -> str:
    """
    Zero-proxy fallback: queries public decentralized Invidious mirror APIs
    to download subtitle tracks if YouTube blocks datacenter IPs.
    """
    mirror_instances = [
        "https://inv.nadeko.net",
        "https://invidious.nerdvpn.de",
        "https://yewtu.be",
        "https://invidious.jing.rocks"
    ]

    for base_url in mirror_instances:
        try:
            api_url = f"{base_url}/api/v1/captions/{video_id}"
            req = urllib.request.Request(
                api_url, 
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                captions = data.get("captions", [])
                if not captions:
                    continue

                # Prioritize English, Hindi, or first available track
                chosen = next((c for c in captions if c.get("languageCode") in ["en", "hi", "es", "fr", "de"]), captions[0])
                caption_url = f"{base_url}{chosen.get('url')}"

                req_cap = urllib.request.Request(
                    caption_url, 
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                )
                with urllib.request.urlopen(req_cap, timeout=4) as cap_resp:
                    raw_content = cap_resp.read().decode("utf-8", errors="ignore")
                    
                    # Clean WebVTT timestamps, headers, and metadata
                    clean_lines = []
                    for line in raw_content.splitlines():
                        line = line.strip()
                        if not line or "-->" in line or line.startswith("WEBVTT") or line.isdigit():
                            continue
                        clean_lines.append(line)
                    
                    cleaned_text = " ".join(clean_lines)
                    if len(cleaned_text) > 80:
                        print(f"[SUCCESS] Extracted transcript via decentralized mirror: {base_url}")
                        return cleaned_text
        except Exception:
            continue

    return ""


def chunk_extractor(url: str) -> dict:
    video_id = extract_video_id(url)
    api = get_transcript_api()
    target_languages = ['en', 'hi', 'es', 'fr', 'de']

    # Step 1: Attempt standard YouTubeTranscriptApi extraction
    try:
        try:
            transcript_list = api.list(video_id)
            try:
                transcript = transcript_list.find_manually_created_transcript(target_languages)
            except Exception:
                transcript = transcript_list.find_generated_transcript(target_languages)
            fetched_data = transcript.fetch()
        except (IpBlocked, RequestBlocked):
            raise
        except Exception:
            fetched_data = api.fetch(video_id, languages=target_languages)

        response_text = " ".join(
            line.text if hasattr(line, 'text') else line['text'] 
            for line in fetched_data
        )
        
        print(f"[SUCCESS] Extracted transcript for video_id: {video_id} ({len(response_text.split())} words)")
        return {
            "text": response_text,
            "video_id": video_id
        }

    except (IpBlocked, RequestBlocked) as ip_err:
        print(f"[WARN] YouTube direct IP blocked ({type(ip_err).__name__}). Attempting mirror failover...")
        
        # Step 2: Zero-proxy failover via public mirrors
        mirror_text = fetch_via_invidious(video_id)
        if mirror_text:
            return {
                "text": mirror_text,
                "video_id": video_id
            }

        # Step 3: If mirrors also fail, provide actionable error for proxy or client-side fallback
        raise RuntimeError(
            "YouTube has blocked this cloud server's IP address. "
            "To resolve this on Render, set YOUTUBE_PROXY in your dashboard or use client-side ingestion."
        ) from ip_err

    except Exception as e:
        # For non-IP block failures, also attempt mirror before failing
        mirror_text = fetch_via_invidious(video_id)
        if mirror_text:
            return {
                "text": mirror_text,
                "video_id": video_id
            }
        print(f"[ERROR] Failed to extract transcript ({type(e).__name__}): {e}")
        raise RuntimeError(f"Failed to extract transcript for video: {e}") from e


if __name__ == "__main__":
    result = chunk_extractor("https://www.youtube.com/watch?v=4JofSJIrjwU")
    print("Test extraction result words:", len(result["text"].split()))
