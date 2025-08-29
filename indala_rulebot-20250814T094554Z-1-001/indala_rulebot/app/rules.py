import re
import string
from typing import List, Tuple
from sqlalchemy.orm import Session
from .models import Faq

_punct_tbl = str.maketrans({c: " " for c in string.punctuation})

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().translate(_punct_tbl)).strip()

def token_set(text: str) -> set:
    return set(normalize(text).split())

def score_match(user_text: str, faq: Faq) -> float:
    u_norm = normalize(user_text)
    u_tokens = token_set(user_text)
    score = 0.0

    # Keyword overlap
    if faq.keywords:
        kw = [k.strip().lower() for k in faq.keywords.split(",") if k.strip()]
        if kw:
            overlap = sum(1 for k in kw if k in u_tokens or k in u_norm)
            score += 2.5 * overlap

    # Patterns (pipe-separated phrases) exact substring boosts
    if faq.patterns:
        pats = [p.strip().lower() for p in faq.patterns.split("|") if p.strip()]
        for p in pats:
            if p and p in u_norm:
                score += 5.0

    # Category cue
    if faq.category:
        for cword in faq.category.lower().split():
            if cword in u_tokens:
                score += 0.5

    # Canonical question substring
    if faq.question and faq.question.lower() in u_norm:
        score += 6.0

    return score

def find_best_matches(db: Session, user_text: str, top_k: int = 3):
    faqs = db.query(Faq).all()
    scored = [(f, score_match(user_text, f)) for f in faqs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s in scored[:top_k] if s[1] > 0]