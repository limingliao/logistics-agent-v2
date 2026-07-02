from app.database.db import Base
from app.database.db import engine

# 导入所有模型
import app.database.models


def init_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()