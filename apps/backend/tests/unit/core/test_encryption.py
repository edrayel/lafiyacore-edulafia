import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from edulafia.core.encryption import EncryptedString, EncryptedJSON

Base = declarative_base()

class EncryptedModel(Base):
    __tablename__ = 'encrypted_models'
    id = Column(Integer, primary_key=True)
    secret_data = Column(EncryptedString)
    secret_json = Column(EncryptedJSON)

@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_encrypted_string_encrypts_and_decrypts(session, engine):
    """Test that EncryptedString encrypts data in DB and decrypts when loaded."""
    # 1. Insert data
    model = EncryptedModel(secret_data="my_super_secret_string")
    session.add(model)
    session.commit()
    
    # 2. Verify it is encrypted in the raw database
    raw_conn = engine.raw_connection()
    cursor = raw_conn.cursor()
    cursor.execute("SELECT secret_data FROM encrypted_models WHERE id=?", (model.id,))
    raw_data = cursor.fetchone()[0]
    
    assert raw_data != "my_super_secret_string"
    assert isinstance(raw_data, str)
    assert len(raw_data) > len("my_super_secret_string")
    
    # 3. Verify it is decrypted when accessed through SQLAlchemy
    loaded_model = session.query(EncryptedModel).filter_by(id=model.id).first()
    assert loaded_model.secret_data == "my_super_secret_string"

def test_encrypted_json_encrypts_and_decrypts(session, engine):
    """Test that EncryptedJSON encrypts data in DB and decrypts when loaded."""
    test_json = {"key": "value", "list": [1, 2, 3]}
    model = EncryptedModel(secret_json=test_json)
    session.add(model)
    session.commit()
    
    raw_conn = engine.raw_connection()
    cursor = raw_conn.cursor()
    cursor.execute("SELECT secret_json FROM encrypted_models WHERE id=?", (model.id,))
    raw_data = cursor.fetchone()[0]
    
    assert raw_data != str(test_json)
    assert "key" not in raw_data
    assert "value" not in raw_data
    
    loaded_model = session.query(EncryptedModel).filter_by(id=model.id).first()
    assert loaded_model.secret_json == test_json

def test_encrypted_string_handles_none(session):
    """Test that None values are handled gracefully."""
    model = EncryptedModel(secret_data=None)
    session.add(model)
    session.commit()
    
    loaded_model = session.query(EncryptedModel).filter_by(id=model.id).first()
    assert loaded_model.secret_data is None
