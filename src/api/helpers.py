from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY , ALGORITHM

def get_object_or_404(db, model, *criterion):
      obj = db.query(model).filter(*criterion).first()

      if obj is None:
            raise HTTPException(
                  status_code=404,
                  detail=f"{model.__name__} not found"
            )

      return obj


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