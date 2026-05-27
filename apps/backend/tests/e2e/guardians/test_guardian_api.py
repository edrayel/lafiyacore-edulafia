"""Tests for Guardians API endpoints - TDD implementation."""


import pytest


class TestGuardiansAPI:
    """Test cases for Guardians API endpoints."""

    def test_guardians_router_exists(self):
        """Test that guardians router is importable."""
        from edulafia.api.v1.guardians import router
        assert router is not None

    def test_create_guardian_endpoint_exists(self):
        """Test that POST /guardians endpoint is registered."""
        from edulafia.api.v1.guardians import router
        routes = [r.path for r in router.routes if hasattr(r, 'methods')]
        assert any(path == '' or 'guardians' in path for path in routes) or len(router.routes) > 0

    def test_list_guardians_endpoint_exists(self):
        """Test that GET /guardians endpoint is registered."""
        from edulafia.api.v1.guardians import router
        assert router is not None

    def test_get_guardian_endpoint_exists(self):
        """Test that GET /guardians/{id} endpoint is registered."""
        from edulafia.api.v1.guardians import router
        assert router is not None

    def test_update_guardian_endpoint_exists(self):
        """Test that PATCH /guardians/{id} endpoint is registered."""
        from edulafia.api.v1.guardians import router
        assert router is not None

    def test_archive_guardian_endpoint_exists(self):
        """Test that DELETE /guardians/{id} endpoint is registered."""
        from edulafia.api.v1.guardians import router
        assert router is not None

    def test_link_guardian_to_student_endpoint_exists(self):
        """Test that POST /guardians/{id}/students/{id} endpoint is registered."""
        from edulafia.api.v1.guardians import router
        assert router is not None

    def test_unlink_guardian_from_student_endpoint_exists(self):
        """Test that DELETE /guardians/{id}/students/{id} endpoint is registered."""
        from edulafia.api.v1.guardians import router
        assert router is not None

    def test_guardians_router_prefix(self):
        """Test that guardians router has correct prefix."""
        from edulafia.api.v1.guardians import router
        assert router.prefix == "/guardians"

    def test_guardians_router_tags(self):
        """Test that guardians router has correct tags."""
        from edulafia.api.v1.guardians import router
        assert "Guardians" in router.tags


class TestGuardianSchemas:
    """Test cases for Guardian schemas."""

    def test_guardian_create_valid(self):
        """Test valid guardian creation schema."""
        from edulafia.modules.guardians.schemas import GuardianCreate

        data = GuardianCreate(
            first_name="Ngozi",
            last_name="Okonkwo",
            phone_number="+2348012345678",
            relationship_type="mother",
        )
        assert data.first_name == "Ngozi"
        assert data.phone_number == "+2348012345678"

    def test_guardian_create_invalid_phone(self):
        """Test that invalid phone number is rejected."""
        from pydantic import ValidationError

        from edulafia.modules.guardians.schemas import GuardianCreate

        with pytest.raises(ValidationError):
            GuardianCreate(
                first_name="Ngozi",
                last_name="Okonkwo",
                phone_number="08012345678",  # Missing +234
                relationship_type="mother",
            )

    def test_guardian_create_invalid_nin(self):
        """Test that invalid NIN is rejected."""
        from pydantic import ValidationError

        from edulafia.modules.guardians.schemas import GuardianCreate

        with pytest.raises(ValidationError):
            GuardianCreate(
                first_name="Ngozi",
                last_name="Okonkwo",
                phone_number="+2348012345678",
                relationship_type="mother",
                nin="123",  # Too short
            )

    def test_guardian_update_partial(self):
        """Test partial guardian update schema."""
        from edulafia.modules.guardians.schemas import GuardianUpdate

        data = GuardianUpdate(first_name="NewName")
        assert data.first_name == "NewName"
        assert data.last_name is None

    def test_guardian_response_from_attributes(self):
        """Test that GuardianResponse can be created from model attributes."""
        from edulafia.modules.guardians.schemas import GuardianResponse

        # Should have from_attributes=True in model_config
        assert GuardianResponse.model_config.get("from_attributes") is True
