import pytest

from app.app import (
    app,
    students,
    courses,
    enrollments,
)


@pytest.fixture
def client():
    students.clear()
    courses.clear()
    enrollments.clear()

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    students.clear()
    courses.clear()
    enrollments.clear()


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_student_registration(client):
    response = client.post(
        "/students",
        json={
            "student_id": "S001",
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["student_id"] == "S001"


def test_duplicate_student_rejected(client):
    student = {
        "student_id": "S001",
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
    }

    client.post("/students", json=student)
    response = client.post("/students", json=student)

    assert response.status_code == 409


def test_course_registration(client):
    response = client.post(
        "/courses",
        json={
            "course_id": "CS101",
            "name": "Data Structures",
            "credits": 6,
        },
    )

    assert response.status_code == 201
    assert response.get_json()["credits"] == 6


def test_enrollment_credit_limit(client):
    client.post(
        "/students",
        json={
            "student_id": "S001",
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
        },
    )

    for course_id in ["CS101", "CS102", "CS103"]:
        client.post(
            "/courses",
            json={
                "course_id": course_id,
                "name": course_id,
                "credits": 6,
            },
        )

        response = client.post(
            "/enrollments",
            json={
                "student_id": "S001",
                "course_id": course_id,
                "semester": "2026-Fall",
            },
        )

        assert response.status_code == 201

    client.post(
        "/courses",
        json={
            "course_id": "CS104",
            "name": "Software Engineering",
            "credits": 3,
        },
    )

    response = client.post(
        "/enrollments",
        json={
            "student_id": "S001",
            "course_id": "CS104",
            "semester": "2026-Fall",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["maximum_credits"] == 18


def test_duplicate_enrollment_rejected(client):
    client.post(
        "/students",
        json={
            "student_id": "S001",
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
        },
    )

    client.post(
        "/courses",
        json={
            "course_id": "CS101",
            "name": "Data Structures",
            "credits": 6,
        },
    )

    enrollment = {
        "student_id": "S001",
        "course_id": "CS101",
        "semester": "2026-Fall",
    }

    first_response = client.post("/enrollments", json=enrollment)
    second_response = client.post("/enrollments", json=enrollment)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_gpa_calculation(client):
    client.post(
        "/students",
        json={
            "student_id": "S001",
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
        },
    )

    for course_id, grade in [
        ("CS101", 8.5),
        ("CS102", 9.0),
        ("CS103", 7.5),
    ]:
        client.post(
            "/courses",
            json={
                "course_id": course_id,
                "name": course_id,
                "credits": 6,
            },
        )

        client.post(
            "/enrollments",
            json={
                "student_id": "S001",
                "course_id": course_id,
                "semester": "2026-Fall",
            },
        )

        grade_response = client.post(
            "/grades",
            json={
                "student_id": "S001",
                "course_id": course_id,
                "semester": "2026-Fall",
                "grade": grade,
            },
        )

        assert grade_response.status_code == 200

    response = client.get("/gpa/S001?semester=2026-Fall")

    assert response.status_code == 200
    assert response.get_json()["gpa"] == 8.33
    assert response.get_json()["total_credits"] == 18
