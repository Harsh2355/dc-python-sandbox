from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://harsh:q1K98r3X4N867dZCTPG3qQ@dc-python-sandbox-14916.7tt.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"
SQLALCHEMY_DATABASE_URL = "cockroachdb://harsh:q1K98r3X4N867dZCTPG3qQ@dc-python-sandbox-14916.7tt.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()