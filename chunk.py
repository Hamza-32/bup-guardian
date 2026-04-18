def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

# Load the extracted text (no need to OCR again)
with open(r"e:\Semester8\AI\Lab\Project\bup-guardian\extracted_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_text(text)

print(f"Total chunks: {len(chunks)}")
print(f"\nFirst chunk preview:\n{chunks[0]}")

# Save chunks for next stage
import json
with open(r"e:\Semester8\AI\Lab\Project\bup-guardian\chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False)

print("\nChunks saved to chunks.json")