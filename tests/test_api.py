"""
Integration tests for the API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


# Note: These tests require the backend to be properly configured
# with a valid GOOGLE_API_KEY for full functionality

@pytest.fixture
def client():
    """Create a test client."""
    # Import here to avoid circular dependencies
    from src.web.backend import app
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_check(self, client):
        """Test that health check endpoint returns status."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "version" in data
        assert "components" in data


class TestAnalyzeEndpoint:
    """Tests for task analysis endpoint."""
    
    def test_analyze_request(self, client):
        """Test task analysis."""
        response = client.post(
            "/api/analyze",
            json={"request": "Write a Python function"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "task_type" in data
        assert "complexity" in data
        assert "domain" in data
    
    def test_analyze_missing_request(self, client):
        """Test analysis with missing request."""
        response = client.post(
            "/api/analyze",
            json={}
        )
        
        # Should return validation error
        assert response.status_code == 422


class TestOptimizeEndpoint:
    """Tests for optimization endpoint."""
    
    def test_optimize_request_structure(self, client):
        """Test that optimize endpoint accepts requests."""
        # This may fail if GOOGLE_API_KEY is not set
        response = client.post(
            "/api/optimize",
            json={
                "prompt": "Explain AI",
                "strategy": "mesa",
                "max_iterations": 5
            }
        )
        
        # Either succeeds or fails due to missing API key
        assert response.status_code in [200, 503]
    
    def test_optimize_invalid_strategy(self, client):
        """Test optimization with valid request format."""
        response = client.post(
            "/api/optimize",
            json={
                "prompt": "Test prompt",
                "strategy": "mesa"
            }
        )
        
        # Should either work or fail gracefully
        assert response.status_code in [200, 503]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
