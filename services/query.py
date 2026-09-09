import chromadb
from services.embadding import get_gemini_embedding, get_chroma_path, get_collection_name

def user_query(user_input: str, video_id: str) -> list:
    """
    Queries ChromaDB for the top 7 most relevant transcript chunks matching user_input.
    Returns [combined_context] formatted for LLM prompts and compatible with app.py.
    """
    client = chromadb.PersistentClient(path=get_chroma_path())
    
    collection_name = get_collection_name(video_id)

    # Safely retrieve collection with fallback to legacy raw video_id
    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        try:
            collection = client.get_collection(name=video_id)
        except Exception:
            raise ValueError(
                f"No transcript found for Video ID '{video_id}'. "
                "Please ensure the video has been processed and ingested first."
            )

    try:
        # Generate query vector with explicitly defined RETRIEVAL_QUERY task type
        try:
            query_embeddings = get_gemini_embedding(user_input, task_type="RETRIEVAL_QUERY")[0]
        except TypeError:
            query_embeddings = get_gemini_embedding(user_input)[0]

        # Query top 7 chunks
        results = collection.query(
            query_embeddings=[query_embeddings],
            n_results=7
        )

        raw_documents = results.get("documents", [[]])[0] if results else []
        
        if not raw_documents:
            print(f"[WARN] No context retrieved for query: '{user_input}'")
            return [""]

        # Combine retrieved chunks into a unified context block
        combined_context = "\n\n---\n\n".join(raw_documents)
        print(f"[QUERY SUCCESS] Retrieved {len(raw_documents)} chunks ({len(combined_context)} chars) for query: '{user_input}'")

        return [combined_context]

    except Exception as e:
        print(f"[ERROR] Vector query failed for video_id {video_id}: {e}")
        raise RuntimeError(f"Vector search failed: {e}") from e
