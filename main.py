from fastapi import FastAPI
from scrape import fetch_gateio_delisted, fetch_bybit_delisted, fetch_binance_delisted, exchanges  # Import your scraping function


app = FastAPI()

@app.get("/api/delisted/{exchange}")
async def scrape(exchange: str):
    # Find the matching exchange URL
    exchange_data = next((ex for ex in exchanges if ex['name'] == exchange), None)
    if not exchange_data:
        return {"error": f"Exchange '{exchange}' not found"}
    
    func_name = f'fetch_{exchange}_delisted'
    if func_name not in globals():
        return {"error": f"Scraper for '{exchange}' not implemented"}
        
    return globals()[func_name](exchange_data['url'])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
