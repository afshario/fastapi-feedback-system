from fastapi import APIRouter, Depends, status, HTTPException
from db import *
from models.users import Users
from sqlalchemy.orm import Session
from .requestmodels import *
from .responsemodels import *
import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from .dependencies import verify_jwt
from config import SECRET_KEY , ALGORITHM



router = APIRouter()
Base.metadata.create_all(bind=engine)


# =======================================================
# AUTH ENDPOINTS
# =======================================================

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({
        "exp": expire
    })
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

@router.post("/auth/login",
    status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(Users)
        .filter(Users.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
        )
      
    password_correct = bcrypt.checkpw(
        request.password.encode("utf-8"),
        user.password.encode("utf-8")
    )

    if not password_correct:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
        )
      
    access_token = create_access_token({
    "sub": str(user.id)
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
      


@router.post("/auth/register",
    status_code=status.HTTP_201_CREATED,
            )
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
    ):
    existing_username = (
        db.query(Users)
        .filter(Users.username == request.username)
        .first()
    )
    existing_email = (
        db.query(Users)
        .filter(Users.email == request.email)
        .first()
    )
    if existing_email :
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
        )
      
    if existing_username:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="username already exists"
        )
      
    hashed_password = bcrypt.hashpw(
        request.password.encode("utf-8"),
        bcrypt.gensalt()
        ).decode("utf-8")
      
    new_user = Users(
        username=request.username,
        email=request.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =======================================================
# USERS ENDPOINTS
# =======================================================

@router.get("/users",
        response_model=list[UserResponse],
        status_code= status.HTTP_200_OK
)
async def get_users(db: Session = Depends(get_db),
                    req : dict = Depends(verify_jwt)):
    return db.query(Users).all()


@router.get("/users/{id}",
            response_model=UserResponse,
            status_code= status.HTTP_200_OK)
async def get_user( id: int,
                    db: Session = Depends(get_db),
                    req : dict = Depends(verify_jwt)):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.put("/users/{id}",
            response_model=UserResponse,
            status_code= status.HTTP_200_OK)
async def update_user(id: int,
                    updated_user: UpdateUser,
                    db: Session = Depends(get_db),
                    req : dict = Depends(verify_jwt),
                    ):
    user = db.query(Users).filter(Users.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_username = (
        db.query(Users)
        .filter((Users.username == updated_user.username) & (Users.id != id))
        .first()
    )
    if existing_username:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="username already exists"
        )
    existing_email = (
        db.query(Users)
        .filter((Users.email == updated_user.email) &  (Users.id != id))
        .first()
    )
    if existing_email :
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
        )
    user.username = updated_user.username
    user.email = updated_user.email
    user.is_active = updated_user.is_active

    db.commit()
    db.refresh(user)

    return user


@router.delete("/users/{id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int,
                    db: Session = Depends(get_db),
                    req : dict = Depends(verify_jwt)):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user does'nt exist"
        )
    db.delete(user)
    db.commit()


# =======================================================
# FEEDBACKS ENDPOINTS
# =======================================================

@router.get("/feedbacks")
async def get_feedbacks():
    return {"message": "Get all feedbacks"}


@router.get("/feedbacks/{id}")
async def get_feedback(id: int):
    return {"message": f"Get feedback {id}"}


@router.post("/feedbacks")
async def create_feedback():
    return {"message": "Create feedback"}


@router.put("/feedbacks/{id}")
async def update_feedback(id: int):
    return {"message": f"Update feedback {id}"}


@router.delete("/feedbacks/{id}")
async def delete_feedback(id: int):
    return {"message": f"Delete feedback {id}"}


# =======================================================
# COMMENTS ENDPOINTS
# =======================================================

@router.get("/feedbacks/{id}/comments")
async def get_feedback_comments(id: int):
    return {"message": f"Get comments for feedback {id}"}


@router.post("/feedbacks/{id}/comments")
async def create_comment(id: int):
    return {"message": f"Add comment to feedback {id}"}


@router.get("/comments/{id}")
async def get_comment(id: int):
    return {"message": f"Get comment {id}"}


@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int):
    return {"message": f"Delete comment {comment_id}"}


# =======================================================
# RESPONSES ENDPOINTS
# =======================================================

@router.get("/feedbacks/{id}/response")
async def get_feedback_response(id: int):
    return {"message": f"Get admin response for feedback {id}"}


@router.get("/responses/{id}")
async def get_response(id: int):
    return {"message": f"Get response {id}"}


@router.delete("/responses/{response_id}")
async def delete_response(response_id: int):
    return {"message": f"Delete response {response_id}"}


# =======================================================
# VOTES ENDPOINTS
# =======================================================

@router.get("/feedbacks/{id}/votes")
async def get_feedback_votes(id: int):
    return {"message": f"Get votes for feedback {id}"}


@router.post("/feedbacks/{id}/votes")
async def create_vote(id: int):
    return {"message": f"Vote for feedback {id}"}


@router.get("/votes/{id}")
async def get_vote(id: int):
    return {"message": f"Get vote {id}"}


@router.delete("/votes/{vote_id}")
async def delete_vote(vote_id: int):
    return {"message": f"Delete vote {vote_id}"}