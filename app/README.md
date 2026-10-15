# Student Academic Management API

## Overview

This Flask REST API manages student records, courses, semester enrollments,
grades, and GPA calculations.

## Base URL

When running locally:

http://127.0.0.1:5000

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check application health |
| GET | `/students` | List all students |
| POST | `/students` | Register a student |
| GET | `/courses` | List all courses |
| POST | `/courses` | Register a course |
| GET | `/enrollments` | List enrollments |
| POST | `/enrollments` | Enroll a student in a course |
| POST | `/grades` | Record a grade |
| GET | `/gpa/<student_id>` | Calculate a student's GPA |

## Business Rules

- A student must be registered before enrollment.
- A course must exist before a student can enroll.
- Duplicate student registrations are rejected.
- Duplicate enrollment in the same course and semester is rejected.
- A student cannot exceed 18 course credits in one semester.
- Grades must be between 0 and 10.
- GPA is calculated as a credit-weighted average of graded courses.

## Example Student Registration

Request:

```json
{
  "student_id": "S001",
  "name": "Rahul Sharma",
  "email": "rahul@example.com"
}
