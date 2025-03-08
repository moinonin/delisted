import redis
import json
from datetime import timedelta

redis_client = redis.Redis(
    host='redis',  # This will be our Redis service name in docker-compose
    port=6379,
    db=0,
    decode_responses=True
)

def get_cached_data(exchange: str) -> list:
    """Get data from Redis cache"""
    data = redis_client.get(f"delisted:{exchange}")
    return json.loads(data) if data else None

def set_cached_data(exchange: str, data: list):
    """Store data in Redis cache with 24-hour expiration"""
    redis_client.setex(
        f"delisted:{exchange}",
        timedelta(hours=24),
        json.dumps(data)
    )