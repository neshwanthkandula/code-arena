from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL ='postgresql://neondb_owner:npg_JoscRx3mU1Vu@ep-calm-recipe-ah1jr1c4-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

engine = create_engine(DATABASE_URL)
sessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()