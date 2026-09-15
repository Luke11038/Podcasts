"""
Convert a HOST:/MIA:/DAN:/SAM: podcast script into one MP3 using
ElevenLabs Text to Dialogue (Eleven v3).

Usage:
    pip install requests
    export ELEVENLABS_API_KEY=your_key_here
    python make_episode.py episode-01-how-to-actually-talk-to-people.md

Needs ffmpeg installed for the final stitch (brew install ffmpeg / apt install ffmpeg).
"""

import os
import re
import sys
import subprocess
import requests

# ---- 1. Put your voice IDs here (Voices page > open voice > Copy voice ID) ----
VOICES = {
    "HOST": "PASTE_HOST_VOICE_ID",
    "MIA":  "PASTE_MIA_VOICE_ID",
    "DAN":  "PASTE_DAN_VOICE_ID",
    "SAM":  "PASTE_SAM_VOICE_ID",
}

MODEL_ID = "eleven_v3"
MAX_CHARS = 2000          # ElevenLabs limit per Text to Dialogue request
SEED = 42                 # keeps delivery a bit more consistent between chunks
API_URL = "https://api.elevenlabs.io/v1/text-to-dialogue"
API_KEY = os.environ.get("ELEVENLABS_API_KEY")

if not API_KEY:
    sys.exit("Set ELEVENLABS_API_KEY first.")


# ---- 2. Parse the script into (speaker, text) turns ----
def parse_script(path):
    turns = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("## RESEARCH NOTES"):
                break  # everything after this is not for audio
            m = re.match(r"^(HOST|MIA|DAN|SAM):\s*(.+)$", line)
            if m:
                turns.append((m.group(1), m.group(2)))
    return turns


# ---- 3. Group turns into chunks under the character limit ----
def chunk_turns(turns):
    chunks, current, size = [], [], 0
    for speaker, text in turns:
        if size + len(text) > MAX_CHARS and current:
            chunks.append(current)
            current, size = [], 0
        current.append({"text": text, "voice_id": VOICES[speaker]})
        size += len(text)
    if current:
        chunks.append(current)
    return chunks


# ---- 4. Generate each chunk ----
def generate(chunk, out_path):
    resp = requests.post(
        API_URL,
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"inputs": chunk, "model_id": MODEL_ID, "seed": SEED},
        timeout=300,
    )
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(resp.content)


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python make_episode.py script.md")
    script = sys.argv[1]
    for k, v in VOICES.items():
        if v.startswith("PASTE_"):
            print(f"Warning: no voice ID set for {k}")

    turns = parse_script(script)
    chunks = chunk_turns(turns)
    print(f"{len(turns)} turns -> {len(chunks)} chunks")

    os.makedirs("chunks", exist_ok=True)
    paths = []
    for i, chunk in enumerate(chunks, 1):
        path = f"chunks/part_{i:03d}.mp3"
        if not os.path.exists(path):          # lets you resume if it fails midway
            print(f"Generating {i}/{len(chunks)}...")
            generate(chunk, path)
        paths.append(path)

    # ---- 5. Stitch with ffmpeg ----
    with open("chunks/list.txt", "w") as f:
        for p in paths:
            f.write(f"file '{os.path.abspath(p)}'\n")
    out = os.path.splitext(os.path.basename(script))[0] + ".mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "chunks/list.txt", "-c", "copy", out],
        check=True,
    )
    print(f"Done: {out}")


if __name__ == "__main__":
    main()
