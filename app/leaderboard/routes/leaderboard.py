from fastapi import FastAPI,APIRouter,Depends
from app.leaderboard.function import get_leaderboard, get_user_rank,add_points
from app.auth.middleware import get_user
from sqlalchemy.orm import Session
from app.database import sessionLocal

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/{contest_id}/me")
def get_rank(contest_id: str,user_id : str = Depends(get_user), db: Session = Depends(get_db)):
    rank = get_user_rank(contest_id,user_id,db )
    
    return rank

@router.get("/{contest_id}")
def leaderboard(contest_id: str, db: Session = Depends(get_db)):
    return get_leaderboard(contest_id, db)