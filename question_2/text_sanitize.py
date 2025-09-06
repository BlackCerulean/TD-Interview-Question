import argparse
from collections import Counter
from google.cloud import storage
import os
import tempfile

def text_sanitizing(text):
    """Read text and return lower-case characters."""
    # String manipulation: lowercase + strip punctuation
    cleaned = text.lower().replace("\t", "____")
    return cleaned

def text_statistics(text):
    """Read text and return statistic of the text."""
    letters = ""
    for ch in text:
        if ch.isalpha():
            letters += ch.lower()
    return Counter(letters)

def write_local(target: str, sanitized: str, stats: Counter):
    """Write sanitized text and stats to local file."""
    with open(target, "w", encoding="utf-8") as f:
        f.write("=== Sanitized Text ===\n")
        f.write(sanitized + "\n\n")
        f.write("=== Alphabet Statistics ===\n")
        for letter, count in sorted(stats.items()):
            f.write(f"{letter}: {count}\n")
    print(f"Results written locally to: {target}")


def write_gcs(target: str, sanitized: str, stats: Counter):
    """Write sanitized text and stats to Google Cloud Storage."""
    if not target.startswith("gs://"):
        raise ValueError("Target must start with gs:// for GCS writes")

    path = target[5:]  # remove gs://
    bucket_name, blob_name = path.split("/", 1)

    # Write to temp file first
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
        tmp.write("=== Sanitized Text ===\n")
        tmp.write(sanitized + "\n\n")
        tmp.write("=== Alphabet Statistics ===\n")
        for letter, count in sorted(stats.items()):
            tmp.write(f"{letter}: {count}\n")
        tmp_path = tmp.name

    # Upload to GCS
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(tmp_path)

    os.remove(tmp_path)
    print(f"Results uploaded to GCS: {target}")

def process_file(source, target):
    # Read input text
    with open(source, "r", encoding="utf-8") as f:
        raw_text = f.read()
    
    # Sanitize text
    sanitized = text_sanitizing(raw_text)

    # Count alphabet frequency
    stats = text_statistics(sanitized)

    # Print results to console
    print("=== Sanitized Text ===")
    print(sanitized)
    print("\n=== Alphabet Statistics ===")
    for letter, count in sorted(stats.items()):
        print(f"{letter}: {count}")

    if target.startswith("gs://"):
        write_gcs(target, sanitized, stats)
    else:
        write_local(target, sanitized, stats)

def main():
    parser = argparse.ArgumentParser(description="File processor with local or GCS output")
    parser.add_argument("--source", required=True, help="Path to input file (local only)")
    parser.add_argument("--target", required=True, help="Path to output file (local path or gs://bucket/path)")
    args = parser.parse_args()

    process_file(args.source, args.target)

if __name__ == "__main__":
    main()