from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
from pathlib import Path 
import json 
from fastapi.middleware.cors import CORSMiddleware
from app.database import sessionLocal 
from app import crud,schema
from fastapi.responses import JSONResponse
from app.services.judge_runner import judge_problem
from app.models import Submission
from app.auth.middleware import get_user
from app.auth.routes.auth import router as auth_router 
from app.contest.routes import router as contest_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(contest_router)

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


PROBLEMS_PATH = Path(".\problems")
if not PROBLEMS_PATH.exists():
   print("Warning: Problems path does not exist.")
else:
    print("valid path")

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally :
        db.close()


@app.post("/admin/sync")
def sync_problems(db: Session = Depends(get_db)):

    if not PROBLEMS_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Problems directory not found: {PROBLEMS_PATH}"
        )
    
    for folder in PROBLEMS_PATH.iterdir():
        if not folder.is_dir():
            continue

        meta_path = folder / "metadata.json"
        print("Reading metadata from:", meta_path)
        if not meta_path.exists():
            continue

        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        print(meta)
        crud.upsert_problem(db, {
            "slug": meta["slug"],
            "title": meta["title"],
            "status": "normal"
        })

    return {"message": "sync completed"}



@app.get("/problems", response_model=list[schema.ProblemOut])
def list_problems(db: Session = Depends(get_db)):
    return crud.get_problems(db)

@app.get("/problem/{slug}")
def get_problem(slug : str, db : Session = Depends(get_db)):
    problem = crud.get_problems_by_slug(db, slug)
    
    if not problem:
        raise HTTPException(status_code=404, detail="problem not found")
    
    md_path = PROBLEMS_PATH/slug/"problem.md"
    if not md_path.exists():
        raise HTTPException(status_code=500, detail="problem statement not found")
    
    data =  {
        "slug" : problem.slug,
        "title": problem.title,
        "statement": md_path.read_text()
    }
    return JSONResponse(
      content = data,
      media_type="application/json"
    )


@app.post("/submit")
async def submit(payload : schema.SubmitRequest, user_id = Depends(get_user), db: Session = Depends(get_db)):
    print(user_id)
    
    try:
        result = await judge_problem(
            payload.problem_slug,
            payload.source_code,
            payload.language_id
        )

        submission = Submission(
            user_id=user_id,  # temporary
            problem_slug=payload.problem_slug,
            source_code=payload.source_code,
            language_id=payload.language_id,
            verdict=result["verdict"]
        )

        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        return result
    except Exception as e : 
        raise HTTPException(status_code=400, detail=str(e))



