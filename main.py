from fastapi import FastAPI
from scrape import fetch_delisted, exchanges  # Import your scraping function


app = FastAPI()

@app.get("/api/delisted/{exchange}")
async def scrape(exchange: str):
    data = fetch_delisted(f'{exchanges[0].get(f"url")}')  # Call your scraping function
    return data               # FastAPI automatically serializes to JSON

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
