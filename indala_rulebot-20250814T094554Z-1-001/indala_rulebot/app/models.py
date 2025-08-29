from sqlalchemy import Column, Integer, String, Text
from .db import Base

class Faq(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    patterns = Column(Text, nullable=True)   # pipe-separated phrases
    keywords = Column(Text, nullable=True)   # comma-separated words
    tags = Column(Text, nullable=True)