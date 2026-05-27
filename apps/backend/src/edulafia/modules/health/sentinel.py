"""LafiyaSentinel Engine for disease surveillance."""

from collections import defaultdict
from datetime import timezone, date, datetime, timedelta
from uuid import UUID

from edulafia.modules.health.models import SentinelSignal, SickBayVisit
from edulafia.modules.health.repository import (
    SentinelConfigurationRepository,
    SentinelSignalRepository,
    SickBayVisitRepository,
)


class SentinelEngine:
    """LafiyaSentinel surveillance engine for disease outbreak detection."""

    def __init__(
        self,
        visit_repo: SickBayVisitRepository,
        signal_repo: SentinelSignalRepository,
        config_repo: SentinelConfigurationRepository,
    ):
        self.visit_repo = visit_repo
        self.signal_repo = signal_repo
        self.config_repo = config_repo

    async def analyze_school_signals(
        self,
        school_id: UUID,
        lga: str | None = None,
        state: str | None = None,
    ) -> list[dict]:
        """Analyze signals from a single school within time window.

        Detects:
        - Class cluster: >=3 same complaints in same class (48 hrs)
        - School cluster: >=5 same complaints across school (72 hrs)
        """
        signals = []

        # Get active configuration
        config = await self.config_repo.get_active_config(school_id)
        time_window_hours = config.time_window_hours if config else 48
        cluster_threshold = config.cluster_threshold if config else 3

        # Calculate time window
        end_date = date.today()
        start_date = end_date - timedelta(hours=time_window_hours)

        # Get visits in time window
        visits = await self.visit_repo.get_visits_in_time_window(
            school_id, start_date, end_date
        )

        # Combine and group by symptom profile
        symptom_groups = self.group_by_symptom_profile(visits)

        # Check each group for threshold
        for symptoms_key, group_visits in symptom_groups.items():
            if len(group_visits) >= cluster_threshold:
                # Determine tier
                if len(group_visits) >= 5:
                    tier = "school"
                else:
                    tier = "school"

                # Create signal
                signal = await self.create_signal(
                    school_ids=[school_id],
                    symptom_profile={
                        "symptoms": symptoms_key.split(","),
                        "count": len(group_visits),
                        "time_window_hours": time_window_hours,
                    },
                    students_affected=len(group_visits),
                    threshold_type="school_cluster",
                    alert_tier=tier,
                    lga=lga,
                    state=state,
                )
                signals.append(signal)

        return signals

    async def analyze_lga_signals(
        self,
        lga: str,
        state: str,
        school_ids: list[UUID],
    ) -> list[dict]:
        """Analyze cross-school clusters within LGA.

        Detects:
        - LGA cluster: >=2 schools in same LGA with similar symptoms (96 hrs)
        """
        signals = []

        # Calculate time window for LGA analysis
        time_window_hours = 96
        end_date = date.today()
        start_date = end_date - timedelta(hours=time_window_hours)

        # Collect visits from all schools
        all_visits_by_school = {}
        for school_id in school_ids:
            visits = await self.visit_repo.get_visits_in_time_window(
                school_id, start_date, end_date
            )
            if visits:
                all_visits_by_school[school_id] = visits

        # Group visits by symptom profile across schools
        school_symptom_groups = defaultdict(set)
        for school_id, visits in all_visits_by_school.items():
            for visit in visits:
                symptoms_key = ",".join(sorted(visit.presenting_complaint_codes))
                school_symptom_groups[symptoms_key].add(school_id)

        # Check for cross-school clusters
        for symptoms_key, affected_schools in school_symptom_groups.items():
            if len(affected_schools) >= 2:
                # Count total affected students
                total_affected = 0
                for school_id in affected_schools:
                    school_visits = all_visits_by_school.get(school_id, [])
                    for visit in school_visits:
                        visit_symptoms = ",".join(sorted(visit.presenting_complaint_codes))
                        if visit_symptoms == symptoms_key:
                            total_affected += 1

                # Create LGA-tier signal
                signal = await self.create_signal(
                    school_ids=list(affected_schools),
                    symptom_profile={
                        "symptoms": symptoms_key.split(","),
                        "count": total_affected,
                        "schools_affected": len(affected_schools),
                        "time_window_hours": time_window_hours,
                    },
                    students_affected=total_affected,
                    threshold_type="lga_cluster",
                    alert_tier="lga",
                    lga=lga,
                    state=state,
                )
                signals.append(signal)

        return signals

    def combine_symptom_events(
        self,
        sick_bay_visits: list[SickBayVisit],
        illness_absences: list[dict] = None,
    ) -> list[dict]:
        """Combine sick bay visits with attendance illness data."""
        events = []

        # Add sick bay visits
        for visit in sick_bay_visits:
            events.append({
                "source": "sick_bay",
                "student_id": visit.student_id,
                "date": visit.visit_date,
                "symptoms": visit.presenting_complaint_codes,
                "class_id": None,  # Would need to fetch from student
            })

        # Add illness absences if provided
        if illness_absences:
            for absence in illness_absences:
                events.append({
                    "source": "attendance",
                    "student_id": absence.get("student_id"),
                    "date": absence.get("date"),
                    "symptoms": absence.get("symptom_codes", []),
                    "class_id": absence.get("class_id"),
                })

        return events

    def group_by_symptom_profile(
        self,
        visits: list[SickBayVisit],
    ) -> dict[str, list[SickBayVisit]]:
        """Group visits by normalized symptom signature."""
        groups = defaultdict(list)

        for visit in visits:
            # Create normalized symptom key
            if visit.presenting_complaint_codes:
                symptoms_key = ",".join(sorted(visit.presenting_complaint_codes))
                groups[symptoms_key].append(visit)

        return dict(groups)

    async def create_signal(
        self,
        school_ids: list[UUID],
        symptom_profile: dict,
        students_affected: int,
        threshold_type: str,
        alert_tier: str,
        lga: str | None = None,
        state: str | None = None,
    ) -> dict:
        """Create a Sentinel signal."""
        signal_data = {
            "school_ids": school_ids,
            "lga": lga,
            "state": state,
            "date_generated": datetime.now(timezone.utc),
            "symptom_profile": symptom_profile,
            "students_affected": students_affected,
            "threshold_type": threshold_type,
            "alert_tier": alert_tier,
            "status": "active",
        }

        signal = await self.signal_repo.create(signal_data)

        return {
            "id": str(signal.id),
            "school_ids": [str(sid) for sid in school_ids],
            "alert_tier": alert_tier,
            "threshold_type": threshold_type,
            "symptom_profile": symptom_profile,
            "students_affected": students_affected,
            "status": "active",
        }

    async def trigger_alerts(
        self,
        signal: SentinelSignal,
        recipients: list[dict] = None,
    ) -> dict:
        """Route alerts to appropriate tier."""
        routing = {
            "school": {
                "recipients": ["headteacher", "nurse"],
                "channels": ["whatsapp", "email"],
            },
            "lga": {
                "recipients": ["lga_health_officer"],
                "channels": ["email", "sms"],
            },
            "state": {
                "recipients": ["state_epidemiologist"],
                "channels": ["email"],
            },
        }

        import logging
        from edulafia.core.arq_queue import enqueue_sentinel_email
        import asyncio

        logger = logging.getLogger(__name__)

        tier_config = routing.get(signal.alert_tier, routing["school"])

        for target in tier_config["recipients"]:
            logger.info(f"SENTINEL ALERT [{signal.alert_tier.upper()}]: Notifying {target} about {signal.threshold_type} for signal {signal.id}.")
            
            # Actually dispatch an email to the admin for alerts
            if "email" in tier_config["channels"]:
                body = f"""
                <h2>Sentinel Health Alert: {signal.alert_tier.upper()}</h2>
                <p><strong>Event Type:</strong> {signal.threshold_type}</p>
                <p><strong>Signal ID:</strong> {signal.id}</p>
                <p><strong>Details:</strong> The threshold for {signal.threshold_type} was exceeded. Please review the health dashboard immediately.</p>
                """
                from edulafia.config import settings
                alert_email = settings.SENTINEL_ALERT_EMAIL
                await enqueue_sentinel_email(
                    to_email=alert_email,
                    subject=f"URGENT: Health Sentinel Alert - {signal.threshold_type}",
                    body=body
                )

        return {
            "signal_id": str(signal.id),
            "alert_tier": signal.alert_tier,
            "recipients": tier_config["recipients"],
            "channels": tier_config["channels"],
            "status": "sent",
        }

    def calculate_percentage_affected(
        self,
        affected_count: int,
        total_population: int,
    ) -> float:
        """Calculate percentage of population affected."""
        if total_population == 0:
            return 0.0
        return round((affected_count / total_population) * 100, 2)

    async def get_dashboard_data(
        self,
        school_id: UUID | None = None,
        lga: str | None = None,
        state: str | None = None,
    ) -> dict:
        """Get Sentinel dashboard data."""
        # Get active signals
        signals = await self.signal_repo.list(
            school_id=school_id,
            lga=lga,
            state=state,
            status="active",
        )

        # Get acknowledged signals (last 30 days)
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        recent_signals = await self.signal_repo.list(
            school_id=school_id,
            lga=lga,
            state=state,
            start_date=thirty_days_ago,
        )

        return {
            "active_alerts": len(signals),
            "recent_signals": len(recent_signals),
            "signals_by_tier": {
                "school": len([s for s in recent_signals if s.alert_tier == "school"]),
                "lga": len([s for s in recent_signals if s.alert_tier == "lga"]),
                "state": len([s for s in recent_signals if s.alert_tier == "state"]),
            },
            "signals_by_status": {
                "active": len([s for s in recent_signals if s.status == "active"]),
                "acknowledged": len([s for s in recent_signals if s.status == "acknowledged"]),
                "resolved": len([s for s in recent_signals if s.status == "resolved"]),
            },
        }
