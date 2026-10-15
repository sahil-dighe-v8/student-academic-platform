from flask import Flask, jsonify, request

app = Flask(__name__)

students = {}
courses = {}
enrollments = []

MAX_SEMESTER_CREDITS = 18


@app.route("/")
def home():
    return jsonify({
        "message": "Student Academic Management Platform",
        "status": "running"
    })


@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(list(students.values()))


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}

    student_id = data.get("student_id")
    name = data.get("name")
    email = data.get("email")

    if not all(isinstance(v, str) and v.strip()
               for v in (student_id, name, email)):
        return jsonify({
            "error": "student_id, name, and email are required"
        }), 400

    student_id = student_id.strip()

    if student_id in students:
        return jsonify({"error": "Student already exists"}), 409

    student = {
        "student_id": student_id,
        "name": name.strip(),
        "email": email.strip()
    }

    students[student_id] = student
    return jsonify(student), 201


@app.route("/courses", methods=["GET"])
def get_courses():
    return jsonify(list(courses.values()))


@app.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json(silent=True) or {}

    course_id = data.get("course_id")
    name = data.get("name")
    credits = data.get("credits")

    if not isinstance(course_id, str) or not course_id.strip():
        return jsonify({"error": "course_id is required"}), 400

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "name is required"}), 400

    if isinstance(credits, bool):
        return jsonify({"error": "credits must be an integer"}), 400

    try:
        numeric_credits = int(credits)
        if str(credits).strip() != str(numeric_credits):
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "credits must be an integer"}), 400

    if not 1 <= numeric_credits <= 6:
        return jsonify({
            "error": "credits must be between 1 and 6"
        }), 400

    course_id = course_id.strip()

    if course_id in courses:
        return jsonify({"error": "Course already exists"}), 409

    course = {
        "course_id": course_id,
        "name": name.strip(),
        "credits": numeric_credits
    }

    courses[course_id] = course
    return jsonify(course), 201


@app.route("/enrollments", methods=["POST"])
def enroll_student():
    data = request.get_json(silent=True) or {}

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    semester = data.get("semester")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (student_id, course_id, semester)
    ):
        return jsonify({
            "error": "student_id, course_id, and semester are required"
        }), 400

    student_id = student_id.strip()
    course_id = course_id.strip()
    semester = semester.strip()

    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404

    if course_id not in courses:
        return jsonify({"error": "Course not found"}), 404

    duplicate = any(
        enrollment["student_id"] == student_id
        and enrollment["course_id"] == course_id
        and enrollment["semester"] == semester
        for enrollment in enrollments
    )

    if duplicate:
        return jsonify({
            "error": "Student is already enrolled in this course for this semester"
        }), 409

    current_credits = sum(
        courses[enrollment["course_id"]]["credits"]
        for enrollment in enrollments
        if enrollment["student_id"] == student_id
        and enrollment["semester"] == semester
    )

    requested_credits = courses[course_id]["credits"]

    if current_credits + requested_credits > MAX_SEMESTER_CREDITS:
        return jsonify({
            "error": "Enrollment exceeds the 18-credit semester limit",
            "current_credits": current_credits,
            "requested_credits": requested_credits,
            "maximum_credits": MAX_SEMESTER_CREDITS
        }), 400

    enrollment = {
        "student_id": student_id,
        "course_id": course_id,
        "semester": semester,
        "grade": None
    }

    enrollments.append(enrollment)
    return jsonify(enrollment), 201


@app.route("/enrollments", methods=["GET"])
def get_enrollments():
    return jsonify(enrollments)


@app.route("/grades", methods=["POST"])
def record_grade():
    data = request.get_json(silent=True) or {}

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    semester = data.get("semester")
    grade = data.get("grade")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (student_id, course_id, semester)
    ):
        return jsonify({
            "error": "student_id, course_id, and semester are required"
        }), 400

    if isinstance(grade, bool) or not isinstance(grade, (int, float)):
        return jsonify({"error": "grade must be a number from 0 to 10"}), 400

    if not 0 <= grade <= 10:
        return jsonify({"error": "grade must be between 0 and 10"}), 400

    for enrollment in enrollments:
        if (
            enrollment["student_id"] == student_id.strip()
            and enrollment["course_id"] == course_id.strip()
            and enrollment["semester"] == semester.strip()
        ):
            enrollment["grade"] = float(grade)
            return jsonify(enrollment), 200

    return jsonify({"error": "Matching enrollment not found"}), 404


@app.route("/gpa/<student_id>", methods=["GET"])
def calculate_gpa(student_id):
    semester = request.args.get("semester")

    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404

    graded_enrollments = [
        enrollment
        for enrollment in enrollments
        if enrollment["student_id"] == student_id
        and enrollment["grade"] is not None
        and (semester is None or enrollment["semester"] == semester)
    ]

    total_credits = sum(
        courses[enrollment["course_id"]]["credits"]
        for enrollment in graded_enrollments
    )

    if total_credits == 0:
        return jsonify({
            "student_id": student_id,
            "semester": semester,
            "gpa": None,
            "message": "No graded courses available"
        }), 200

    weighted_points = sum(
        enrollment["grade"]
        * courses[enrollment["course_id"]]["credits"]
        for enrollment in graded_enrollments
    )

    gpa = weighted_points / total_credits

    return jsonify({
        "student_id": student_id,
        "semester": semester,
        "total_credits": total_credits,
        "gpa": round(gpa, 2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
