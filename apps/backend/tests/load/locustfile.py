from locust import HttpUser, task, between, events
import json
import uuid
import hmac
import hashlib

class EduLafiaUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Executed when a simulated user starts."""
        self.login()
        self.school_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

    def login(self):
        """Simulate user login."""
        response = self.client.post("/api/v1/auth/login", json={
            "email": "admin@edulafia.com",
            "password": "Admin123!"
        })
        if response.status_code == 200:
            # Token is set via httpOnly cookie, locust's session handles cookies automatically
            pass
        else:
            print(f"Login failed: {response.status_code} - {response.text}")

    @task(3)
    def view_school_dashboard(self):
        """Simulate a user fetching the school dashboard."""
        self.client.get(f"/api/v1/intelligence/school/{self.school_id}/dashboard")

    @task(1)
    def generate_report(self):
        """Simulate a user generating a report."""
        self.client.post("/api/v1/intelligence/reports/generate", json={
            "report_type": "school",
            "parameters": {"school_id": self.school_id},
            "format": "pdf"
        })

    @task(2)
    def view_sentinel_dashboard(self):
        """Simulate a user fetching the sentinel health dashboard."""
        self.client.get("/api/v1/intelligence/sentinel/dashboard")


class WebhookSimulator(HttpUser):
    """Simulate bursts of webhooks from payment gateways."""
    wait_time = between(0.1, 0.5)  # Faster rate for webhooks

    @task
    def paystack_webhook(self):
        """Simulate a Paystack webhook event."""
        payload = {
            "event": "charge.success",
            "data": {
                "reference": f"REF-{uuid.uuid4()}",
                "amount": 500000
            }
        }
        
        # Mocking signature (in reality, requires the correct secret, but we can simulate the hit)
        # We will hit the endpoint; if it returns 404/401, that's fine for load testing the web server layer
        # as it will still process the request and hit the DB to check reference.
        secret = b"test_secret"
        payload_bytes = json.dumps(payload).encode('utf-8')
        signature = hmac.new(secret, payload_bytes, hashlib.sha512).hexdigest()
        
        self.client.post(
            "/api/v1/webhooks/paystack",
            json=payload,
            headers={"x-paystack-signature": signature}
        )
