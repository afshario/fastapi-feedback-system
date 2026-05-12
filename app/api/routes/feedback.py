from fastapi import APIRouter

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
