from fastapi import FastAPI,APIRouter, HTTPException, Request, Response , Depends
from sqlalchemy.orm import Session
from app.database import sessionLocal
from app.models import Problem
from app.schema import CreateContestRequest,ContestSubmitRequest
from pathlib import Path
import json 
from app import crud
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from app.auth.middleware import get_user
from app.contest.function import get_contest_state,get_problem_points
from app.models import Contest,Submission
from app.services.judge_runner import judge_problem

router = APIRouter(prefix="/contest", tags=["contest"])
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally :
        db.close()



CONTESTS_PATH = Path(".\contests")
@router.post("/create")
def create_contest(db: Session = Depends(get_db)):
    print("create_contest called")
    for contest in CONTESTS_PATH.iterdir():
        for folder in contest.iterdir():
            if not folder.is_dir():
                continue

            meta_path = folder / "metadata.json"
            print("Reading metadata from:", meta_path)
            if not meta_path.exists():
                continue

            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            print(meta)

            # --- Contest ---
            start_time = meta.get("startTime")
            if not start_time:
                start_time = datetime.utcnow().isoformat()

            crud.upsert_contest(db, {
                "contest_id": meta["contest_id"],
                "start_Time": start_time,
                "Duration": str(meta["duration"])
            })

            # --- Problem ---
            crud.upsert_problem(db, {
                "slug": meta["slug"],
                "title": meta["title"],
                "status": "contest",
                "contest_id" : meta["contest_id"]
            })

    return {"message": "sync completed"}


@router.get("/")
def list_contests(db: Session = Depends(get_db)):
    contests = db.query(Problem.contest_id).filter(Problem.status == "contest").distinct().all()
    contests = [row[0] for row in contests]
    return contests

@router.get("/{contest_id}/problems")
def get_contest_problems(contest_id: str, db: Session = Depends(get_db)):
    problems = (
        db.query(Problem)
        .filter(
            Problem.contest_id == contest_id,
            Problem.status == "contest"
        )
        .all()
    )

    if not problems:
        raise HTTPException(status_code=404, detail="Contest not found")

    return [
        {
            "slug": p.slug,
            "title": p.title
        }
        for p in problems
    ]

# slug = contest_id + A | B | c | D"
#slug should be unique
@router.get("/problem/{slug}")
def get_problem(slug: str, db: Session = Depends(get_db)):
    problem = crud.get_problems_by_slug(db, slug)

    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")

    md_path = (
        CONTESTS_PATH
        / str(problem.contest_id)
        / problem.slug
        / "problem.md"
    )

    if not md_path.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Problem statement missing: {md_path}"
        )

    data = {
        "slug": problem.slug,
        "title": problem.title,
        "statement": md_path.read_text(encoding="utf-8"),
    }

    return JSONResponse(content=data)


@router.post("/submit")
async def submit_code(payload : ContestSubmitRequest, user_id:int = Depends(get_user), db: Session = Depends(get_db)):
    problem = db.query(Problem).filter_by(slug=payload.problem_slug).first()

    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Contest check
    if problem.status != "contest":
        raise HTTPException(status_code=400, detail="Not a contest problem")

    contest_id = problem.contest_id

    contest = db.query(Contest).filter(contest_id == contest_id).first()
    # TODO: contest time check (later)
    # assume running for now
    # contest_state = get_contest_state(contest.start_Time , contest.Duration)
    # if(contest_state == "upcoming" or contest_state == "finished") :
    #    raise HTTPException(status_code=404, detail="constest is not running")

    # write a judge_contest_problem same but tsst case filepath changes
    # Run judge
    # result = await judge_problem(
    #     payload.problem_slug,
    #     payload.source_code,
    #     payload.language_id
    # )

    # verdict = result["verdict"]
    verdict = "Accepted"
    points = 0

    if verdict == "Accepted":
        # compute problem index inside contest
        problems = (
            db.query(Problem)
            .filter(Problem.contest_id == contest_id)
            .order_by(Problem.id)
            .all()
        )
        index = problems.index(problem) + 1
        points = index * 50

    submission = Submission(
        user_id=user_id,
        contest_id=contest_id,
        verdict=verdict,
        points=points,
        source_code=payload.source_code,
        language_id=payload.language_id,
        problem_slug = payload.problem_slug
    )

    db.add(submission)
    db.commit()

    return {
        "verdict": verdict,
        "points": points
    }
