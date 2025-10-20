# stage4_summarize.py
import sys
from transformers import pipeline

def summarize_chunks(chunk_files, model_name="sshleifer/distilbart-cnn-12-6", max_length=180, min_length=40):
    summarizer = pipeline("summarization", model=model_name, device=-1)  # device=-1 -> CPU
    chunk_summaries = []
    for cf in chunk_files:
        text = open(cf, "r", encoding="utf-8").read()
        # the pipeline returns a list of dicts, pick the 'summary_text'
        out = summarizer(text, max_length=max_length, min_length=min_length, truncation=True)[0]["summary_text"]
        chunk_summaries.append(out.strip())
        print(f"Summarized {cf} -> {len(out.split())} words")
    return chunk_summaries

def hierarchical_combine(chunk_summaries, final_model="sshleifer/distilbart-cnn-12-6"):
    summarizer = pipeline("summarization", model=final_model, device=-1)
    combined_text = " ".join(chunk_summaries)
    final = summarizer(combined_text, max_length=300, min_length=80, truncation=True)[0]["summary_text"]
    return final.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stage4_summarize.py chunk_1.txt chunk_2.txt ... [out_summary.txt]")
        sys.exit(1)
    chunk_files = sys.argv[1:-1] if len(sys.argv) > 2 else [sys.argv[1]]
    out_file = sys.argv[-1] if len(sys.argv) > 2 else "summary.txt"
    chunk_summaries = summarize_chunks(chunk_files)
    final_summary = hierarchical_combine(chunk_summaries)
    open(out_file, "w", encoding="utf-8").write(final_summary)
    print(f"Final summary saved to {out_file}")
    print("\n---SUMMARY---\n")
    print(final_summary)
