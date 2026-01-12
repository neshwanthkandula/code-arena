from fastapi import APIRouter,FastAPI,Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import sessionLocal
from app.models import User
from app.schema import SignupRequest,LoginRequest
from app.auth.password import hash_password
from app.auth.jwt import create_jwt
from app.auth.password import verify_password



router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally :
        db.close()

@router.post("/signup")
def signup(payload : SignupRequest, response : Response, db: Session = Depends(get_db)):
    print("signup called")
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status=400, detail="User already exsists")
    
    user = User(
        username = payload.username,
        email = payload.email,
        password_hash=hash_password(payload.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_jwt(user.id)
    response.set_cookie(
        key = "token",
        value = token,
        httponly = True,
        secure=False,         # REQUIRED for SameSite=None
        samesite="lax",     # REQUIRED for cross-site
        path="/"
    )

    return { "messages" : "Signup successful"}


@router.post("/login")
def login(payload : LoginRequest , response : Response , db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_jwt(user.id)
    response.set_cookie(
        key = "token",
        value = token,
        httponly=True,
        secure=False,         # REQUIRED for SameSite=None
        samesite="lax",     # REQUIRED for cross-site
        path="/"
    )

    return { "message" : "Login successful"}

