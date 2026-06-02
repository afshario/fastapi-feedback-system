from fastapi import APIRouter, Depends, status, HTTPException
from db import *
from models import users , posts, tags, comments
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
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
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
        db.query(users.Users)
        .filter(users.Users.email == request.email)
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
    "sub": str(user.id),
    "username" : user.username
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
        db.query(users.Users)
        .filter(users.Users.username == request.username)
        .first()
    )
    existing_email = (
        db.query(users.Users)
        .filter(users.Users.email == request.email)
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
      
    new_user = users.Users(
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
    return db.query(users.Users).all()


@router.get("/users/{id}",
            response_model=UserResponse,
            status_code= status.HTTP_200_OK)
async def get_user( id: int,
                    db: Session = Depends(get_db),
                    req : dict = Depends(verify_jwt)):
    user = db.query(users.Users).filter(users.Users.id == id).first()
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
    user = db.query(users.Users).filter(users.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_username = (
        db.query(users.Users)
        .filter((users.Users.username == updated_user.username) & (users.Users.id != id))
        .first()
    )
    if existing_username:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="username already exists"
        )
    existing_email = (
        db.query(users.Users)
        .filter((users.Users.email == updated_user.email) &  (users.Users.id != id))
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
    user = db.query(users.Users).filter(users.Users.id == id).first()
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
async def get_feedbacks(db: Session = Depends(get_db),
                        req : dict = Depends(verify_jwt)):
    return db.query(posts.Posts).all()
    

@router.get("/feedbacks/{id}")
async def get_feedback(id: int,
                       db: Session = Depends(get_db),
                        req : dict = Depends(verify_jwt)):
    post = db.query(posts.Posts).filter(posts.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post.tags


@router.post("/feedbacks")
async def create_feedback(post_data: PostCreate,
                        db: Session = Depends(get_db),
                        req : dict = Depends(verify_jwt)):
    post = posts.Posts(
        author=req["username"],
        title=post_data.title,
        content=post_data.content
    )

    for tag_name in post_data.tags:
        tag = db.query(tags.Tag).filter(tags.Tag.name == tag_name).first()
        if not tag:
            continue
        post.tags.append(tag)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.put("/feedbacks/{id}")
async def update_feedback(id: int,
                          updated_post : PostUpdate,
                        db: Session = Depends(get_db),
                        req : dict = Depends(verify_jwt)):
    
    post = db.query(posts.Posts).filter(posts.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = updated_post.model_dump(exclude_unset=True)
    tag_names = update_data.pop("tags", None)

    for key, value in update_data.items():
        setattr(post, key, value)

    if tag_names is not None:
    
        post.tags.clear()

        for tag_name in tag_names:
            tag = db.query(tags.Tag)\
                .filter(tags.Tag.name == tag_name)\
                .first()
            if tag:
                post.tags.append(tag)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.delete("/feedbacks/{id}")
async def delete_feedback(id: int,
                          db: Session = Depends(get_db),
                          req : dict = Depends(verify_jwt)):
    post = db.query(posts.Posts).filter(posts.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()


# =======================================================
# COMMENTS ENDPOINTS
# =======================================================

@router.get("/feedbacks/{id}/comments")
async def get_feedback_comments(id: int,
                                db: Session = Depends(get_db),
                                req : dict = Depends(verify_jwt)):
    post = db.query(posts.Posts).filter(posts.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = db.query(comments.Comments).filter(comments.Comments.post == id).all()
    return comment


@router.post("/feedbacks/{id}/comments")
async def create_comment(id: int,
                        comment : CommentCreate,
                        db: Session = Depends(get_db),
                        req : dict = Depends(verify_jwt)):
    post = db.query(posts.Posts).filter(posts.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = comments.Comments(
        writer = req["username"],
        post = id,
        content = comment.content
    )
    db.add(new_comment)
    db.commit()

    return new_comment


@router.get("/comments/{id}")
async def get_comment(id: int,
                    db: Session = Depends(get_db),
                    req : dict = Depends(verify_jwt)):
    comment = db.query(comments.Comments).filter(comments.Comments.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    
    return comment


@router.delete("/comments/{id}",
               status_code= status.HTTP_204_NO_CONTENT)
async def delete_comment(id: int,
                        db: Session = Depends(get_db),
                        req : dict = Depends(verify_jwt)):

    comment = db.query(comments.Comments).filter(comments.Comments.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    
    db.delete(comment)
    db.commit()

    return {}

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