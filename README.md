# Student Academic Management Platform

## Overview

The Student Academic Management Platform is a Flask-based REST API
for managing students, courses, enrollments, grades, and GPA calculations.

## Features

- Register and list students.
- Register and list courses.
- Enroll students in courses.
- Reject duplicate students and enrollments.
- Enforce a maximum of 18 credits per semester.
- Record grades for enrolled students.
- Calculate credit-weighted GPA.
- Run automated tests using pytest.

## Technology Stack

- Python
- Flask
- pytest
- Git and GitHub
- Docker
- Kubernetes with Minikube
- Jenkins CI/CD

## Run Locally

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
