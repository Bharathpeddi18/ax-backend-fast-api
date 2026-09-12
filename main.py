from psycopg import connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_database_connection


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SubmissionRequest(BaseModel):
    name: str
    number: str


@app.get("/")
def root():
    return {
        "message": "FastAPI backend is running successfully"
    }


@app.get("/submissions")
def get_all_submissions():
    connection = get_database_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, number
            FROM form_submissions
            ORDER BY id DESC;
            """
        )

        rows = cursor.fetchall()

        submissions = [
            {
                "id": row[0],
                "name": row[1],
                "number": row[2],
            }
            for row in rows
        ]

        return {
            "status": 200,
            "submissions": submissions,
        }

    finally:
        cursor.close()
        connection.close()

@app.get("/submissions-delete/{id}")
def delete_all_submissions(id: int):
    connection = get_database_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM form_submissions
            WHERE id = %s;
            """,
            (id,)
        )

        connection.commit()

        return {
            "status": 200,
            'message': 'Submission deleted successfully',
        }

    finally:
        cursor.close()
        connection.close()

@app.post("/submit")
def submit_form(data: SubmissionRequest):
    connection = get_database_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO form_submissions (name, number)
            VALUES (%s, %s)
            RETURNING id;
            """,
            (data.name, data.number),
        )

        submission_id = cursor.fetchone()[0]

        connection.commit()

        return {
            "message": "Student created successfully",
            "submission": {
                "id": submission_id,
                "name": data.name,
                "number": data.number,
            },
        }

    finally:
        cursor.close()
        connection.close()