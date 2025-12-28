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
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        if hasattr(transcript, "snippets"):
            return " ".join(snippet.text for snippet in transcript.snippets)
        # fallback for older versions (list of dicts)
        return " ".join(item.get("text", "") for item in transcript)
    except Exception:
        raise TranscriptNotFound("Transcript not found")

if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    try:
        video_id = extract_video_id(url)
        print(f"Extracted Video ID: {video_id}")
        transcript = fetch_transcript(video_id)
        print(transcript)
    except (InvalidYouTubeURL, TranscriptNotFound) as e:
        print(e)