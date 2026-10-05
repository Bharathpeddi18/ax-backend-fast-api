from fastapi import Cookie, Depends, HTTPException, status

from database import get_connection
from security import decode_access_token


def get_current_user(
    access_token: str | None = Cookie(default=None),
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = decode_access_token(access_token)

        user_id = int(payload["sub"])

    except (
        ValueError,
        KeyError,
        TypeError,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    email,
                    role,
                    is_active
                FROM users
                WHERE id = %s
                LIMIT 1
                """,
                (user_id,),
            )

            user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    return user

def require_roles(*allowed_roles: str):

    def role_checker(
        current_user=Depends(get_current_user),
    ):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return role_checker