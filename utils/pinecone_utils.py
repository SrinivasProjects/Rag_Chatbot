from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer('all-MiniLM-L6-v2')

def init_pinecone():
    PINECONE_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    if not PINECONE_KEY or not PINECONE_ENV or not INDEX_NAME:
        raise ValueError("Pinecone environment variables are not set.")
    pc = Pinecone(api_key=PINECONE_KEY)
    region = PINECONE_ENV.split('-')[-1] if '-' in PINECONE_ENV else PINECONE_ENV
    # Check if index exists
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region=region  # e.g., 'us-east-1'
            )
        )
    return pc

def upsert_chunks(chunks):
    PINECONE_KEY = os.getenv("PINECONE_API_KEY")
    INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    if not PINECONE_KEY or not INDEX_NAME:
        raise ValueError("Pinecone environment variables are not set.")
    pc = Pinecone(api_key=PINECONE_KEY)
    index = pc.Index(INDEX_NAME)
    vectors = [(f"id-{i}", model.encode(chunk).tolist(), {"text": chunk}) for i, chunk in enumerate(chunks)]
    index.upsert(vectors)
