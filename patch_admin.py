import os

file_path = 'apps/backend/src/edulafia/modules/admin/service.py'
with open(file_path, 'r') as f:
    content = f.read()

old_block = """        # This would query actual historical data
        # For now, return analysis based on threshold config
        is_percentage = "%" in str(threshold.value)
        value_num = float(str(threshold.value).replace("%", ""))
        
        simulated_value = value_num * 1.1 if is_percentage else value_num + 5"""

new_block = """        # Query actual historical data if possible
        # We will attempt to get historical data via direct DB queries if applicable
        # This implementation uses the current session to run an aggregation
        from sqlalchemy import select, func, text
        
        is_percentage = "%" in str(threshold.value)
        value_num = float(str(threshold.value).replace("%", ""))
        simulated_value = value_num * 1.1 if is_percentage else value_num + 5
        
        try:
            if threshold.metric == "attendance":
                stmt = text("SELECT COUNT(*) FROM attendance_records WHERE status = 'absent' AND school_id = :school_id")
                result = await self.db.execute(stmt, {"school_id": str(school_id)})
                simulated_value = float(result.scalar() or 0)
            elif threshold.metric == "health":
                stmt = text("SELECT COUNT(*) FROM sick_bay_visits WHERE school_id = :school_id")
                result = await self.db.execute(stmt, {"school_id": str(school_id)})
                simulated_value = float(result.scalar() or 0)
        except Exception:
            # Fallback to simulated if tables don't exist or query fails
            pass"""

content = content.replace(old_block, new_block)
with open(file_path, 'w') as f:
    f.write(content)

print("Patched admin/service.py")
