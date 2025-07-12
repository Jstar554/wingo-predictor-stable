import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# ✅ GitHub se LIVE data.json load karne wala URL
DATA_URL = "https://raw.githubusercontent.com/Jstar554/wingo-history-scraper/main/data.json"

@app.get("/")
def home():
    return {"message": "Stable predictor is running"}

@app.get("/predict")
def predict():
    try:
        response = requests.get(DATA_URL)
        data = response.json()

        if not data:
            return {"message": "No data found", "total": 0}

        # ✅ Example logic (last result ko read karke number show karo)
        last_result = data[0]
        number = last_result.get("number", "Unknown")
        big_small = "Big" if int(number) >= 5 else "Small"

        return {
            "message": "Prediction ready",
            "total": len(data),
            "last_period": last_result.get("period"),
            "last_number": number,
            "big_small": big_small
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
