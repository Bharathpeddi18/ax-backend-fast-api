import os
from src.roles.dependencies import require_roles
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Request, Response, status, Depends

from src.database.database import get_connection
from src.user.security import create_access_token, verify_password
from src.roles.dependencies import get_current_user
from global_config import groups

router = APIRouter(prefix="/auth", tags=["Authentication"])

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development",
)

IS_PRODUCTION = ENVIRONMENT == "production"

class LoginRequest(BaseModel):
    email: str
    password: str

# region api-login
@router.post('/login')
def login(
    data: LoginRequest,
    response: Response,
):

    email = data.email.strip().lower()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    id,
                    email,
                    group_code,
                    is_active,
                    password_hash
                FROM users
                WHERE LOWER(email) = %s
                """,
                (email,),
            )

            user = cursor.fetchone()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    access_token = create_access_token(user["id"])

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
            "id": user["id"],
            "email": user["email"],
            "group_code": user["group_code"],
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
def me(current_user = Depends(get_current_user)):
    return {
        "user": {
            "id": current_user["id"],
            "email": current_user["email"],
            "group_code": current_user["group_code"],
        }
    }

@router.get("/test-owner")
def test_owner(
    current_user=Depends(
        require_roles("owner")
    ),
):
    return {
        "message": "onwer access granted",
        "user": current_user,
    }