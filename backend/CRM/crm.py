from fastapi import  APIRouter, Depends, HTTPException
from textblob import TextBlob
from database.repository.feedbackLog import feedbackInstance
from database.schemas.feedback import DocumentLog
from database import schemas, database
from backend.extraction_service.app.utils import currentuser
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from backend.cache.redis_client import redis_client
import json

get_db = database.get_db
get_feedback_db = database.get_feedback_db


router = APIRouter(tags=['CRM'])


def get_sentiment(text: str):
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



@router.post("/api/feedback")
def handle_review(
    review: str,
    feedback_db: Session = Depends(database.get_feedback_db),
    current_user: schemas.client.Client = Depends(currentuser.get_current_client)
):
    redis_key = f"doc_context:{current_user.email}"

    cached = redis_client.get(redis_key)

    if not cached:
        raise HTTPException(
            status_code=400,
            detail="Please upload a document first."
        )

    context = json.loads(cached)

    feedbacklog = DocumentLog(
        UserID=current_user.email,
        ocr_text=context["ocr_text"],
        doc_type=context["doc_type"],
        review=review,
        date=context["date"]
    )

    sentiment = get_sentiment(review)
    reply = generate_reply(sentiment, current_user.name)

    if sentiment == "Negative":
        feedbackInstance(feedbacklog, feedback_db)

    redis_client.delete(redis_key)

    return {
        "sentiment": sentiment,
        "reply": reply
    }




