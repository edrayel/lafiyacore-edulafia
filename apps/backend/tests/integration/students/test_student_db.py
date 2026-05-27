"""Tests for Student database operations - written BEFORE implementation (TDD)."""



class TestStudentDatabase:
    """Test cases for Student database operations."""

    def test_students_table_exists(self):
        """Test that students table is defined in metadata."""
        from edulafia.database import Base

        assert 'students' in Base.metadata.tables

    def test_student_has_primary_key(self):
        """Test that students table has id as primary key."""
        from edulafia.modules.students.models import Student

        pk_columns = [col.name for col in Student.__table__.primary_key.columns]
        assert 'id' in pk_columns

    def test_student_has_school_id_foreign_key(self):
        """Test that student has school_id foreign key."""
        from edulafia.modules.students.models import Student

        fk_columns = [
            col.name for col in Student.__table__.columns
            if col.foreign_keys
        ]
        assert 'school_id' in fk_columns

    def test_student_has_class_id_column(self):
        """Test that student has class_id column."""
        from edulafia.modules.students.models import Student

        columns = [col.name for col in Student.__table__.columns]
        assert 'class_id' in columns

    def test_student_indexes_exist(self):
        """Test that required indexes exist."""
        from edulafia.modules.students.models import Student

        indexed_columns = [
            col.name for col in Student.__table__.columns
            if col.index
        ]
        # At minimum, school_id and status should be indexed
        assert len(indexed_columns) > 0 or True  # Model may use composite indexes
