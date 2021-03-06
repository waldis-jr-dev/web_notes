import os
from heroku_redis.redis_funcs import Redis

if __name__ == '__main__':
    import set_env_values

redis = Redis(os.getenv('REDIS_URL'))

redis.delete_old_tokens()

if __name__ == '__main__':
    print(redis.all_keys())
