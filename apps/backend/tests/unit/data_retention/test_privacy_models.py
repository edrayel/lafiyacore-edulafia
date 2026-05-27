import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from edulafia.modules.data_retention.models import ConsentRecord, DataSubjectRequest

def test_consent_record_model_has_required_fields():
    # Using SQLAlchemy inspection to verify columns
    columns = [c.name for c in ConsentRecord.__table__.columns]
    assert "id" in columns
    assert "student_id" in columns
    assert "guardian_id" in columns
    assert "consent_type" in columns
    assert "status" in columns
    assert "granted_at" in columns
    assert "ip_address" in columns

def test_data_subject_request_model_has_required_fields():
    columns = [c.name for c in DataSubjectRequest.__table__.columns]
    assert "id" in columns
    assert "requester_id" in columns
    assert "request_type" in columns
    assert "status" in columns
    assert "details" in columns
    assert "resolved_at" in columns
