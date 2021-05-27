from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

_ENGINE = create_engine(
    "{engine}://{username}:{password}@{host}:{port}/{db_name}".format(
        engine="postgresql",
        username="iamos",
        password="iamos123",
        host="postgres",
        port="5432",
        db_name="wantedlabs",
    ),
    convert_unicode=False,
    encoding="utf-8",
    max_overflow=10,
    pool_size=8,
    pool_recycle=3600,
    pool_timeout=10,
    connect_args={
        "sslmode": "allow",
        "application_name": "wantedlabs_backend",
    },
)

# Local Database
# _ENGINE = create_engine(
#     "{engine}://{username}:{password}@{host}:{port}/{db_name}".format(
#         engine="postgresql",
#         username="iamos",
#         password="iamos123",
#         host="localhost",
#         port="5432",
#         db_name="postgres",
#     ),
#     convert_unicode=False,
#     encoding="utf-8",
#     max_overflow=10,
#     pool_size=8,
#     pool_recycle=3600,
#     pool_timeout=10,
#     connect_args={
#         "sslmode": "allow",
#         "application_name": "wantedlabs_backend",
#     },
# )

session = scoped_session(sessionmaker(bind=_ENGINE, autocommit=False))
Base = declarative_base()
