# stage3_clean_chunk.py
import sys
import re
from pathlib import Path

def clean_text(raw_text):
    t = raw_text
    # basic cleanup rules — tweak as needed
    t = re.sub(r"\[.*?\]", " ", t)            # drop [00:01:23] style timestamps
    t = re.sub(r"\s+", " ", t).strip()       # collapse whitespace
    return t

def chunk_text(text, max_chars=3000):
    # simple character-based chunker that tries to split at sentences.
    sentences = re.split(r'(?<=[\.\?\!])\s+', text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current += (" " if current else "") + s
        else:
            if current:
                chunks.append(current.strip())
            current = s
    if current:
        chunks.append(current.strip())
    return chunks

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stage3_clean_chunk.py transcript.txt [out_clean.txt]")
        sys.exit(1)
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8")
    clean = clean_text(raw)
    out_clean = sys.argv[2] if len(sys.argv) > 2 else "transcript_clean.txt"
    Path(out_clean).write_text(clean, encoding="utf-8")
    print(f"Clean transcript saved to {out_clean}")
    chunks = chunk_text(clean)
    print(f"Split into {len(chunks)} chunk(s).")
    for i, c in enumerate(chunks, 1):
        with open(f"chunk_{i}.txt", "w", encoding="utf-8") as f:
            f.write(c)
    print("Saved chunk_1.txt ...")
