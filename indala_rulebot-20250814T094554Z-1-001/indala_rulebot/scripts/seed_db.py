import csv
from pathlib import Path
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app.models import Faq

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "faq_template.csv"

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        db.query(Faq).delete()
        db.commit()

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for r in rows:
            faq = Faq(
                category=r.get("category","").strip(),
                question=r.get("question","").strip(),
                answer=r.get("answer","").strip(),
                patterns=r.get("patterns","").strip(),
                keywords=r.get("keywords","").strip(),
                tags=r.get("tags","").strip(),
            )
            if faq.question and faq.answer:
                db.add(faq)
        db.commit()
        print(f"Seeded {db.query(Faq).count()} FAQs from {CSV_PATH.name}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()