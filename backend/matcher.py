# matcher.py

from sentence_transformers import SentenceTransformer, util

# Load model only once (efficient)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_similarity_score(resume_text: str, job_text: str) -> float:
    """
    Compute cosine similarity between resume and job using embeddings.
    """
    # Convert texts into dense vector representations
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    # Cosine similarity is a value between 0 and 1 (higher = more similar)
    similarity = util.cos_sim(resume_embedding, job_embedding)[0][0].item()

    return float(similarity)
