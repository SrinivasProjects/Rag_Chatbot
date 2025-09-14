# RAG Chatbot

A cutting-edge Retrieval-Augmented Generation (RAG) chatbot that lets you upload PDF documents and ask natural language questions, delivering instant, context-aware answers. Built with FastAPI and a stunning HTML/CSS/JavaScript frontend, this is one of the best AI applications for document understanding, productivity, and knowledge management across

![RAG Chatbot Screenshot](photo.png)


[Watch video](video.mp4)

## How This Is Useful

- **Document Understanding:** Instantly ask questions about any uploaded PDF and get accurate, context-aware answers.
- **Productivity:** Save time searching through large documents—just ask and get relevant information.
- **Knowledge Management:** Useful for students, researchers, and professionals to extract insights from reports, manuals, or books.
- **Conversational Experience:** Chat-like interface makes interacting with documents intuitive and engaging.
- **Customizable:** Easily adapt for different domains (legal, medical, education, etc.) by changing models or data sources.

## Features
- Upload PDF documents and index them for semantic search
- Ask questions about uploaded documents
- Chat-like UI with message bubbles and bot thinking animation
- Uses OpenAI and Pinecone (or other vector DBs)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SrinivasProjects/Rag_Chatbot.git
   cd Rag_Chatbot
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and add your API keys:
     ```
     OPENAI_API_KEY=your-openai-key-here
     PINECONE_API_KEY=your-pinecone-key-here
     SERVICE3_API_KEY=your-service3-key-here
     SERVICE4_API_KEY=your-service4-key-here
     ```

## Running the App

1. **Start the FastAPI server:**
   ```bash
   python -m uvicorn main:app --reload
   ```

2. **Open the frontend:**
   - Visit [http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html) in your browser.

## Usage
- Click the PDF icon or "Upload PDF" button to upload a document.
- Ask questions in the chat input; answers will appear as chat bubbles.
- Use suggestion chips for quick queries.

## Customization
- Edit `static/style.css` for UI changes.
- Update backend logic in `main.py` and `utils/` as needed.

## License
MIT
