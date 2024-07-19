from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Union, Annotated
from fastapi import Depends, HTTPException, Security, status
from pydantic import ValidationError

from src.shared.infrastructure.db.crud import get_item
from src.shared.infrastructure.config import get_settings
from src.user.domain.user_schema import User

SETTINGS = get_settings()

# function to encrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# utility to check if a received password matches the stored hash.
async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create a utility function to encrypt a password coming from the user.
async def get_password_hash(password):
    return pwd_context.hash(password)


# Search user in database
async def get_user(email: str):
    filter = {"email": email}
    projection = {}
    # Find in database
    find_user = await get_item("users", filter, projection)
    if find_user:
        return find_user
    return None


# Search user in database
async def get_username(email: str):
    filter = {"email": email}
    projection = {"username": 1, "email": 1, "active": 1}
    # Find in database
    find_user = await get_item("users", filter, projection)
    if find_user:
        return find_user
    return None


async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False
    valid_password = await verify_password(password, user["password"])
    if not valid_password:
        return False
    return user


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.SECRET_KEY, algorithm=SETTINGS.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    """
    Security Scopes:
    The parameter security_scopes will be of type SecurityScopes.
    It will have a property scopes with a list containing all the scopes required
    by itself and all the dependencies that use this as a sub-dependency.
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        # Decode token
        payload = jwt.decode(
            token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
    except (JWTError, ValidationError):
        raise credentials_exception
    # Verify that the user exists
    user = await get_user(email)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user)],
):
    if current_user["active"] is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
