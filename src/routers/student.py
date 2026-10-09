
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.core.database import get_db
from src.models.student import Student
from src.services.azure_blob import upload_file, delete_file, get_file_url, download_file_stream

router = APIRouter()


@router.post("/add-student")
async def add_student(
    name: str = Form(...),
    class_id: int = Form(...),
    photo: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    print("STEP 1: API received", flush=True)

    photo_id = None

    if photo:
        print("STEP 2: Starting Azure upload", flush=True)
        photo_id = await upload_file(photo)
        print("STEP 3: Azure upload completed", photo_id, flush=True)

    print("STEP 4: Starting database operation", flush=True)
    new_student = Student(
        name=name,
        class_id=class_id,
        photo_id=photo_id
    )

    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
    except Exception:
        db.rollback()
        raise

    print("STEP 5: Database operation completed", flush=True)

    return {
        "id": new_student.id,
        "name": new_student.name,
        "class_id": new_student.class_id,
        "photo_id": new_student.photo_id,
        "photo_url": f"/photo/{new_student.photo_id}" if new_student.photo_id else None
    }

@router.get("/students")
async def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "class_id": s.class_id,
            "photo_id": s.photo_id,
            "photo_url": f"/photo/{s.photo_id}" if s.photo_id else None
        }
        for s in students
    ]

@router.get("/students/{student_id}")
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "id": student.id,
        "name": student.name,
        "class_id": student.class_id,
        "photo_id": student.photo_id,
        "photo_url": f"/photo/{student.photo_id}" if student.photo_id else None
    }

@router.get("/photo/{photo_id}")
async def get_photo(photo_id: str):
    try:
        stream_generator = await download_file_stream(photo_id)
        return StreamingResponse(stream_generator, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Photo not found")