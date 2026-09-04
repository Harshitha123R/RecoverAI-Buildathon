from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import sys
import os

# Allow backend to access files inside ml
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ml"))

from policy_engine import decide_action

from train_model import pipeline


app = FastAPI(
    title="RecoverAI API",
    description="AI-powered payment revenue recovery system"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class Payment(BaseModel):
    amount: float
    previous_successes: int
    previous_failures: int
    retry_count: int
    customer_age_days: int
    payment_method: str
    failure_type: str
    hour: int


@app.get("/")
def home():
    return {
        "message": "RecoverAI API is running!"
    }


@app.post("/predict")
def predict(payment: Payment):

    data = pd.DataFrame([{
        "amount": payment.amount,
        "previous_successes": payment.previous_successes,
        "previous_failures": payment.previous_failures,
        "retry_count": payment.retry_count,
        "customer_age_days": payment.customer_age_days,
        "payment_method": payment.payment_method,
        "failure_type": payment.failure_type,
        "hour": payment.hour
    }])

    probability = pipeline.predict_proba(data)[0][1]

    action = decide_action(
        probability,
        payment.retry_count,
        payment.failure_type
    )

    return {
        "recovery_probability": round(probability * 100, 2),
        "recommended_action": action
    }