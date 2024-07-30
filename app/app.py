from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chatbot import Chatbot
from vectorstore import get_books, search_books

app = FastAPI()
chatbot = Chatbot()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Mount the frontend directory to serve static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

class ChatRequest(BaseModel):
    session_id: str
    query: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = chatbot.handle_query(request.session_id, request.query)
    return ChatResponse(response=response)

@app.get("/books")
async def list_books():
    books = get_books()
    return JSONResponse(content={"books": books})

@app.get("/books/search/")
async def search_books_route(q: str):
    books = search_books(q)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return JSONResponse(content={"books": books})

@app.get("/chat/{session_id}")
async def chat(session_id: str, query: str):
    async def event_generator():
        response = chatbot.handle_query(session_id, query)
        yield f"data: {response}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    if session_id not in chatbot.store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    history = chatbot.store[session_id].messages
    return JSONResponse(content={"history": [{"type": type(message).__name__, "content": message.content} for message in history]})

@app.get("/recommendations")
async def get_recommendations(query: str):
    recommendations = chatbot.get_recommendations(query)
    return JSONResponse(content={"recommendations": recommendations})

@app.get("/health_check")
async def health_check():
    return JSONResponse(content={"status": "ok"})
