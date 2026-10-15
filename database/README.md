# Database Layer

## Current Implementation

The Student Academic Management Platform currently stores
student records, courses, enrollments, and grades in memory
using Python data structures.

## Persistence Limitation

Data is not persisted to a database. Records are lost when
the application process restarts.

## Future Improvement

A persistent database, such as PostgreSQL, could be integrated
to store academic records between application restarts.
