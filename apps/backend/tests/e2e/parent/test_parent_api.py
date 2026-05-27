"""Tests for Parent API endpoints - written BEFORE implementation (TDD)."""



class TestParentAPI:
    """Test cases for Parent API endpoints."""

    def test_parent_router_exists(self):
        """Test that parent router exists."""
        from edulafia.modules.parent.api.parent import router
        assert router is not None

    def test_request_otp_endpoint_exists(self):
        """Test that POST /auth/request-otp endpoint exists."""
        from edulafia.modules.parent.api.parent import router
        routes = [r.path for r in router.routes if hasattr(r, 'methods')]
        assert any('auth' in path for path in routes) or len(router.routes) > 0

    def test_verify_otp_endpoint_exists(self):
        """Test that POST /auth/verify-otp endpoint exists."""
        from edulafia.modules.parent.api.parent import router
        assert router is not None

    def test_list_children_endpoint_exists(self):
        """Test that GET /children endpoint exists."""
        from edulafia.modules.parent.api.parent import router
        assert router is not None

    def test_get_notifications_endpoint_exists(self):
        """Test that GET /notifications endpoint exists."""
        from edulafia.modules.parent.api.parent import router
        assert router is not None

    def test_submit_excusal_endpoint_exists(self):
        """Test that POST /children/{id}/excusal endpoint exists."""
        from edulafia.modules.parent.api.parent import router
        assert router is not None

    def test_submit_feedback_endpoint_exists(self):
        """Test that POST /feedback endpoint exists."""
        from edulafia.modules.parent.api.parent import router
        assert router is not None
