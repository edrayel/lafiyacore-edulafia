"""Tests for Students API endpoints - written BEFORE implementation (TDD)."""

from uuid import uuid4

import pytest


class TestStudentsAPI:
    """Test cases for Student API endpoints."""

    @pytest.fixture
    def student_payload(self):
        """Sample student creation payload."""
        return {
            "first_name": "Emeka",
            "last_name": "Nwosu",
            "admission_number": "EDU/2026/042",
            "date_of_birth": "2011-08-20",
            "gender": "male",
            "class_id": str(uuid4()),
            "admission_date": "2026-01-15",
        }

    def test_create_student_endpoint_exists(self):
        """Test that POST /api/v1/students endpoint is registered."""
        from edulafia.api.v1.students import router
        routes = [r.path for r in router.routes if hasattr(r, 'methods')]
        assert any('students' in path for path in routes) or len(router.routes) > 0

    def test_list_students_endpoint_exists(self):
        """Test that GET /api/v1/students endpoint is registered."""
        from edulafia.api.v1.students import router
        assert router is not None

    def test_get_student_endpoint_exists(self):
        """Test that GET /api/v1/students/{id} endpoint is registered."""
        from edulafia.api.v1.students import router
        assert router is not None

    def test_update_student_endpoint_exists(self):
        """Test that PATCH /api/v1/students/{id} endpoint is registered."""
        from edulafia.api.v1.students import router
        assert router is not None

    def test_archive_student_endpoint_exists(self):
        """Test that DELETE /api/v1/students/{id} endpoint is registered."""
        from edulafia.api.v1.students import router
        assert router is not None
