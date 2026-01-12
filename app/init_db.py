# init_db.py
from app.database import Base, engine
from app.models import User, Problem, Submission

def init_database():
    Base.metadata.create_all(engine)
    print("Database tables created!")

if __name__ == "__main__":
    init_database()