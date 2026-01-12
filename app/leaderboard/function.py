from app.leaderboard.redis_client import redis_client
from sqlalchemy.orm import Session
from app.models import Leaderboard,Contest

LEADERBOARD_KEY = "leaderboard"

def add_points(user_id : int, points : int):
    redis_client.zincrby(LEADERBOARD_KEY, points, user_id)


def ensure_contest_exists(contest_id: str, db: Session):
    contest = db.query(Contest).filter(Contest.contest_id == contest_id).first()
    if not contest:
        raise ValueError("Invalid contest_id")

def get_leaderboard_from_redis():
     
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


def get_user_rank_from_redis(user_id : int):
    rank = redis_client.zrevrank(LEADERBOARD_KEY, user_id)
    score = redis_client.zscore(LEADERBOARD_KEY, user_id)

    if rank is None :
        return None 
    

    return {
        "rank" : rank+1,
        "points" : int(score)
    }

def get_leaderboard_from_db(contest_id: str, db: Session):
    rows = (
        db.query(Leaderboard)
        .filter(Leaderboard.contest_id == contest_id)
        .order_by(Leaderboard.rank.asc())
        .all()
    )

    return [
        {
            "rank": row.rank,
            "user_id": row.user_id,
            "points": row.total_points
        }
        for row in rows
    ]


def get_user_rank_from_db(contest_id: str, user_id: int, db: Session):
    row = (
        db.query(Leaderboard)
        .filter(
            Leaderboard.contest_id == contest_id,
            Leaderboard.user_id == user_id
        )
        .first()
    )

    if not row:
        return None

    return {
        "rank": row.rank,
        "points": row.total_points
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


def get_leaderboard(contest_id: str, db: Session):
    ensure_contest_exists(contest_id, db)

    rows = db.query(Leaderboard).filter(Leaderboard.contest_id == contest_id).first()

    if rows:
        return get_leaderboard_from_db(contest_id, db)

    return get_leaderboard_from_redis()


def get_user_rank(contest_id: str, user_id: int, db: Session):
    ensure_contest_exists(contest_id, db)

    row = (
        db.query(Leaderboard)
        .filter(
            Leaderboard.contest_id == contest_id,
            Leaderboard.user_id == user_id
        )
        .first()
    )

    if row:
        return get_user_rank_from_db(contest_id, user_id, db)

    return get_user_rank_from_redis(user_id)