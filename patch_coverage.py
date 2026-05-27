import os

file_path = 'apps/backend/src/edulafia/modules/health/repository.py'
with open(file_path, 'r') as f:
    content = f.read()

old_block = """    async def get_coverage(
        self,
        school_id: UUID,
        vaccine_name: str | None = None,
    ) -> dict:
        \"\"\"Get vaccination coverage statistics.\"\"\"
        # This would calculate coverage percentages
        # For now, return basic stats
        return {
            "total_students": 0,
            "vaccinated": 0,
            "coverage_percent": 0,
        }"""

new_block = """    async def get_coverage(
        self,
        school_id: UUID,
        vaccine_name: str | None = None,
    ) -> dict:
        \"\"\"Get vaccination coverage statistics.\"\"\"
        from sqlalchemy import text
        
        # Calculate total students
        total_stmt = text("SELECT COUNT(*) FROM students WHERE school_id = :school_id AND status = 'active'")
        total_res = await self.db.execute(total_stmt, {"school_id": str(school_id)})
        total_students = int(total_res.scalar() or 0)
        
        if total_students == 0:
            return {"total_students": 0, "vaccinated": 0, "coverage_percent": 0}
            
        # Calculate vaccinated
        if vaccine_name:
            vac_stmt = text(\"\"\"
                SELECT COUNT(DISTINCT student_id) FROM vaccination_records
                WHERE school_id = :school_id AND vaccine_name = :vname AND status = 'completed'
            \"\"\")
            vac_res = await self.db.execute(vac_stmt, {"school_id": str(school_id), "vname": vaccine_name})
        else:
            vac_stmt = text(\"\"\"
                SELECT COUNT(DISTINCT student_id) FROM vaccination_records
                WHERE school_id = :school_id AND status = 'completed'
            \"\"\")
            vac_res = await self.db.execute(vac_stmt, {"school_id": str(school_id)})
            
        vaccinated = int(vac_res.scalar() or 0)
        
        return {
            "total_students": total_students,
            "vaccinated": vaccinated,
            "coverage_percent": round((vaccinated / total_students) * 100, 2)
        }"""

content = content.replace(old_block, new_block)
with open(file_path, 'w') as f:
    f.write(content)

print("Patched health/repository.py")
