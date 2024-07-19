from fastapi import APIRouter, HTTPException, status
from datetime import timedelta

from src.user.domain.user_schema import Login, ResponseLogin
from src.user.infrastructure.user import authenticate_user, create_access_token

from src.shared.infrastructure.config import get_settings

SETTINGS = get_settings()

router = APIRouter()


@router.post("/login")
async def login(user: Login) -> ResponseLogin:
    try:
        user_dic = dict(user)
        val_user = await authenticate_user(user_dic["email"], user_dic["password"])
        if not val_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(
            data={"sub": val_user["username"], "scopes": val_user["scopes"]},
            expires_delta=access_token_expires,
        )
        return ResponseLogin(token=access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
