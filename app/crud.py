from sqlalchemy.orm import Session
from app.models import Problem 
from app.models import Contest

def get_problems(db:Session):
    return db.query(Problem).filter(Problem.status == "normal").all()


def get_problems_by_slug(db : Session , slug: str):
    return db.query(Problem).filter(Problem.slug == slug).first()


def upsert_problem(db: Session, data: dict):
    slug = data["slug"]
    problem = db.query(Problem).filter(Problem.slug == slug).first()

    if problem:
        for key, value in data.items():
            if key != "slug":
                setattr(problem, key, value)
    else:
        problem = Problem(**data)
        db.add(problem)

    db.commit()
    db.refresh(problem)
    return problem

def upsert_contest(db: Session, data: dict):
    contest_id = data["contest_id"]
    contest = db.query(Contest).filter(Contest.contest_id == contest_id).first()

    if contest:
        for key, value in data.items():
            if key != "contest_id":
                setattr(contest, key, value)
    else:
        contest = Contest(**data)
        db.add(contest)

    db.commit()
    db.refresh(contest)
    return contest
