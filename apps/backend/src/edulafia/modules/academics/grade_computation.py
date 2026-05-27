"""Grade computation service for calculating grades and rankings."""

from decimal import Decimal


class GradeComputationService:
    """Service for grade computation business logic."""

    @staticmethod
    def get_default_grading_rules() -> list[dict]:
        """Get the default WAEC grading scale rules."""
        return [
            {"grade": "A1", "min_score": 75, "max_score": 100, "remark": "Excellent", "position": 1},
            {"grade": "B2", "min_score": 70, "max_score": 74, "remark": "Very Good", "position": 2},
            {"grade": "B3", "min_score": 65, "max_score": 69, "remark": "Good", "position": 3},
            {"grade": "C4", "min_score": 60, "max_score": 64, "remark": "Credit", "position": 4},
            {"grade": "C5", "min_score": 55, "max_score": 59, "remark": "Credit", "position": 5},
            {"grade": "C6", "min_score": 50, "max_score": 54, "remark": "Credit", "position": 6},
            {"grade": "D7", "min_score": 45, "max_score": 49, "remark": "Pass", "position": 7},
            {"grade": "E8", "min_score": 40, "max_score": 44, "remark": "Pass", "position": 8},
            {"grade": "F9", "min_score": 0, "max_score": 39, "remark": "Fail", "position": 9},
        ]

    @staticmethod
    def compute_grade(
        score: Decimal,
        grading_rules: list[dict] | None = None,
    ) -> dict:
        """Compute grade for a given score."""
        if grading_rules is None:
            grading_rules = GradeComputationService.get_default_grading_rules()

        # Clamp score to valid range
        score = max(Decimal("0"), min(score, Decimal("100")))
        score = round(score) # Round to nearest integer for accurate grading against integer boundaries

        # Find matching grade
        for rule in grading_rules:
            min_score = Decimal(str(rule["min_score"]))
            max_score = Decimal(str(rule["max_score"]))
            if min_score <= score <= max_score:
                return {
                    "grade": rule["grade"],
                    "remark": rule["remark"],
                    "position": rule["position"],
                }

        # Default to F9 if no match
        return {
            "grade": "F9",
            "remark": "Fail",
            "position": 9,
        }

    @staticmethod
    def calculate_total_score(
        ca_total: Decimal,
        exam_score: Decimal,
    ) -> Decimal:
        """Calculate total score from CA and exam scores."""
        return ca_total + exam_score

    @staticmethod
    def calculate_weighted_total(
        ca_raw: Decimal,
        exam_raw: Decimal,
        ca_max: Decimal = Decimal("30"),
        exam_max: Decimal = Decimal("70"),
    ) -> Decimal:
        """Calculate weighted total score with configurable weights."""
        # Normalize scores to their respective weights, guarding against division by zero
        ca_weighted = (ca_raw / ca_max) * ca_max if ca_max > 0 else Decimal("0")
        exam_weighted = (exam_raw / exam_max) * exam_max if exam_max > 0 else Decimal("0")
        return ca_weighted + exam_weighted

    @staticmethod
    def calculate_class_ranks(scores: list[dict]) -> list[dict]:
        """Calculate class ranks from a list of student scores.

        Args:
            scores: List of dicts with 'student_id', 'total_score', and optional 'flag'

        Returns:
            List of dicts with added 'rank' field
        """
        if not scores:
            return []

        # Separate ranked and excluded students
        ranked_students = []
        excluded_students = []

        for score_entry in scores:
            flag = score_entry.get("flag")
            if flag in ("ABS", "INC"):
                # Exclude absent/incomplete students from ranking
                score_entry["rank"] = None
                excluded_students.append(score_entry)
            else:
                ranked_students.append(score_entry)

        # Sort by total score descending
        ranked_students.sort(
            key=lambda x: x["total_score"],
            reverse=True,
        )

        # Assign ranks with tie handling
        current_rank = 1
        previous_score = None
        same_rank_count = 0

        for i, student in enumerate(ranked_students):
            if previous_score is None or student["total_score"] < previous_score:
                # New rank (not tied)
                current_rank = i + 1
                same_rank_count = 0
            else:
                # Tied with previous
                same_rank_count += 1

            student["rank"] = current_rank
            previous_score = student["total_score"]

        # Combine and return
        return ranked_students + excluded_students

    @staticmethod
    def validate_grading_scale(rules: list[dict]) -> bool:
        """Validate that grading scale has complete coverage without overlaps."""
        if not rules:
            return False

        # Check for complete coverage of 0-100 range
        covered_ranges = []
        for rule in rules:
            min_score = float(rule["min_score"])
            max_score = float(rule["max_score"])
            if min_score > max_score:
                return False
            covered_ranges.append((min_score, max_score))

        # Sort by min_score
        covered_ranges.sort(key=lambda x: x[0])

        # Check for gaps or overlaps
        for i in range(1, len(covered_ranges)):
            prev_max = covered_ranges[i - 1][1]
            curr_min = covered_ranges[i][0]

            # Allow small gaps (shouldn't happen with proper WAEC scale)
            if curr_min > prev_max + 1:
                return False

        # Check full coverage from 0 to 100
        first_min = covered_ranges[0][0]
        last_max = covered_ranges[-1][1]

        if first_min > 0 or last_max < 100:
            return False

        return True
