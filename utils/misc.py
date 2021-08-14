# python shell
from db import redis_db


redis_db.get('key')  # Получить значение по ключу
redis_db.set('key', 'value')  # Положить значение по ключу
redis_db.expire('key', 10)  # Установить время жизни ключа в секундах
# А можно последние две операции сделать за один запрос к Redis.
redis_db.setex('key', 10, 'value')  # Положить значение по ключу с ограничением времени жизни в секундах