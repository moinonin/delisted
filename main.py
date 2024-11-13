from fastapi import FastAPI
from scrape import fetch_gateio_delisted, fetch_bybit_delisted, exchanges  # Import your scraping function


app = FastAPI()

@app.get("/api/delisted/{exchange}")
async def scrape(exchange: str):
    func_name = f'fetch_{exchange}_delisted'
    return globals()[func_name](f"{exchanges[0].get('url')}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
