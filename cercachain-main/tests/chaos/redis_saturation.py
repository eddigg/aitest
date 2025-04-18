import redis
import time

def simulate_redis_storm():
    r = redis.Redis()
    try:
        # Flood Redis with data
        for i in range(10000):
            r.set(f"key{i}", "x" * 1000)
        print("Redis saturation complete")
        
        # Test read operations under load
        start_time = time.time()
        for i in range(100):
            r.get(f"key{i}")
        end_time = time.time()
        print(f"Read latency under load: {end_time - start_time:.2f}s")
        
        # Cleanup
        r.flushall()
    except redis.RedisError as e:
        print(f"Redis error during chaos test: {e}")
    except Exception as e:
        print(f"Unexpected error during chaos test: {e}")