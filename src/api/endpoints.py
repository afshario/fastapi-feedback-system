from fastapi import (APIRouter, status, HTTPException, Depends)
from db import (Base, engine, get_db)
from models import (users, posts, tags, comments, votes)
from sqlalchemy.orm import Session
from .requestmodels import (RegisterRequest, LoginRequest, UpdateUser, PostCreate, PostUpdate, CommentCreate, VoteCreate)
from .responsemodels import (RegisterResponse, UserResponse, PostResponse)
from .helpers import (get_object_or_404, create_access_token)
from .dependencies import verify_jwt
from .caching import RedisCache

router = APIRouter()
Base.metadata.create_all(bind=engine)


# =======================================================
# AUTH ENDPOINTS
# =======================================================

@router.post("/auth/login",
    status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    
    user = get_object_or_404(db,users.Users, users.Users.email == request.email)

    access_token = create_access_token({
        "sub": user.id,
        "username" : user.username
        })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
      

@router.post("/auth/register",
    status_code=status.HTTP_201_CREATED,
    response_model= UserResponse
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
    if existing_username:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="username already exists"
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
      
    new_user = users.Users(
        username=request.username,
        email=request.email,
    )

    new_user.set_password(request.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =======================================================
# USERS ENDPOINTS
# =======================================================

@router.get("/users",
        response_model=list[UserResponse],
        status_code= status.HTTP_200_OK,
        dependencies=[Depends(verify_jwt)]
)
async def get_users(db: Session = Depends(get_db)):
    return db.query(users.Users).all()


@router.get("/users/{id}",
            response_model=UserResponse,
            status_code= status.HTTP_200_OK,
            dependencies=[Depends(verify_jwt)])
async def get_user(id: int,
                    db: Session = Depends(get_db),):
    
    user = get_object_or_404(db,users.Users, users.Users.id == id)

    return user



@router.put("/users/{id}",
            response_model=UserResponse,
            status_code= status.HTTP_200_OK,
            dependencies=[Depends(verify_jwt)])
async def update_user(id: int,
                    updated_user: UpdateUser,
                    db: Session = Depends(get_db),
                    ):
    
    user = get_object_or_404(db,users.Users, users.Users.id == id)
    
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
    for key,value in updated_user.model_dump():
        setattr(user,key,value)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/users/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(verify_jwt)])
async def delete_user(id: int,
                    db: Session = Depends(get_db)
                    ):
    user = get_object_or_404(db,users.Users,users.Users.id == id)
    db.delete(user)
    db.commit()


# =======================================================
# FEEDBACKS ENDPOINTS
# =======================================================

@router.get("/feedbacks",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(verify_jwt)],
            response_model= list[PostResponse])
async def get_feedbacks(db: Session = Depends(get_db)):
    return db.query(posts.Posts).all()
    

@router.get("/feedbacks/{id}",
            status_code= status.HTTP_200_OK,
            dependencies=[Depends(verify_jwt)],
            response_model= PostResponse)
async def get_feedback(id: int,
                       db: Session = Depends(get_db)):
    post = get_object_or_404(db,posts.Posts,posts.Posts.id == id)
    return post


@router.post("/feedbacks",
            status_code= status.HTTP_200_OK,
            response_model= list[PostResponse])
async def create_feedback(post_data: PostCreate,
                        db: Session = Depends(get_db),
                        req : dict = Depends(verify_jwt)):
    post = posts.Posts(
        author=req["username"],
        title=post_data.title,
        content=post_data.content
    )

    for tag_name in post_data.tags:
        tag = get_object_or_404(db,tags.Tag,tags.Tag.name == tag_name)
        post.tags.append(tag)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.put("/feedbacks/{id}",
            dependencies=[Depends(verify_jwt)],
            status_code=status.HTTP_200_OK,
            response_model= PostResponse)
