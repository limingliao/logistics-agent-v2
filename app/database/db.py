import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path

# 获取当前文件目录
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = Path(__file__).resolve().parent.parent

# 强制绝对路径
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)

# DB_PATH = os.path.join(DB_DIR, "orders.db")
DB_PATH = BASE_DIR / "data" / "orders.db"


DATABASE_URL = f"sqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# print("========== DATABASE INFO ==========")
# print("DB URL:", DATABASE_URL)
# print("ABS PATH:", os.path.abspath("./app/data/orders.db"))
# print("===================================")

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)