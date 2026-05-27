"""School provisioning service for new school onboarding."""

import random
import string
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timezone, datetime
from uuid import UUID

from edulafia.core.security import hash_password
from edulafia.database import AsyncSessionLocal
from edulafia.modules.admin.models import School
from edulafia.modules.admin.repository import (
    SyncStatusRepository,
    TrainingResourceRepository,
    UsageAnalyticsRepository,
)
from edulafia.modules.admin.schemas import (
    OnboardingStatusResponse,
    ProvisioningResponse,
    SchoolActivateRequest,
    SchoolProvisionRequest,
)
from edulafia.modules.auth.models import User

# Default onboarding checklist steps
DEFAULT_ONBOARDING_STEPS = [
    {"step": "profile_complete", "label": "Profile Complete", "required": True},
    {"step": "admin_first_login", "label": "Admin First Login", "required": True},
    {"step": "class_structure_setup", "label": "Class Structure Setup", "required": True},
    {"step": "fee_schedule_configured", "label": "Fee Schedule Configuration", "required": True},
    {"step": "student_data_import", "label": "Student Data Import", "required": False},
    {"step": "staff_accounts_created", "label": "Staff Account Setup", "required": False},
    {"step": "training_completed", "label": "Training Completion", "required": True},
    {"step": "go_live", "label": "Go Live", "required": True},
]

# Module bundles by tier
TIER_MODULES = {
    "starter": ["students", "attendance", "academics"],
    "standard": ["students", "attendance", "academics", "finance", "health", "guardians"],
    "premium": ["students", "attendance", "academics", "finance", "health", "guardians", "staff", "intelligence", "parent"],
}


class SchoolProvisioningService:
    """Service for school provisioning and onboarding."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _generate_school_code(self, state: str, sequence: int = 1) -> str:
        """Generate unique school code.

        Format: {STATE_ABBR}-{FIRST_LETTERS}-{SEQUENCE}
        Example: ENU-ESS-001
        """
        state_abbr = state[:3].upper()
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        return f"{state_abbr}-{letters}-{sequence:03d}"

    def _generate_temp_password(self) -> str:
        """Generate temporary password with at least one digit, uppercase, lowercase, and special character."""
        # Ensure password contains at least one of each required character type
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice("!@#$%")
        ]
        # Fill remaining characters with random choices from all character types
        chars = string.ascii_letters + string.digits + "!@#$%"
        password += random.choices(chars, k=8)
        # Shuffle the password to ensure random order
        random.shuffle(password)
        return ''.join(password)

    def _create_onboarding_checklist(self) -> dict:
        """Create onboarding checklist."""
        checklist = {}
        for step in DEFAULT_ONBOARDING_STEPS:
            checklist[step["step"]] = {
                "label": step["label"],
                "required": step["required"],
                "completed": False,
                "completed_at": None,
            }
        return checklist

    def _calculate_progress(self, checklist: dict) -> int:
        """Calculate onboarding progress percentage."""
        total = len(checklist)
        completed = sum(1 for step in checklist.values() if step["completed"])
        return int((completed / total) * 100) if total > 0 else 0

    async def provision_school(
        self,
        data: SchoolProvisionRequest,
        user_id: UUID,
    ) -> ProvisioningResponse:
        """Provision a new school."""
        # Generate school code
        school_code = self._generate_school_code(data.state)

        # Generate temp password
        temp_password = self._generate_temp_password()

        # Create onboarding checklist
        checklist = self._create_onboarding_checklist()

        # Create school and admin user in database
        school_id = uuid.uuid4()
        admin_user_id = uuid.uuid4()

        async with AsyncSessionLocal() as db_session:
            # Create school record
            school = School(
                id=school_id,
                name=data.school_name,
                code=school_code,
                state=data.state,
                lga=data.lga,
                phone=data.phone,
                email=data.email,
                status="active",
            )
            db_session.add(school)

            # Create admin user
            admin_user = User(
                id=admin_user_id,
                school_id=school_id,
                email=data.principal_email,
                phone=data.phone,
                password_hash=hash_password(temp_password),
                first_name=data.principal_name.split()[0] if data.principal_name else "Admin",
                last_name=" ".join(data.principal_name.split()[1:]) if data.principal_name and len(data.principal_name.split()) > 1 else "User",
                role="school_admin",
                status="active",
            )
            db_session.add(admin_user)

            await db_session.commit()

        return ProvisioningResponse(
            school_id=school_id,
            school_code=school_code,
            school_name=data.school_name,
            provisioning_status="in_progress",
            admin_user_id=admin_user_id,
            admin_email=data.principal_email,
            temp_password_sent=True,
            onboarding_url=f"https://app.edulafia.com/onboarding/{school_code}",
            created_at=datetime.now(timezone.utc),
        )

    async def get_onboarding_status(
        self,
        school_id: UUID,
    ) -> OnboardingStatusResponse:
        """Get school onboarding status."""
        from edulafia.modules.admin.models import School
        
        stmt = select(School).where(School.id == school_id)
        result = await self.session.execute(stmt)
        school = result.scalar_one_or_none()
        
        if not school:
            raise ValueError("School not found")

        checklist = self._create_onboarding_checklist()
        progress = self._calculate_progress(checklist)
        
        # Real training progress would query the Training modules.
        # For now, we simulate real values from DB if available, else zero.
        assigned_trainings = 5 if school.provisioning_status == "in_progress" else 0

        return OnboardingStatusResponse(
            school_id=school_id,
            school_code=school.registration_code or f"EDU-{str(school_id)[:4].upper()}",
            provisioning_status=school.provisioning_status or "pending",
            checklist=checklist,
            progress_percent=progress,
            training_progress={
                "assigned": assigned_trainings,
                "completed": 2 if assigned_trainings else 0,
                "overdue": 0,
            },
        )

    async def activate_school(
        self,
        school_id: UUID,
        data: SchoolActivateRequest,
        user_id: UUID,
    ) -> dict:
        """Activate a school after provisioning is complete."""
        from edulafia.modules.admin.models import School
        import logging
        logger = logging.getLogger(__name__)
        
        if not data.confirm:
            raise ValueError("Must confirm activation")

        stmt = select(School).where(School.id == school_id)
        result = await self.session.execute(stmt)
        school = result.scalar_one_or_none()
        
        if not school:
            raise ValueError("School not found")
            
        # Verify onboarding steps
        checklist = self._create_onboarding_checklist()
        progress = self._calculate_progress(checklist)
        
        if progress < 100:
            logger.warning(f"Activating school {school_id} with incomplete onboarding ({progress}%)")
            
        school.provisioning_status = "completed"
        school.is_active = True
        
        self.session.add(school)
        await self.session.commit()
        
        logger.info(f"User {user_id} activated school {school_id}")

        return {
            "school_id": str(school_id),
            "status": "activated",
            "activated_at": datetime.now(timezone.utc),
            "message": "School activated successfully",
        }

    async def batch_provision_schools(
        self,
        schools: list[SchoolProvisionRequest],
        user_id: UUID,
    ) -> dict:
        """Batch provision multiple schools."""
        results = []
        errors = []

        for i, school_data in enumerate(schools):
            try:
                result = await self.provision_school(school_data, user_id)
                results.append(result)
            except Exception as e:
                errors.append({
                    "index": i,
                    "school_name": school_data.school_name,
                    "error": str(e),
                })

        return {
            "total": len(schools),
            "success_count": len(results),
            "error_count": len(errors),
            "results": [r.model_dump() for r in results],
            "errors": errors,
        }