async def update_feedback(id: int,
                          updated_post : PostUpdate,
                        db: Session = Depends(get_db)):
    
    post = get_object_or_404(db,posts.Posts,posts.Posts.id == id)
    update_data = updated_post.model_dump(exclude_unset=True)
    tag_names = update_data.pop("tags", None)

    for key, value in update_data.items():
        setattr(post, key, value)

    if tag_names is not None:
        post.tags.clear()
        for tag_name in tag_names:
            tag = get_object_or_404(db,tags.Tag,tags.Tag.name == tag_name)
            post.tags.append(tag)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.delete("/feedbacks/{id}",
               dependencies=[Depends(verify_jwt)],
                status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback(id: int,
                          db: Session = Depends(get_db)):
    post = get_object_or_404(db,posts.Posts,posts.Posts.id == id)
    db.delete(post)
    db.commit()


# =======================================================
# COMMENTS ENDPOINTS
# =======================================================

@router.get("/feedbacks/{id}/comments",
            dependencies=[Depends(verify_jwt)],
            status_code=status.HTTP_200_OK)
async def get_feedback_comments(id: int,
                                db: Session = Depends(get_db)):
    post = get_object_or_404(db,posts.Posts,posts.Posts.id == id)
    comment = db.query(comments.Comments).filter(comments.Comments.post == id).all()
    return comment


@router.post("/feedbacks/{id}/comments",
             status_code=status.HTTP_200_OK)
async def create_comment(id: int,
                        comment : CommentCreate,
                        db: Session = Depends(get_db),
                        req : dict = Depends(verify_jwt)):
    post = get_object_or_404(db,posts.Posts,posts.Posts.id == id)
    new_comment = comments.Comments(
        writer = req["username"],
        post = id,
        content = comment.content
    )
    db.add(new_comment)
    db.commit()

    return new_comment


@router.get("/comments/{id}",
            dependencies=[Depends(verify_jwt)],
            status_code=status.HTTP_200_OK)
async def get_comment(id: int,
                    db: Session = Depends(get_db)):
    comment = get_object_or_404(db,comments.Comments,comments.Comments.id == id)
    
    return comment


@router.delete("/comments/{id}",
               dependencies=[Depends(verify_jwt)],
               status_code= status.HTTP_204_NO_CONTENT)
async def delete_comment(id: int,
                        db: Session = Depends(get_db)):

    comment = get_object_or_404(db,comments.Comments,comments.Comments.id == id)
    
    db.delete(comment)
    db.commit()

# =======================================================
# VOTES ENDPOINTS
# =======================================================

@router.get("/feedbacks/{id}/votes",
            dependencies=[Depends(verify_jwt)],
            status_code=status.HTTP_200_OK)
async def get_feedback_votes(id: int,
                            db: Session = Depends(get_db)):

    return db.query(votes.Votes).filter(votes.Votes.post == id).all()


@router.post("/feedbacks/{id}/votes",
             status_code=status.HTTP_200_OK)
async def create_vote(id: int,
                    vote: VoteCreate,
                    db: Session = Depends(get_db),
                    req : dict = Depends(verify_jwt)):
    
    post = get_object_or_404(db,posts.Posts,posts.Posts.id == id)
    
    new_vote = votes.Votes(
        voter=req["sub"],
        post=id,
        type=vote.type
    )

    db.add(new_vote)

    if vote.type == "down":
        post.dvotec += 1
    else:
        post.uvotec += 1

    try:
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="You have already voted for this post"
        )

    return new_vote


@router.get("/votes/{id}",
            dependencies=[Depends(verify_jwt)],
            status_code=status.HTTP_200_OK)
async def get_vote(id: int,
                   db: Session = Depends(get_db)):
    vote = get_object_or_404(db,votes.Votes,votes.Votes.id == id)
    return vote


@router.delete("/votes/{id}",
            dependencies=[Depends(verify_jwt)],
            status_code=status.HTTP_204_NO_CONTENT)
async def delete_vote(id: int,
                      db: Session = Depends(get_db)):
    vote = get_object_or_404(db,votes.Votes,votes.Votes.id == id)
    post = db.query(posts.Posts).filter(posts.Posts.id == vote.post).first()
    if vote.type == "down":
        post.dvotec -= 1
    else:
        post.uvotec -= 1

    db.delete(vote)
    db.commit()



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