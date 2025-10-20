# Video Summarizer

A simple, modular pipeline to download audio from a YouTube video, transcribe it, clean and chunk the transcript, then produce a concise summary using a transformer model.

## Features
- Stage 1: Download audio from YouTube (yt-dlp)
- Stage 2: Transcribe audio using faster-whisper
- Stage 3: Clean and chunk the transcript
- Stage 4: Summarize with Hugging Face transformers
- Orchestrator to run all or selected stages step-by-step

## Requirements
- Python 3.12
- Linux (tested on Ubuntu)
- Optional: NVIDIA GPU + CUDA for faster inference (PyTorch/ctranslate2 wheels are installed by pip)

## Quickstart
```bash
# 0) Create and activate venv
python3 -m venv venv --without-pip
source venv/bin/activate
curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py && rm get-pip.py

# 1) Install dependencies
pip install yt-dlp faster-whisper transformers sentencepiece torch

# 2) (Optional) Install FFmpeg for MP3 conversion used by yt-dlp
# sudo apt update && sudo apt install -y ffmpeg

# 3) Run full pipeline with orchestrator
python orchestrator.py --url "https://www.youtube.com/watch?v=_Td7JjCTfyc"
```

## Orchestrator Usage
The orchestrator wraps all stage scripts and wires inputs/outputs.

```bash
# Full pipeline (stages 1-4)
python orchestrator.py --url "<youtube_url>"

# Run specific stages (repeat --step)
python orchestrator.py --step=1 --step=2 --url "<youtube_url>"

# Stage 1 only (download audio)
python orchestrator.py --step=1 --url "<youtube_url>" --audio audio.mp3

# Stage 2 only (transcribe)
python orchestrator.py --step=2 --audio audio.mp3 --model small --transcript transcript.txt
# Optionally provide language
python orchestrator.py --step=2 --audio audio.mp3 --model small --language en --transcript transcript.txt

# Stage 3 only (clean + chunk)
python orchestrator.py --step=3 --transcript transcript.txt --clean transcript_clean.txt

# Stage 4 only (summarize)
# Auto-discovers chunk_*.txt; falls back to --clean if available
python orchestrator.py --step=4 --summary summary.txt
```

### CLI Flags
- --url: required for step 1
- --audio: audio path (output of step 1 / input to step 2). Default: audio.mp3
- --model: Whisper model size for step 2 (tiny|base|small|medium|large). Default: small
- --language: optional language code (e.g. en). If omitted, stage 2 uses auto-detection and its default output path.
- --transcript: transcript file for step 2 output / step 3 input. Default: transcript.txt
- --clean: cleaned transcript output for step 3. Default: transcript_clean.txt
- --summary: final summary output for step 4. Default: summary.txt

## Individual Stages
- stage1_download_audio.py
  ```bash
  python stage1_download_audio.py <youtube_url> [output_filename.mp3]
  ```
  Notes: If FFmpeg is not installed, yt-dlp may save WebM audio into the given filename.

- stage2_transcribe.py
  ```bash
  python stage2_transcribe.py <audio_path> [model_size] [language] [out.txt]
  ```
  Example: `python stage2_transcribe.py audio.mp3 small en transcript.txt`

- stage3_clean_chunk.py
  ```bash
  python stage3_clean_chunk.py transcript.txt [out_clean.txt]
  ```
  Produces chunk_*.txt files in the working directory.

- stage4_summarize.py
  ```bash
  python stage4_summarize.py chunk_1.txt [chunk_2.txt ...] [out_summary.txt]
  ```

## Troubleshooting
- yt-dlp error: ffprobe and ffmpeg not found
  - Install FFmpeg: `sudo apt install -y ffmpeg`
- Stage 2 argument mismatch (language vs output)
  - When omitting --language in the orchestrator, stage 2 uses its default output path.
- GPU usage
  - Current scripts use CPU by default. To enable GPU, update stage2_transcribe.py/stage4_summarize.py to set device appropriately and ensure compatible CUDA drivers.

## Reference
- Source video example: [YouTube link](https://youtube.com/shorts/2vBHh7D804o?si=4TXVYzD7d3AV-Pg5)

## License
MIT
