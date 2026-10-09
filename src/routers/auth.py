import os
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.core.database import get_db
from src.core.security import create_access_token, verify_password
from src.core.dependencies import get_current_user, require_roles
from src.models.users import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production"

class LoginRequest(BaseModel):
    email: str
    password: str

# region api-login
@router.post('/login')
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    email = data.email.strip().lower()

    user = db.query(User).filter(func.lower(User.email) == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    access_token = create_access_token(user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="none" if IS_PRODUCTION else "lax",
        max_age=30 * 60,
        path="/",
    )

    return {
        "message": "Login was succesfull",
        "user": {
            "id": user.id,
            "email": user.email,
            "group_code": user.group_code,
        },
    }

# region api-logout
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="none" if IS_PRODUCTION else "lax",
    )
    return {"message": "Logout successful"}

# region api-me
@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "group_code": current_user.group_code,
        }
    }

@router.get("/test-owner")
def test_owner(
    current_user: User = Depends(require_roles("owner")),
):
    return {
        "message": "owner access granted",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "group_code": current_user.group_code,
        },
    }