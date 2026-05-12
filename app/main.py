from fastapi import FastAPI

from app.api.routes.feedback import router as feedback_router

app = FastAPI(title="FastAPI Feedback System")
app.include_router(feedback_router)
