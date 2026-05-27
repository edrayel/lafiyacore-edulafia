import os

file_path = 'apps/backend/src/edulafia/modules/health/repository.py'
with open(file_path, 'r') as f:
    content = f.read()

old_block = """    async def get_coverage(self, school_id: UUID) -> dict[str, Any]:
        \"\"\"Get vaccination coverage statistics.\"\"\"
        # TODO: Implement actual calculation
        return {
            "total_students": 0,
            "vaccinated": 0,
            "coverage_percent": 0.0,
            "by_vaccine": {}
        }"""

new_block = """    async def get_coverage(self, school_id: UUID) -> dict[str, Any]:
        \"\"\"Get vaccination coverage statistics.\"\"\"
        from sqlalchemy import select, func, text
        
        # Calculate total students in the school
        total_stmt = text("SELECT COUNT(*) FROM students WHERE school_id = :school_id AND status = 'active'")
        total_res = await self.session.execute(total_stmt, {"school_id": str(school_id)})
        total_students = int(total_res.scalar() or 0)
        
        if total_students == 0:
            return {"total_students": 0, "vaccinated": 0, "coverage_percent": 0.0, "by_vaccine": {}}
            
        # Calculate distinct students with at least one vaccination
        vac_stmt = text(\"\"\"
            SELECT COUNT(DISTINCT student_id) FROM vaccination_records
            WHERE school_id = :school_id AND status = 'completed'
        \"\"\")
        vac_res = await self.session.execute(vac_stmt, {"school_id": str(school_id)})
        vaccinated = int(vac_res.scalar() or 0)
        
        coverage_percent = round((vaccinated / total_students) * 100, 2)
        
        # Breakdown by vaccine name
        by_vaccine = {}
        breakdown_stmt = text(\"\"\"
            SELECT vaccine_name, COUNT(*) as count 
            FROM vaccination_records
            WHERE school_id = :school_id AND status = 'completed'
            GROUP BY vaccine_name
        \"\"\")
        bd_res = await self.session.execute(breakdown_stmt, {"school_id": str(school_id)})
        for row in bd_res:
            by_vaccine[row.vaccine_name] = row.count
            
        return {
            "total_students": total_students,
            "vaccinated": vaccinated,
            "coverage_percent": coverage_percent,
            "by_vaccine": by_vaccine
        }"""

content = content.replace(old_block, new_block)
with open(file_path, 'w') as f:
    f.write(content)

print("Patched health/repository.py")
