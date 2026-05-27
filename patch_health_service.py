import os

file_path = 'apps/backend/src/edulafia/modules/health/service.py'
with open(file_path, 'r') as f:
    content = f.read()

old_block = """    async def _check_repeat_visitor(
        self,
        school_id: UUID,
        student_id: UUID,
        complaint_codes: list[str],
    ) -> bool:
        \"\"\"Check if student is a repeat visitor (>3 visits for same complaint this term).\"\"\"
        term_start = date.today() - __import__("datetime").timedelta(days=90)
        term_end = date.today()

        try:
            from sqlalchemy import text"""

new_block = """    async def _check_repeat_visitor(
        self,
        school_id: UUID,
        student_id: UUID,
        complaint_codes: list[str],
    ) -> bool:
        \"\"\"Check if student is a repeat visitor (>3 visits for same complaint this term).\"\"\"
        term_end = date.today()
        term_start = date.today() - __import__("datetime").timedelta(days=90)
        
        try:
            from sqlalchemy import text

            from edulafia.database import AsyncSessionLocal

            async with AsyncSessionLocal() as db_session:
                # Try to get actual academic year term dates if they exist
                term_stmt = text(\"\"\"
                    SELECT start_date FROM academic_years 
                    WHERE school_id = :school_id AND is_current = true LIMIT 1
                \"\"\")
                term_res = await db_session.execute(term_stmt, {"school_id": str(school_id)})
                actual_start = term_res.scalar()
                if actual_start:
                    term_start = actual_start"""

content = content.replace(old_block, new_block)
with open(file_path, 'w') as f:
    f.write(content)

print("Patched health/service.py")
