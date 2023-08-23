from sqlalchemy.engine import create_engine as create_mysql_engine
from os import getenv


def create_engine(user, password, host, database):
    url = "mysql+pymysql://{}:{}@{}/{}".format(
        user, password, host, database
    )
    engine = create_mysql_engine(url, echo=True)
    return engine


ENGINE = create_engine(
    user=getenv("DB_USER"),
    password=getenv("PASSWORD"),
    host=getenv("HOST"),
    database=getenv("DATABASE")
)


