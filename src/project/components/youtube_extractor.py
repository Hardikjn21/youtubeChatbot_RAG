import re
from youtube_transcript_api import YouTubeTranscriptApi

class InvalidYouTubeURL(Exception):
    pass

class TranscriptNotFound(Exception):
    pass

def extract_video_id(url: str) -> str:
    patterns = [r"v=([^&]+)", r"youtu\.be/([^?]+)"]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise InvalidYouTubeURL("Invalid YouTube URL")

def fetch_transcript(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(item["text"] for item in transcript)
    except Exception:
        raise TranscriptNotFound("Transcript not found")
