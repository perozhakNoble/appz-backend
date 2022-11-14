from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBClient:
    current_session = None

    def __init__(
            self,
            host='postgres',
            port=5432,
            user='user',
            password='password',
            db_name='expenses_reports'
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.SessionLocal = None

    def connect(self):
        engine = create_engine(
            f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


db_client = DBClient()
db_client.connect()
