import os

with open("private.pem") as f:
  PRIVATE_KEY = f.read()

class Config:
    try:
        DB_USER = os.environ["POSTGRES_USER"]
        DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
        DB_HOST = os.environ["POSTGRES_HOST"]
        DB_PORT = os.environ["POSTGRES_PORT"]
        DB_NAME = os.environ["POSTGRES_DB"]
    except KeyError as e:
        raise RuntimeError(f"Missing required environment variable: {e}")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=disable"
        )
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRIVATE_KEY = PRIVATE_KEY