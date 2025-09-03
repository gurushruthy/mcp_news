import chromadb
from chromadb.config import Settings
from models.news import NewsItem
from dotenv import load_dotenv
import os
from chromadb.utils import embedding_functions

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)
os.environ["CHROMA_TELEMETRY_DISABLED"] = "1"
Openai_model=os.getenv("OPENAI_EMBED_MODEL","text-embedding-3-small")
openai_ef=embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],
    model_name=Openai_model,
    )

client=chromadb.PersistentClient(path=".chroma")

collection=client.get_or_create_collection(name="bcc_news",embedding_function=openai_ef,)

def upsert(items:list[NewsItem]):
    if not items:
        return 0
    ids, documents, metadatas = [], [], []
    ids=[i.id for i in items]
    documents=[f"{i.title}. {i.description}" for i in items]
    for i in items:
        metadatas.append({
            "id": i.id,
            "title": i.title or "",
            "description": i.description or "",
            "url": i.url or "",
            "source": i.source or "BBC",
            "published_at": (
                i.published_at.isoformat()
                if getattr(i, "published_at", None) else None
            ),
        })

    collection.upsert(ids=ids,documents=documents, metadatas=metadatas)
    return len(ids)

def latest(limit:int):
    got=collection.get()
    metas=got.get("metadatas",[])
    metas.sort(key=lambda x:x["published_at"],reverse=True)
    return metas[:limit]

def semantic_search(query,k:int=5):
    res=collection.query(query_texts=[query],n_results=k)
    return res["metadatas"][0] if res and "metadatas" in res else []


    
