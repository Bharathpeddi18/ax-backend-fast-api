from pwdlib import PasswordHash
from sqlalchemy import select

from src.core.database import SessionLocal
from src.models.userss import User
from src.models.groupss import Group


password_hash = PasswordHash.recommended()


def seed_user():
    db = SessionLocal()

    try:
        existing_user = db.scalar(
            select(User).where(
                User.email == "owner@astrax.com"
            )
        )

        if existing_user is None:
            user = User(
                name="Astrax Owner",
                email="owner@astrax.com",
                password_hash=password_hash.hash("ChangeMe123!"),
                group_code="owner",
            )

            db.add(user)
            db.commit()

            print("Owner user created successfully!")

        else:
            print("Owner user already exists.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_user()