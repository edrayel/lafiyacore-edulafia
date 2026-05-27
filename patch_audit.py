import os

file_path = 'apps/backend/src/edulafia/core/audit.py'
with open(file_path, 'r') as f:
    content = f.read()

old_block = """        # Simple logging for now
        # A more robust system would save to a database table or external audit service
        logger.info(
            "Audit Log: %s %s - Status: %s - Time: %.4fs",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )"""

new_block = """        # More robust logging that captures user info from request state if available
        user_id = "anonymous"
        if hasattr(request.state, "user") and request.state.user:
            user_id = request.state.user.get("id", "anonymous")
            
        logger.info(
            "Audit Log: [User: %s] %s %s - Status: %s - Time: %.4fs",
            user_id,
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )"""

content = content.replace(old_block, new_block)
with open(file_path, 'w') as f:
    f.write(content)

print("Patched core/audit.py")
