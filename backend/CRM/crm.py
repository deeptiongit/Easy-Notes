from fastapi import  APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from textblob import TextBlob
from database.repository.feedbackLog import feedbackInstance
from database.schemas.feedback import DocumentLog
from database import schemas, database
from backend.extraction_service.app.utils import oauth2
from sqlalchemy.orm import Session
import os



router = APIRouter(prefix="/crm", tags=['CRM'])

@router.get("/")
def root():
    return {"message": "CRM Service API", "version": "1.0.0"}

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "crm-service"}

@router.post('/api/sentiment')
def get_sentiment(text: str, current_user: schemas.Client = Depends(oauth2.get_current_user)):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def generate_reply(sentiment: str, username: str):
    if sentiment == "Positive":
        return f"Thank you so much for your kind feedback, {username}! "
    elif sentiment == "Neutral":
        return f"Thanks for your feedback, {username}. We'll continue to improve!"
    else:
        return f"We're sorry to hear that, {username}. We'll work to resolve this immediately. "

@router.post('/api/review')
async def handle_review(
    request: Request, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.Client = Depends(oauth2.get_current_user)
):
    data = await request.json()
    username = data.get('username')
    review = data.get('review')

    feedbacklog = DocumentLog(
        UserID=username,
        document_id=data.get('document_id'),
        ocr_text=data.get('product_name'),
        doc_type=data.get('doc_type'),
        review=review,
        date=data.get('DataTime')
    )

    sentiment = get_sentiment(review, current_user)
    reply = generate_reply(sentiment, username)

    if sentiment == "Negative":
        feedbackInstance(feedbacklog, db)

    return JSONResponse({
        "sentiment": sentiment,
        "reply": reply
    })

