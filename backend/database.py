from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:Anshu%4099@localhost/compliance_ai"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)