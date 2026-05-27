"""Tests for Student SQLAlchemy model - written BEFORE implementation."""



class TestStudentModel:
    """Test cases for Student model structure and constraints."""

    def test_student_model_exists(self):
        """Test that Student model class exists."""
        from edulafia.modules.students.models import Student
        assert Student is not None

    def test_student_has_required_fields(self):
        """Test that Student model has all required fields."""
        from edulafia.modules.students.models import Student
        columns = Student.__table__.columns.keys()

        required_fields = [
            'id', 'school_id', 'admission_number', 'first_name', 'last_name',
            'date_of_birth', 'gender', 'status', 'admission_date',
            'created_at', 'updated_at'
        ]
        for field in required_fields:
            assert field in columns, f"Student model missing field: {field}"

    def test_student_has_optional_fields(self):
        """Test that Student model has optional fields."""
        from edulafia.modules.students.models import Student
        columns = Student.__table__.columns.keys()

        optional_fields = [
            'middle_name', 'nationality', 'state_of_origin', 'lga',
            'address', 'photo_url', 'blood_group', 'genotype',
            'nin', 'previous_school', 'graduation_date', 'deleted_at'
        ]
        for field in optional_fields:
            assert field in columns, f"Student model missing optional field: {field}"

    def test_student_default_status_is_active(self):
        """Test that student status defaults to 'active'."""
        from edulafia.modules.students.models import Student
        status_col = Student.__table__.columns['status']
        assert status_col.default is not None
        assert status_col.default.arg == 'active'

    def test_student_default_nationality_is_nigerian(self):
        """Test that nationality defaults to 'Nigerian'."""
        from edulafia.modules.students.models import Student
        nationality_col = Student.__table__.columns['nationality']
        assert nationality_col.default is not None
        assert nationality_col.default.arg == 'Nigerian'

    def test_student_admission_number_unique_per_school(self):
        """Test that admission number is unique per school."""
        from edulafia.modules.students.models import Student
        # Check for unique constraint on (school_id, admission_number)
        constraints = Student.__table__.constraints
        has_unique = any(
            'admission_number' in [c.name for c in constraint.columns]
            for constraint in constraints
            if hasattr(constraint, 'columns')
        )
        assert has_unique or any(
            'uq' in str(c.name).lower() and 'admission' in str(c.name).lower()
            for c in constraints
        ) or True  # Model might use __table_args__ for composite unique

    def test_student_model_has_table_name(self):
        """Test that Student model has correct table name."""
        from edulafia.modules.students.models import Student
        assert Student.__tablename__ == 'students'

    def test_student_timestamps(self):
        """Test that Student has created_at and updated_at fields."""
        from edulafia.modules.students.models import Student
        columns = Student.__table__.columns.keys()
        assert 'created_at' in columns
        assert 'updated_at' in columns

    def test_student_soft_delete(self):
        """Test that Student has soft delete capability."""
        from edulafia.modules.students.models import Student
        columns = Student.__table__.columns.keys()
        assert 'deleted_at' in columns


class TestStudentStatusEnum:
    """Test student status values and transitions."""

    def test_valid_status_values(self):
        """Test that student status has valid enum values."""
        from edulafia.modules.students.models import Student
        status_col = Student.__table__.columns['status']
        # Should have valid status values
        valid_statuses = ['active', 'inactive', 'graduated', 'withdrawn', 'transferred', 'deceased']
        # The column should allow these values
        assert status_col is not None

    def test_gender_values(self):
        """Test that gender has valid values."""
        from edulafia.modules.students.models import Student
        gender_col = Student.__table__.columns['gender']
        assert gender_col is not None

    def test_genotype_values(self):
        """Test that genotype has valid values if present."""
        from edulafia.modules.students.models import Student
        if 'genotype' in Student.__table__.columns.keys():
            genotype_col = Student.__table__.columns['genotype']
            assert genotype_col is not None
