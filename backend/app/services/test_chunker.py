from app.services.chunker import Chunker

chunker = Chunker(
    chunk_size=1000,
    chunk_overlap=200,
)

text = """
Diabetes is a chronic medical condition that affects blood glucose levels.
The body either does not produce enough insulin or cannot effectively use
the insulin it produces. Maintaining healthy blood glucose levels is
important for preventing complications. Regular exercise, a balanced diet,
and appropriate medical treatment can help manage diabetes.
"""

chunks = chunker.chunk_text(text)

print(f"Number of chunks: {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)
