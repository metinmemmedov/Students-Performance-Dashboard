GRADE_THRESHOLDS = (
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
)
FAILING_GRADE = "F"
AVERAGE_DECIMAL_PLACES = 1


def calculate_grade(student_score):
    for minimum_score, grade in GRADE_THRESHOLDS:
        if student_score >= minimum_score:
            return grade
    return FAILING_GRADE


def add_grades(students):
    return [
        {**student, "grade": calculate_grade(student["score"])}
        for student in students
    ]


def calculate_statistics(students):
    if not students:
        return {
            "total_students": 0,
            "average_score": 0,
            "highest_score": 0,
            "lowest_score": 0,
        }

    scores = [student["score"] for student in students]
    return {
        "total_students": len(scores),
        "average_score": round(sum(scores) / len(scores), AVERAGE_DECIMAL_PLACES),
        "highest_score": max(scores),
        "lowest_score": min(scores),
    }