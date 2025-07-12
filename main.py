import aiohttp, asyncio
from fastapi import FastAPI, Query
from starlette.responses import JSONResponse

app = FastAPI()
data_cache = []

async def fetch_data():
    global data_cache
    url = "https://api.66lottery20.com/api/game/periods?game_id=9&size=1000&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.66lottery20.com/"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    result = await response.json()
                    new_data = []
                    for item in result.get("data", []):
                        num = int(item["number"])
                        new_data.append({
                            "period": item["period"],
                            "number": num,
                            "color": item["color"],
                            "bigsmall": "Big" if num >= 5 else "Small"
                        })
                    data_cache = new_data
                    print("✅ Data updated:", len(data_cache))
                else:
                    print("⚠️ API returned non-200 status")
    except Exception as e:
        print("❌ Error fetching data:", str(e))

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(schedule_fetch())

async def schedule_fetch():
    while True:
        await fetch_data()
        await asyncio.sleep(90)

@app.get("/")
def root():
    return {"message": "Stable predictor is running", "total": len(data_cache)}

@app.get("/data.json")
def get_data():
    return JSONResponse(content=data_cache or [])

@app.get("/predict")
def predict(period: str = Query(...)):
    if not data_cache:
        return {
            "period": period,
            "predicted_number": 5,
            "bigsmall": "Big",
            "color": "Red"
        }
    recent = [d["number"] for d in data_cache[:10]]
    pred_number = int(round(sum(recent) / len(recent)))
    pred_number = max(0, min(9, pred_number))
    return {
        "period": period,
        "predicted_number": pred_number,
        "bigsmall": "Big" if pred_number >= 5 else "Small",
        "color": ["Red", "Green", "Violet"][pred_number % 3]
    }
