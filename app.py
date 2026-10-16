import pandas as pd
import streamlit as st

import database
import services

MIN_SCORE = 0
MAX_SCORE = 100
SHOW_STUDENTS_KEY = "show_students"


def show_add_student_form():
    st.subheader("Add Student")
    student_name = st.text_input("Student Name")
    student_score = st.number_input(
        "Score", min_value=MIN_SCORE, max_value=MAX_SCORE, step=1
    )

    if st.button("Add Student"):
        save_student(student_name, student_score)


def save_student(student_name, student_score):
    clean_name = student_name.strip()
    if not clean_name:
        st.error("Student name cannot be empty.")
        return

    database.add_student(clean_name, int(student_score))
    st.success(f"{clean_name} was added.")


def show_statistics(students):
    statistics = services.calculate_statistics(students)
    total_column, average_column, highest_column, lowest_column = st.columns(4)

    total_column.metric("Total Students", statistics["total_students"])
    average_column.metric("Average Score", statistics["average_score"])
    highest_column.metric("Highest Score", statistics["highest_score"])
    lowest_column.metric("Lowest Score", statistics["lowest_score"])


def show_student_list():
    st.subheader("Students")
    search_text = st.text_input("Search Student")

    matching_students = database.get_student(search_text.strip())
    students_with_grades = services.add_grades(matching_students)

    if not students_with_grades:
        st.info("No students found.")
        return

    table = pd.DataFrame(students_with_grades).rename(columns=str.capitalize)
    st.dataframe(table, hide_index=True)


def toggle_student_list():
    is_visible = st.session_state.get(SHOW_STUDENTS_KEY, False)
    st.session_state[SHOW_STUDENTS_KEY] = not is_visible


def show_student_list_section():
    is_visible = st.session_state.get(SHOW_STUDENTS_KEY, False)
    button_label = "Hide Students" if is_visible else "Show Students"
    st.button(button_label, on_click=toggle_student_list)

    if is_visible:
        show_student_list()


def main():
    st.title("Student Performance Dashboard")
    show_add_student_form()
    show_statistics(database.get_students())
    show_student_list_section()


main()