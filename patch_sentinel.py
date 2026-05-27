import os

file_path = 'apps/backend/src/edulafia/modules/health/sentinel.py'
with open(file_path, 'r') as f:
    content = f.read()

old_block = """    async def trigger_alerts(self, events: list[SentinelEvent], school_id: UUID) -> dict[str, Any]:
        \"\"\"Trigger alerts for detected events.\"\"\"
        # In production, this would send notifications
        # For now, return the alert routing
        
        routing = {
            "critical": ["ministry_of_health", "lga_health_officer", "school_admin"],
            "high": ["school_admin", "school_nurse"],
            "medium": ["school_nurse"],
            "low": []
        }"""

new_block = """    async def trigger_alerts(self, events: list[SentinelEvent], school_id: UUID) -> dict[str, Any]:
        \"\"\"Trigger alerts for detected events.\"\"\"
        routing = {
            "critical": ["ministry_of_health", "lga_health_officer", "school_admin"],
            "high": ["school_admin", "school_nurse"],
            "medium": ["school_nurse"],
            "low": []
        }
        
        # Simulated external API call for notifications
        import logging
        logger = logging.getLogger(__name__)
        
        for event in events:
            targets = routing.get(event.severity, [])
            for target in targets:
                logger.info(f"SENTINEL ALERT [{event.severity.upper()}]: Notifying {target} about {event.event_type} at school {school_id}. Threshold: {event.threshold_exceeded}")"""

content = content.replace(old_block, new_block)
with open(file_path, 'w') as f:
    f.write(content)

print("Patched health/sentinel.py")
