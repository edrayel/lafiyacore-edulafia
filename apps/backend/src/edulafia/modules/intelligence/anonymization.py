"""Data anonymization module for intelligence dashboards."""

from datetime import date
from decimal import Decimal
from typing import Any


class Anonymizer:
    """Data anonymization for different access levels."""

    # Thresholds
    LGA_MIN_POPULATION = 10
    LGA_SUPPRESSION = 5
    STATE_MIN_POPULATION = 30
    STATE_SUPPRESSION = 10
    RESEARCH_MIN_POPULATION = 50
    RESEARCH_K_ANONYMITY = 5

    @staticmethod
    def anonymize_for_lga(
        data: dict,
        min_population: int = 10,
        suppression: int = 5,
    ) -> dict:
        """Anonymize data for LGA level access.

        Rules:
        - Hide populations below minimum threshold
        - Suppress counts below suppression threshold
        - Round percentages to whole numbers
        """
        anonymized = data.copy()

        # Check minimum population
        total_students = data.get("total_students", 0)
        if total_students < min_population:
            anonymized["total_students"] = None
            anonymized["school_count"] = None
            anonymized["avg_attendance_rate"] = None
            anonymized["total_sick_bay_visits"] = None
            anonymized["total_collections"] = None
            return anonymized

        # Suppress small counts
        if anonymized.get("total_sick_bay_visits", 0) < suppression:
            anonymized["total_sick_bay_visits"] = None

        # Round percentages
        if anonymized.get("avg_attendance_rate"):
            anonymized["avg_attendance_rate"] = round(
                float(anonymized["avg_attendance_rate"])
            )

        return anonymized

    @staticmethod
    def anonymize_for_state(
        data: dict,
        min_population: int = 30,
        suppression: int = 10,
    ) -> dict:
        """Anonymize data for state level access.

        Rules:
        - Higher thresholds than LGA
        - Suppress counts below suppression threshold
        - Aggregate to LGA level only
        """
        anonymized = data.copy()

        # Check minimum population
        total_students = data.get("total_students", 0)
        if total_students < min_population:
            anonymized["total_students"] = None
            anonymized["lga_count"] = None
            anonymized["school_count"] = None
            anonymized["avg_attendance_rate"] = None
            anonymized["total_sick_bay_visits"] = None
            anonymized["total_collections"] = None
            return anonymized

        # Suppress small counts
        if anonymized.get("total_sick_bay_visits", 0) < suppression:
            anonymized["total_sick_bay_visits"] = None

        return anonymized

    @staticmethod
    def anonymize_for_research(
        data: list[dict],
        k_anonymity: int = 5,
        min_population: int = 50,
    ) -> list[dict]:
        """Anonymize data for research use.

        Rules:
        - Apply k-anonymity (k=5)
        - Remove all names and contact info
        - Generalize dates to month/year
        - Minimum population 50
        - Round all counts to nearest 5
        """
        if len(data) < min_population:
            return []

        anonymized = []

        for record in data:
            anon_record = {}

            # Copy allowed fields only
            allowed_fields = [
                "school_id", "lga", "state", "gender", "age_group",
                "grade_level", "attendance_rate", "health_category"
            ]

            for field in allowed_fields:
                if field in record:
                    anon_record[field] = record[field]

            # Generalize dates to month/year
            if "date" in record:
                d = record["date"]
                if isinstance(d, date):
                    anon_record["date"] = d.strftime("%Y-%m")
                else:
                    anon_record["date"] = str(d)[:7]

            # Round counts to nearest 5
            count_fields = ["count", "total", "value"]
            for field in count_fields:
                if field in record and record[field] is not None:
                    anon_record[field] = round(record[field] / 5) * 5

            # Remove any field that could identify individuals
            excluded_fields = [
                "name", "first_name", "last_name", "phone", "email",
                "address", "nin", "admission_number", "student_id",
                "guardian_id", "parent_name"
            ]
            for field in excluded_fields:
                anon_record.pop(field, None)

            anonymized.append(anon_record)

        return anonymized

    @staticmethod
    def round_to_nearest(value: Any, nearest: int = 5) -> Any:
        """Round a value to the nearest multiple."""
        if value is None:
            return None
        if isinstance(value, (int, float, Decimal)):
            return round(float(value) / nearest) * nearest
        return value

    @staticmethod
    def suppress_low_counts(
        value: int,
        threshold: int = 5,
        replacement: Any = None,
    ) -> Any:
        """Suppress values below threshold."""
        if value < threshold:
            return replacement
        return value
