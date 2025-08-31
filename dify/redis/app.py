import os
import redis

def test_redis_connection():
    host = os.environ.get("REDIS_HOST", "localhost")
    port = int(os.environ.get("REDIS_PORT", "6379"))
    username = os.environ.get("REDIS_USERNAME", None)
    password = os.environ.get("REDIS_PASSWORD", None)

    print(f"Connecting to Redis at {host}:{port}...")

    try:
        r = redis.Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            decode_responses=True
        )

        # Test write
        r.set('test_key', 'Hello Redis!')

        # Test read
        value = r.get('test_key')
        print(f"Redis is working! Stored value: {value}")

        # Clean up
        r.delete('test_key')
        print("Cleanup done.")

    except redis.ConnectionError as e:
        print(f"Redis connection failed: {e}")
    except redis.AuthenticationError as e:
        print(f"Redis authentication failed: {e}")

if __name__ == "__main__":
    test_redis_connection()
