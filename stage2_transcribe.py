# stage2_transcribe.py
import sys
from faster_whisper import WhisperModel

def transcribe(audio_path, model_size="small", language=None, output_txt="transcript.txt"):
    # model_size options: "tiny", "base", "small", "medium", "large"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5, language=language)
    full_text = []
    with open(output_txt, "w", encoding="utf-8") as f:
        for segment in segments:
            text = segment.text.strip()
            f.write(text + "\n")
            full_text.append(text)
    print(f"Transcription saved to {output_txt}")
    return " ".join(full_text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stage2_transcribe.py <audio.mp3> [model_size] [language] [out.txt]")
        sys.exit(1)
    audio = sys.argv[1]
    size = sys.argv[2] if len(sys.argv) > 2 else "small"
    lang = sys.argv[3] if len(sys.argv) > 3 else None
    out = sys.argv[4] if len(sys.argv) > 4 else "transcript.txt"
    transcribe(audio, model_size=size, language=lang, output_txt=out)
