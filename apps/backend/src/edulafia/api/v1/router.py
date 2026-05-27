"""API v1 router aggregation."""

from fastapi import APIRouter

from edulafia.api.v1 import guardians, students
from edulafia.api.v1.health import router as v1_health_router
from edulafia.modules.academics.api.scores import router as scores_router
from edulafia.modules.academics.api.subjects import router as subjects_router
from edulafia.modules.accreditation.api.router import router as accreditation_router
from edulafia.modules.admin.api.admin import (
    analytics_router,
    backup_router,
    schools_router,
    sentinel_router,
    sync_router,
    training_router,
    updates_router,
    users_router,
)

# New module routers
from edulafia.modules.admissions.api.router import router as admissions_router
from edulafia.modules.attendance.api.attendance import router as attendance_router
from edulafia.modules.auth.api.auth import router as auth_router
from edulafia.modules.building_projects.api.router import router as building_projects_router
from edulafia.modules.bus_tracking.api.router import router as bus_tracking_router
from edulafia.modules.cafeteria.api.router import router as cafeteria_router
from edulafia.modules.clubs.api.router import router as clubs_router
from edulafia.modules.custody.api.router import router as custody_router
from edulafia.modules.data_retention.api.router import router as data_retention_router
from edulafia.modules.discipline.api.router import router as discipline_router
from edulafia.modules.emergency.api.router import router as emergency_router
from edulafia.modules.exam_registration.api.router import router as exam_registration_router
from edulafia.modules.finance.api.fees import router as fees_router
from edulafia.modules.finance.api.webhooks import router as webhooks_router
from edulafia.modules.fundraising.api.router import router as fundraising_router
from edulafia.modules.girl_child_tracking.api.router import router as girl_child_tracking_router
from edulafia.modules.health.api.health import router as health_router
from edulafia.modules.health.api.sentinel import router as sentinel_router
from edulafia.modules.inspection_tracking.api.router import router as inspection_tracking_router
from edulafia.modules.intelligence.api.intelligence import router as intelligence_router
from edulafia.modules.inventory.api.router import router as inventory_router
from edulafia.modules.leave_management.api.router import router as leave_management_router
from edulafia.modules.library.api.router import router as library_router
from edulafia.modules.ministry_reporting.api.router import router as ministry_reporting_router
from edulafia.modules.parent.api.parent import router as parent_router
from edulafia.modules.payroll.api.router import router as payroll_router
from edulafia.modules.proprietor.api.router import router as proprietor_router
from edulafia.modules.smc_reporting.api.router import router as smc_reporting_router
from edulafia.modules.special_needs.api.router import router as special_needs_router
from edulafia.modules.staff.api.attendance import router as staff_attendance_router
from edulafia.modules.staff.api.staff import router as staff_router
from edulafia.modules.staff.api.timetable import router as timetable_router
from edulafia.modules.waec_bulk.api.router import router as waec_bulk_router

from edulafia.modules.messaging.api.router import router as messaging_router
from edulafia.modules.lms.api.router import router as lms_router
from edulafia.modules.hostel.api.router import router as hostel_router
from edulafia.modules.calendar.api.router import router as calendar_router
from edulafia.modules.alumni.api.router import router as alumni_router

api_router = APIRouter(prefix="/v1")

# Include all module routers
api_router.include_router(v1_health_router, tags=["Health"])
api_router.include_router(auth_router, tags=["Authentication"])

# Privacy & compliance
@api_router.get("/privacy-policy", tags=["Compliance"])
async def privacy_policy():
    """Return the platform privacy policy summary."""
    return {
        "status": "success",
        "data": {
            "policy": (
                "EduLafia collects and processes student personal data in accordance with "
                "the Nigeria Data Protection Regulation (NDPR) and applicable data protection laws. "
                "Data collected includes student demographics, academic records, attendance, "
                "and health information, each with appropriate consent. "
                "Data is stored within AWS af-south-1 (Cape Town) region. "
                "Retention periods are configurable per school. "
                "Data Subject Requests can be submitted via POST /api/v1/data-retention/dsr. "
                "Contact the school administrator for questions about your data."
            ),
            "data_controller": "School administrator",
            "jurisdiction": "Nigeria (NDPR)",
            "data_residency": "AWS af-south-1 (Cape Town)",
        },
    }

api_router.include_router(students.router, tags=["Students"])
api_router.include_router(guardians.router, tags=["Guardians"])
api_router.include_router(subjects_router, tags=["Subjects"])
api_router.include_router(scores_router, tags=["Academics"])
api_router.include_router(attendance_router, tags=["Attendance"])
api_router.include_router(fees_router, tags=["Finance"])
api_router.include_router(webhooks_router, tags=["Finance Webhooks"])
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(sentinel_router, tags=["Sentinel"])
api_router.include_router(staff_router, tags=["Staff"])
api_router.include_router(timetable_router, tags=["Staff Timetables"])
api_router.include_router(staff_attendance_router, tags=["Staff Attendance"])
api_router.include_router(parent_router, tags=["Parent Portal"])
api_router.include_router(intelligence_router, tags=["Intelligence"])

# Admin module routers
api_router.include_router(schools_router, tags=["School Provisioning"])
api_router.include_router(users_router, tags=["User Management"])
api_router.include_router(sync_router, tags=["Sync Monitoring"])
api_router.include_router(updates_router, tags=["System Updates"])
api_router.include_router(backup_router, tags=["System Backups"])
api_router.include_router(training_router, tags=["Training Resources"])
api_router.include_router(analytics_router, tags=["Analytics"])

# New module routers
api_router.include_router(admissions_router, tags=["Admissions"])
api_router.include_router(emergency_router, tags=["Emergency"])
api_router.include_router(special_needs_router, tags=["Special Needs"])
api_router.include_router(custody_router, tags=["Custody"])
api_router.include_router(data_retention_router, tags=["Data Retention"])
api_router.include_router(inventory_router, tags=["Inventory"])
api_router.include_router(library_router, tags=["Library"])
api_router.include_router(cafeteria_router, tags=["Cafeteria"])
api_router.include_router(clubs_router, tags=["Clubs"])
api_router.include_router(bus_tracking_router, tags=["Bus Tracking"])
api_router.include_router(payroll_router, tags=["Payroll"])
api_router.include_router(leave_management_router, tags=["Leave Management"])
api_router.include_router(exam_registration_router, tags=["Exam Registration"])
api_router.include_router(girl_child_tracking_router, tags=["Girl-Child Tracking"])
api_router.include_router(discipline_router, tags=["Discipline"])
api_router.include_router(inspection_tracking_router, tags=["Inspections"])
api_router.include_router(accreditation_router, tags=["Accreditation"])
api_router.include_router(fundraising_router, tags=["Fundraising"])
api_router.include_router(building_projects_router, tags=["Building Projects"])
api_router.include_router(ministry_reporting_router, tags=["Ministry Reports"])
api_router.include_router(proprietor_router, tags=["Proprietor Dashboard"])
api_router.include_router(smc_reporting_router, tags=["SMC Reports"])
api_router.include_router(waec_bulk_router, tags=["WAEC Bulk Registration"])

api_router.include_router(messaging_router, tags=["Messaging"])
api_router.include_router(lms_router, tags=["LMS & Homework"])
api_router.include_router(hostel_router, tags=["Hostel Management"])
api_router.include_router(calendar_router, tags=["School Calendar"])
api_router.include_router(alumni_router, tags=["Alumni Network"])

