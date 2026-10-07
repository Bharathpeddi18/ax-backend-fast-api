from sqlalchemy import select

from src.core.database import SessionLocal
from src.models.groupss import Group


def seed_groups():
    db = SessionLocal()

    try:
        existing_group = db.scalar(
            select(Group).where(
                Group.group_code == "owner"
            )
        )

        if existing_group is None:
            owner_group = Group(
                group_code="owner",
                group_name="Owner",
                group_description="Full system access",
            )

            db.add(owner_group)
            db.commit()

            print("OWNER group created successfully!")

        else:
            print("OWNER group already exists.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_groups()