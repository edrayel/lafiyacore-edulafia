from __future__ import annotations

from datetime import date
from uuid import UUID, uuid4

import pytest

pytestmark = pytest.mark.skip(reason="Needs proper DB setup")

from edulafia.core.security import create_access_token, create_user_token_payload
from edulafia.modules.academics.models import AcademicYear
from edulafia.modules.admin.models import School
from edulafia.modules.finance.models import FeeSchedule
from edulafia.modules.health.models import StudentHealthProfile
from edulafia.modules.students.models import Student


def make_headers(*, role: str, school_id: UUID, user_id: UUID | None = None) -> dict[str, str]:
    payload = create_user_token_payload(
        user_id=user_id or uuid4(),
        role=role,
        school_id=school_id,
    )
    token = create_access_token(payload)
    return {"Authorization": f"Bearer {token}"}


async def create_school(db_session, *, school_id: UUID, code: str) -> School:
    school = School(
        id=school_id,
        name=f"Test School {code}",
        code=code,
        status="active",
    )
    db_session.add(school)
    await db_session.commit()
    return school


async def create_academic_year(db_session, *, school_id: UUID) -> AcademicYear:
    academic_year = AcademicYear(
        id=uuid4(),
        school_id=school_id,
        name="2025/2026",
        start_date=date(2025, 9, 1),
        end_date=date(2026, 7, 31),
        is_active=True,
    )
    db_session.add(academic_year)
    await db_session.commit()
    return academic_year


async def create_student(db_session, *, school_id: UUID, student_id: UUID | None = None) -> Student:
    student = Student(
        id=student_id or uuid4(),
        school_id=school_id,
        admission_number=f"ADM-{uuid4().hex[:8].upper()}",
        first_name="Test",
        last_name="Student",
        date_of_birth=date(2012, 1, 1),
        gender="male",
        admission_date=date(2025, 9, 1),
        status="active",
    )
    db_session.add(student)
    await db_session.commit()
    return student


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.security
class TestPrivilegedEndpointAuthorization:
    async def test_admin_backup_create_forbidden_for_wrong_role(self, client, db_session):
        school_id = uuid4()
        await create_school(db_session, school_id=school_id, code="ADM001")

        headers = make_headers(role="school_admin", school_id=school_id)
        response = await client.post("/api/v1/admin/backup/create", headers=headers)
        assert response.status_code == 403

    async def test_admin_backup_create_allowed_for_owner(self, client, db_session):
        school_id = uuid4()
        await create_school(db_session, school_id=school_id, code="ADM002")

        headers = make_headers(role="owner", school_id=school_id)
        response = await client.post("/api/v1/admin/backup/create", headers=headers)
        assert response.status_code == 200

    async def test_finance_record_payment_forbidden_for_wrong_role(self, client, db_session):
        school_id = uuid4()
        await create_school(db_session, school_id=school_id, code="FIN001")
        student = await create_student(db_session, school_id=school_id)

        headers = make_headers(role="school_admin", school_id=school_id)
        response = await client.post(
            "/api/v1/finance/payments",
            headers=headers,
            json={
                "student_id": str(student.id),
                "amount": "1000.00",
                "payment_method": "cash",
                "payment_reference": "TEST-REF-001",
                "description": "Test payment",
            },
        )
        assert response.status_code == 403

    async def test_finance_fee_schedule_not_accessible_cross_school(self, client, db_session):
        school_a = uuid4()
        school_b = uuid4()
        await create_school(db_session, school_id=school_a, code="FINA01")
        await create_school(db_session, school_id=school_b, code="FINB01")
        academic_year_b = await create_academic_year(db_session, school_id=school_b)

        schedule = FeeSchedule(
            id=uuid4(),
            school_id=school_b,
            academic_year_id=academic_year_b.id,
            name="Other School Fees",
            description=None,
            is_active=True,
        )
        db_session.add(schedule)
        await db_session.commit()

        headers = make_headers(role="school_admin", school_id=school_a)
        response = await client.get(
            f"/api/v1/finance/fee-schedules/{schedule.id}",
            headers=headers,
        )
        assert response.status_code == 404

    async def test_health_sick_bay_visit_forbidden_for_wrong_role(self, client, db_session):
        school_id = uuid4()
        await create_school(db_session, school_id=school_id, code="HLT001")
        student = await create_student(db_session, school_id=school_id)

        headers = make_headers(role="teacher", school_id=school_id)
        response = await client.post(
            "/api/v1/health/sick-bay-visits",
            headers=headers,
            json={
                "student_id": str(student.id),
                "presenting_complaint_codes": ["fever"],
                "outcome": "returned_to_class",
            },
        )
        assert response.status_code == 403

    async def test_health_profile_not_accessible_cross_school(self, client, db_session):
        school_a = uuid4()
        school_b = uuid4()
        await create_school(db_session, school_id=school_a, code="HLTA01")
        await create_school(db_session, school_id=school_b, code="HLTB01")
        student_b = await create_student(db_session, school_id=school_b)

        profile = StudentHealthProfile(
            id=uuid4(),
            student_id=student_b.id,
            school_id=school_b,
            blood_group="O+",
            genotype="AA",
            parental_consent_given=True,
        )
        db_session.add(profile)
        await db_session.commit()

        headers = make_headers(role="nurse", school_id=school_a)
        response = await client.get(
            f"/api/v1/health/students/{student_b.id}/profile",
            headers=headers,
        )
        assert response.status_code == 404

    async def test_proprietor_dashboard_forbidden_for_wrong_role(self, client, db_session):
        school_id = uuid4()
        await create_school(db_session, school_id=school_id, code="PRP001")

        headers = make_headers(role="teacher", school_id=school_id)
        response = await client.get("/api/v1/proprietor/dashboard/summary", headers=headers)
        assert response.status_code == 403

    async def test_proprietor_dashboard_allowed_for_owner(self, client, db_session):
        school_id = uuid4()
        await create_school(db_session, school_id=school_id, code="PRP002")

        headers = make_headers(role="owner", school_id=school_id)
        response = await client.get("/api/v1/proprietor/dashboard/summary", headers=headers)
        assert response.status_code == 200
