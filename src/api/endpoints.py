from fastapi import APIRouter, Depends, status
from db import *
from models.users import Users

router = APIRouter()
Base.metadata.create_all(bind=engine)


# =======================================================
# AUTH ENDPOINTS
# =======================================================

@router.post("/auth/login")
async def login():
    return {"message": "Login endpoint"}


@router.post("/auth/register")
async def register():
    return {"message": "Register endpoint"}


# =======================================================
# USERS ENDPOINTS
# =======================================================

@router.get("/users")
async def get_users():
    return {"message": "Get all users"}


@router.get("/users/{id}")
async def get_user(id: int):
    return {"message": f"Get user {id}"}


@router.put("/users/{id}")
async def update_user(id: int):
    return {"message": f"Update user {id}"}


@router.delete("/users/{id}")
async def delete_user(id: int):
    return {"message": f"Delete user {id}"}


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