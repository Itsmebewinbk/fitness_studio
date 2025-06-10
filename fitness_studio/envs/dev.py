from decouple import config
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = "/api_fitness_studio/api/static/"
MEDIA_URL = "/api_fitness_studio/api/media/"

DATABASES = {
    "default": {
        "ENGINE": "dj_db_conn_pool.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": 5432,
        "POOL_OPTIONS": {
            "POOL_SIZE": 10,  
            "MAX_OVERFLOW": 20,  
            "RECYCLE": 24 * 60 * 60, 
            "POOL_TIMEOUT": 30, 
            "POOL_PRE_PING": True,
        },
    }
}
