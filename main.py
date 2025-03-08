from fastapi import FastAPI
from scrape import exchanges
from cache import get_cached_data
from scheduler import init_scheduler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_scheduler()

@app.get("/api/delisted/{exchange}")
async def get_delisted(exchange: str):
    # Find the matching exchange
    exchange_data = next((ex for ex in exchanges if ex['name'] == exchange), None)
    if not exchange_data:
        return {"error": f"Exchange '{exchange}' not found"}
    
    # Get data from cache
    data = get_cached_data(exchange)
    if data is None:
        return {"error": "No data available"}
        
    return data
