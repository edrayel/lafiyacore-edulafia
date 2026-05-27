from datetime import date, timedelta
from uuid import uuid4

import pytest

pytestmark = pytest.mark.skip(reason="Needs proper DB setup")

from edulafia.core.security import hash_password
from edulafia.modules.auth.models import User


@pytest.mark.asyncio
class TestStudentCRUD:
    async def test_create_and_get_student(self, db_session, client):
        """Test creating and retrieving a student."""
        user_id = uuid4()
        school_id = uuid4()
        user = User(
            id=user_id,
            school_id=school_id,
            email="teacher@test.com",
            password_hash=hash_password("Pass123!"),
            first_name="Teacher",
            last_name="Test",
            role="school_admin",
            status="active",
        )
        db_session.add(user)
        await db_session.commit()

        # Login to get cookies
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "teacher@test.com", "password": "Pass123!"},
        )
        cookies = response.cookies

        # Create student
        student_data = {
            "first_name": "Student",
            "last_name": "One",
            "date_of_birth": str(date.today() - timedelta(days=365 * 14)),
            "gender": "male",
            "admission_number": "EDU/2024/0001",
            "admission_date": str(date.today() - timedelta(days=30)),
        }
        response = await client.post(
            "/api/v1/students",
            json=student_data,
            cookies=cookies,
        )
        assert response.status_code == 201
        student = response.json()
        assert student["first_name"] == "Student"
        assert student["admission_number"] == "EDU/2024/0001"

        student_id = student["id"]

        # Get student
        response = await client.get(
            f"/api/v1/students/{student_id}",
            cookies=cookies,
        )
        assert response.status_code == 200
        assert response.json()["id"] == student_id
