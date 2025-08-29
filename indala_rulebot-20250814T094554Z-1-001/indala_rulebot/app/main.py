from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from .db import Base, engine, get_db
from .models import Faq
from .schemas import ChatIn, ChatOut, FaqOut
from .rules import find_best_matches

app = FastAPI(title="Indala Rule-Based Chatbot")

# CORS (restrict to your domain in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatOut)
def chat(payload: ChatIn, db: Session = Depends(get_db)):
    matches = find_best_matches(db, payload.text, top_k=3)
    if not matches:
        return ChatOut(
            reply=(
                "I couldn't find that. Try keywords like 'admission', 'fees', 'hostel', 'sports', or 'departments'. "
                "For full details, please check the official website."
            ),
            matches=[]
        )
    top_faq, top_score = matches[0]
    out_matches: List[FaqOut] = [
        FaqOut(id=f.id, category=f.category, question=f.question, answer=f.answer, score=s)
        for f, s in matches
    ]
    return ChatOut(reply=top_faq.answer, matches=out_matches)

@app.get("/faq/search", response_model=List[FaqOut])
def faq_search(q: str, db: Session = Depends(get_db)):
    matches = find_best_matches(db, q, top_k=10)
    return [
        FaqOut(id=f.id, category=f.category, question=f.question, answer=f.answer, score=s)
        for f, s in matches
    ]