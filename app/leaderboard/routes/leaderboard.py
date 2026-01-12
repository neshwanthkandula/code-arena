from fastapi import FastAPI,APIRouter,Depends
from app.leaderboard.function import get_leaderboard, get_user_rank,add_points
from app.auth.middleware import get_user

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/me")
def get_my_rank(user_id : str = Depends(get_user)):
    rank = get_user_rank(user_id)
    if not rank:
       return {"rank": None, "points" : 0 }
    
    return rank

@router.get("")
def leaderboard():
    return get_leaderboard()