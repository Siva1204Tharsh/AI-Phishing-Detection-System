from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from utils.remediation import get_remediation_action
import os
import pandas as pd
import datetime

app = FastAPI()

model = joblib.load("model/phishing_model.pkl")
LOG_FILE = "../logs/log.csv"

class TextInput(BaseModel):
    message: str

def log_message(message, prediction):
    timestamp = datetime.datetime.now().isoformat()
    log_data = pd.DataFrame([[timestamp, message, prediction]], columns=["time", "message", "phishing"])
    if os.path.exists(LOG_FILE):
        log_data.to_csv(LOG_FILE, mode='a', header=False, index=False)
    else:
        log_data.to_csv(LOG_FILE, index=False)

@app.post("/predict")
def predict(data: TextInput):
    pred = model.predict([data.message])[0]
    log_message(data.message, pred)
    return {"phishing": bool(pred)}

@app.post("/predict_remediate")
def predict_and_remediate(data: TextInput):
    pred = model.predict([data.message])[0]
    log_message(data.message, pred)
    remediation = get_remediation_action(pred)
    return {
        "phishing": bool(pred),
        "remediation": remediation
    }

@app.get("/logs")
def get_logs():
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        return df.tail(10).to_dict(orient="records")
    return []


### create a test endpoint