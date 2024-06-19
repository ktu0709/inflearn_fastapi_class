from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3307/todos"


engine = create_engine(DATABASE_URL,echo=True)
sessionfactory = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    session = sessionfactory()
    try:
        yield session
    finally:
        session.close()


#terminal 실행
'''
from sqlalchemy import select
session = sessionfactory()
session.scalar(select(1))
list(session.scalars(select(ToDo)))
'''