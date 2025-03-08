from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scrape import fetch_gateio_delisted, fetch_bybit_delisted, fetch_binance_delisted, exchanges
from cache import set_cached_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_cache():
    """Fetch data from all exchanges and store in Redis"""
    logger.info("Starting daily fetch of exchange data")
    
    for exchange in exchanges:
        try:
            name = exchange['name']
            url = exchange['url']
            
            if name == 'gateio':
                data = fetch_gateio_delisted(url)
            elif name == 'bybit':
                data = fetch_bybit_delisted(url)
            elif name == 'binance':
                data = fetch_binance_delisted(url)
            
            if data:
                set_cached_data(name, data)
                logger.info(f"Successfully cached data for {name}")
            else:
                logger.warning(f"No data retrieved for {name}")
                
        except Exception as e:
            logger.error(f"Error fetching data for {name}: {str(e)}")

def init_scheduler():
    """Initialize the scheduler to run at midnight"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_and_cache,
        trigger=CronTrigger(hour=0, minute=0),  # Run at midnight
        id='fetch_exchange_data',
        name='Fetch exchange data daily',
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler initialized")
    
    # Run immediately on startup
    fetch_and_cache()