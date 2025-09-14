import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import google.generativeai as genai  # type: ignore

load_dotenv()

model = SentenceTransformer('all-MiniLM-L6-v2')
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def query_pinecone(query: str, top_k=5):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    if not INDEX_NAME:
        raise ValueError("PINECONE_INDEX_NAME is not set.")
    index = pc.Index(INDEX_NAME)
    query_vector = model.encode(query).tolist()
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)  # type: ignore
    return [match['metadata']['text'] for match in results['matches']]  # type: ignore

def generate_answer(context, question):
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # type: ignore
    preferred_models = [
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro"
    ]
    model_name = preferred_models[0]  # Default to first preferred
    try:
        model = genai.GenerativeModel(model_name)  # type: ignore
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # If model not found or deprecated, list available models and try again
        if 'model not found' in str(e).lower() or 'deprecated' in str(e).lower() or '404' in str(e):
            try:
                models = genai.list_models()  # type: ignore
                available_models = [m.name for m in models if 'generateContent' in getattr(m, 'supported_generation_methods', [])]
                # Prefer recommended models if available
                for preferred in preferred_models:
                    if preferred in available_models:
                        model_name = preferred
                        break
                else:
                    if available_models:
                        model_name = available_models[0]
                    else:
                        return "No supported Gemini models available. Please check your API access."
                model = genai.GenerativeModel(model_name)  # type: ignore
                response = model.generate_content(prompt)
                return response.text
            except Exception as e2:
                return f"Gemini API error: {str(e2)}. Available models: {available_models if 'available_models' in locals() else 'unknown'}"
        return f"Gemini API error: {str(e)}"
