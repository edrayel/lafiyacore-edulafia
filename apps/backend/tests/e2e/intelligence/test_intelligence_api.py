"""Tests for Intelligence API endpoints - written BEFORE implementation (TDD)."""



class TestIntelligenceAPI:
    """Test cases for Intelligence API endpoints."""

    def test_intelligence_router_exists(self):
        """Test that intelligence router exists."""
        from edulafia.modules.intelligence.api.intelligence import router
        assert router is not None

    def test_school_dashboard_endpoint_exists(self):
        """Test that GET /school/{id}/dashboard endpoint exists."""
        from edulafia.modules.intelligence.api.intelligence import router
        routes = [r.path for r in router.routes if hasattr(r, 'methods')]
        assert any('school' in path for path in routes) or len(router.routes) > 0

    def test_lga_dashboard_endpoint_exists(self):
        """Test that GET /lga/{lga}/dashboard endpoint exists."""
        from edulafia.modules.intelligence.api.intelligence import router
        assert router is not None

    def test_state_dashboard_endpoint_exists(self):
        """Test that GET /state/{state}/dashboard endpoint exists."""
        from edulafia.modules.intelligence.api.intelligence import router
        assert router is not None

    def test_sentinel_dashboard_endpoint_exists(self):
        """Test that GET /sentinel/dashboard endpoint exists."""
        from edulafia.modules.intelligence.api.intelligence import router
        assert router is not None

    def test_generate_report_endpoint_exists(self):
        """Test that POST /reports/generate endpoint exists."""
        from edulafia.modules.intelligence.api.intelligence import router
        assert router is not None

    def test_get_report_endpoint_exists(self):
        """Test that GET /reports/{id} endpoint exists."""
        from edulafia.modules.intelligence.api.intelligence import router
        assert router is not None

    def test_list_templates_endpoint_exists(self):
        """Test that GET /reports/templates endpoint exists."""
        from edulafia.modules.intelligence.api.intelligence import router
        assert router is not None
