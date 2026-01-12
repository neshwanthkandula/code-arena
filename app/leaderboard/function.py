from app.leaderboard.redis_client import redis_client
from sqlalchemy.orm import Session
from app.models import Leaderboard

LEADERBOARD_KEY = "leaderboard"

def add_points(user_id : int, points : int):
    redis_client.zincrby(LEADERBOARD_KEY, points, user_id)


def get_leaderboard():
    raw = redis_client.zrevrange(
        LEADERBOARD_KEY,
        0,
        -1,
        withscores=True
    )

    leaderboard = []
    rank = 1
    for user_id, score in raw:
        leaderboard.append({
            "rank": rank,
            "user_id": int(user_id),
            "points": int(score)
        })
        rank += 1

    return leaderboard


def get_user_rank(user_id : int):
    rank = redis_client.zrevrank(LEADERBOARD_KEY, user_id)
    score = redis_client.zscore(LEADERBOARD_KEY, user_id)

    if rank is None :
        return None 
    

    return {
        "rank" : rank+1,
        "points" : int(score)
    }


def reset_leaderboard():
    redis_client.delete(LEADERBOARD_KEY)

def persist_leaderboard(contest_id : str, db: Session):
    raw = redis_client.zrevrange(
        LEADERBOARD_KEY,
        0,
        -1,
        withscores=True
    )

    rank = 1
    for user_id,score in raw:
        row = Leaderboard(
            contest_id = contest_id,
            user_id=int(user_id),
            total_points=int(score),
            rank=rank
        )

        db.add(row)
        rank+=1

    db.commit()


    