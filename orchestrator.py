# orchestrator.py
import argparse
import subprocess
import sys
from pathlib import Path

STAGES = {
    1: ("Download audio from YouTube", "stage1_download_audio.py"),
    2: ("Transcribe audio to text", "stage2_transcribe.py"),
    3: ("Clean + chunk transcript text", "stage3_clean_chunk.py"),
    4: ("Summarize transcript with LLM", "stage4_summarize.py"),
}

def run_stage(step, *, url=None, audio="audio.mp3", model="small", language=None,
              transcript="transcript.txt", clean="transcript_clean.txt", summary="summary.txt"):
    name, script = STAGES[step]
    print(f"\n🚀 Running Stage {step}: {name}")
    print("=" * 60)

    if step == 1:
        if not url:
            print("--url is required for stage 1.", file=sys.stderr)
            sys.exit(1)
        cmd = [sys.executable, script, url, audio]
    elif step == 2:
        if not Path(audio).exists():
            print(f"Audio not found: {audio}", file=sys.stderr)
            sys.exit(1)
        cmd = [sys.executable, script, audio, model]
        if language:
            # Only pass transcript when language is explicitly provided to preserve CLI positions
            cmd.append(language)
            cmd.append(transcript)
        else:
            # No language provided: rely on stage2 default output path
            if transcript != "transcript.txt":
                print("[Note] --language not provided; using stage2 default output 'transcript.txt'.")
    elif step == 3:
        if not Path(transcript).exists():
            print(f"Transcript not found: {transcript}", file=sys.stderr)
            sys.exit(1)
        cmd = [sys.executable, script, transcript, clean]
    else:  # step 4
        chunk_files = sorted(str(p) for p in Path('.').glob('chunk_*.txt'))
        if not chunk_files:
            if Path(clean).exists():
                chunk_files = [clean]
            else:
                print("No chunk_*.txt files or clean transcript found.", file=sys.stderr)
                sys.exit(1)
        cmd = [sys.executable, script, *chunk_files, summary]

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"✅ Stage {step} completed successfully.\n")
    else:
        print(f"❌ Stage {step} failed. Check logs.\n")
        sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser(description="Video Summarization Orchestrator")
    parser.add_argument("--step", action="append",
                        help="Stage number (1-4); repeat to run multiple. Omit to run all.")
    parser.add_argument("--url", help="YouTube URL (required for step 1)")
    parser.add_argument("--audio", default="audio.mp3",
                        help="Audio output of step 1 / input to step 2")
    parser.add_argument("--model", default="small",
                        help="Whisper model size for step 2")
    parser.add_argument("--language", default=None,
                        help="Language code for step 2 (e.g., en)")
    parser.add_argument("--transcript", default="transcript.txt",
                        help="Transcript output of step 2 / input to step 3")
    parser.add_argument("--clean", default="transcript_clean.txt",
                        help="Clean transcript output of step 3")
    parser.add_argument("--summary", default="summary.txt",
                        help="Final summary output of step 4")
    args = parser.parse_args()

    steps = [int(s) for s in args.step] if args.step else [1, 2, 3, 4]
    for s in steps:
        run_stage(s,
                  url=args.url,
                  audio=args.audio,
                  model=args.model,
                  language=args.language,
                  transcript=args.transcript,
                  clean=args.clean,
                  summary=args.summary)

if __name__ == "__main__":
    main()
