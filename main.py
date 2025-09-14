
import dotenv; dotenv.load_dotenv()
from fastapi import FastAPI, UploadFile, File, Form
from utils.pdf_utils import extract_text
from utils.chunk_utils import chunk_text
from utils.pinecone_utils import init_pinecone, upsert_chunks
from utils.rag_utils import query_pinecone, generate_answer

from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app):
    init_pinecone()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        import fitz  # PyMuPDF
        contents = await file.read()
        print("Uploaded file size:", len(contents))
        with open("debug_uploaded.pdf", "wb") as f:
            f.write(contents)
        if not contents:
            return {"error": "Uploaded file is empty."}
        doc = fitz.open(stream=contents, filetype="pdf")
        full_text = "\n".join([page.get_text() for page in doc])  # type: ignore
        chunks = chunk_text(full_text)
        upsert_chunks(chunks)
        return {"status": "PDF uploaded and indexed"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    chunks = query_pinecone(question)
    context = "\n".join(chunks)
    answer = generate_answer(context, question)
    return {"answer": answer}
