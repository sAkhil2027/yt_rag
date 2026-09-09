import chromadb
from services.embadding import get_gemini_embedding, get_chroma_path

def user_query(user_input: str, video_id: str) -> list:
    client = chromadb.PersistentClient(path=get_chroma_path())
    collection = client.get_collection(video_id)
    try:
        query_embeddings = get_gemini_embedding(user_input, task_type="RETRIEVAL_QUERY")[0]
        results = collection.query(query_embeddings=[query_embeddings], n_results=7)
        raw_documents = results.get("documents", [[]])[0] if results else []
        combined_context = "\n\n---\n\n".join(raw_documents)
        return [combined_context]
    except Exception as e:
        raise Exception(f"Vector search failed: {e}")
