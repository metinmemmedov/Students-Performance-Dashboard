from contextlib import closing

import pyodbc

import config


def create_connection():
    connection_string = (
        f"DRIVER={{{config.DRIVER_NAME}}};"
        f"SERVER={config.SERVER_NAME};"
        f"DATABASE={config.DATABASE_NAME};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string)

def rows_to_students(rows):
    return [{"name": row.Name, "score": row.Score} for row in rows]


def add_student(student_name, student_score):
    query = "INSERT INTO Students (Name, Score) VALUES (?, ?)"
    with closing(create_connection()) as connection:
        connection.execute(query, student_name, student_score)
        connection.commit()


def get_students():
    query = "SELECT Name, Score FROM Students ORDER BY Name"
    with closing(create_connection()) as connection:
        rows = connection.execute(query).fetchall()
    return rows_to_students(rows)


def get_student(student_name):
    query = "SELECT Name, Score FROM Students WHERE Name LIKE ?"
    with closing(create_connection()) as connection:
        rows = connection.execute(query, f"%{student_name}%").fetchall()
    return rows_to_students(rows)