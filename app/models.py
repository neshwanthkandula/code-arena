from app.database import Base, engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String,default="normal")
    contest_id = Column(String, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_slug = Column(String, ForeignKey("problems.slug"), nullable=False)

    source_code = Column(Text, nullable=False)
    language_id = Column(Integer, nullable=False)
    verdict = Column(String)
    contest_id = Column(String , nullable=True)
    points = Column(String , default=0)

    user = relationship("User")
    problem = relationship("Problem")


class Contest(Base):
    __tablename__ = "contest"

    contest_id = Column(String, primary_key=True)
    start_Time = Column(String, nullable=False)
    Duration =Column(String, nullable=False)

class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer , primary_key=True)
    contest_id = Column(String , nullable=False)
    user_id = Column(String)
    total_points = Column(Integer)
    rank =Column(Integer)

    

