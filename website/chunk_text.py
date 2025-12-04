from pathlib import Path
import re

def chunk_text(text, chunk_size=2500, overlap=300):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap

    return chunks

# Load extracted text
text_file = Path("textbook.txt")
text = text_file.read_text(encoding="utf-8")

# Clean extra spacing
text = re.sub(r"\n\s*\n+", "\n\n", text)

chunks = chunk_text(text)

# Save chunks
out_dir = Path("chunks")
out_dir.mkdir(exist_ok=True)

for i, ch in enumerate(chunks):
    (out_dir / f"chunk_{i:03}.txt").write_text(ch, encoding="utf-8")

print(f"Created {len(chunks)} chunks inside /chunks folder.")

