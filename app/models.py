
from app.database import Base
from sqlalchemy import Column, Integer, String, Float
from app.database import engine


class Problem(Base):
    __tablename__ = "Problems"

    id = Column(Integer , primary_key= True)
    slug = Column(String, unique =True)
    title = Column(String)
    status = Column(String)


    
    
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully!")