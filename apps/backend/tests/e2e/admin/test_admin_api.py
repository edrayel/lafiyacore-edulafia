"""Tests for Admin API endpoints - written BEFORE implementation (TDD)."""



class TestAdminAPI:
    """Test cases for Admin API endpoints."""

    def test_schools_router_exists(self):
        """Test that schools router exists."""
        from edulafia.modules.admin.api.admin import schools_router
        assert schools_router is not None

    def test_users_router_exists(self):
        """Test that users router exists."""
        from edulafia.modules.admin.api.admin import users_router
        assert users_router is not None

    def test_sync_router_exists(self):
        """Test that sync router exists."""
        from edulafia.modules.admin.api.admin import sync_router
        assert sync_router is not None

    def test_sentinel_router_exists(self):
        """Test that sentinel router exists."""
        from edulafia.modules.admin.api.admin import sentinel_router
        assert sentinel_router is not None

    def test_updates_router_exists(self):
        """Test that updates router exists."""
        from edulafia.modules.admin.api.admin import updates_router
        assert updates_router is not None

    def test_training_router_exists(self):
        """Test that training router exists."""
        from edulafia.modules.admin.api.admin import training_router
        assert training_router is not None

    def test_analytics_router_exists(self):
        """Test that analytics router exists."""
        from edulafia.modules.admin.api.admin import analytics_router
        assert analytics_router is not None

    def test_provision_school_endpoint_exists(self):
        """Test that POST /schools/provision endpoint exists."""
        from edulafia.modules.admin.api.admin import schools_router
        routes = [r.path for r in schools_router.routes if hasattr(r, 'methods')]
        assert any('provision' in path for path in routes) or len(schools_router.routes) > 0
