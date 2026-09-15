"""
Convert a podcast script (NICK:/SOPHIE:/DAN:/SAM: labels) into the plain
"Speaker 1: ..." format VibeVoice expects, stripping any [bracket] cues.

Usage:
    python md_to_vibevoice.py episodes/episode-02.md episodes/episode-02.txt

Prints the speaker order so you know which --speaker_names to pass.
"""
import re
import sys

STOP_AT = "## RESEARCH NOTES"
LABEL = re.compile(r"^([A-Z][A-Z]+):\s*(.+)$")
CUE = re.compile(r"\s*\[[^\]]*\]\s*")

def convert(src, dst):
    speakers, lines = [], []
    with open(src, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line.startswith(STOP_AT):
                break
            m = LABEL.match(line)
            if not m:
                continue
            name, text = m.group(1), m.group(2)
            text = CUE.sub(" ", text).strip()          # drop [laughing] etc.
            text = re.sub(r"\s{2,}", " ", text)
            if not text:
                continue
            if name not in speakers:
                speakers.append(name)
            idx = speakers.index(name) + 1
            lines.append(f"Speaker {idx}: {text}")
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(lines)} turns written to {dst}")
    for i, s in enumerate(speakers, 1):
        print(f"  Speaker {i} = {s}")
    return speakers

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python md_to_vibevoice.py in.md out.txt")
    convert(sys.argv[1], sys.argv[2])
