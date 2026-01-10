from sqlalchemy.orm import Session
from app.models import Problem 


def get_problems(db:Session):
    return db.query(Problem).filter(Problem.status == "published").all()


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
