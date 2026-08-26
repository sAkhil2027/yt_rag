import chromadb
from services.embadding import get_model
from config import HF_TOKEN

def user_query(user_niput: str, video_id: str):
    # connect to local DB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(video_id)

    try:
        model = get_model()
        query_embaddings = model.encode(user_niput).tolist()

        # Retrieve top 7 most relevant 800-char chunks across the entire video transcript
        results = collection.query(
            query_embeddings=[query_embaddings],
            n_results=7
        )
        
        raw_documents = results["documents"][0] if results and "documents" in results and results["documents"] else []
        
        # Combine retrieved chunks into a cohesive context block
        combined_context = "\n\n---\n\n".join(raw_documents)
        print(f"Retrieved {len(raw_documents)} transcript chunks ({len(combined_context)} chars) for query: '{user_niput}'")

        return [combined_context]

    except Exception as e:
        raise Exception(f"error: {e}")
