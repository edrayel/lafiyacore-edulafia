import os

file_path = 'apps/backend/src/edulafia/modules/health/service.py'
with open(file_path, 'r') as f:
    content = f.read()

old_code = """        # Simple check for repeat visitors (more than 3 visits in a term)
        # Assuming a term is roughly 90 days
        term_start = date.today() - __import__("datetime").timedelta(days=90)
        visits = await self.repository.list_sick_bay_visits(
            school_id=school_id,
            student_id=student_id,
            start_date=term_start
        )
"""

new_code = """        # Check for repeat visitors dynamically by querying the current active term
        # Fallback to 90 days if no active term is found for the school
        from edulafia.modules.academics.models import Term
        from sqlalchemy import select
        
        term_stmt = select(Term).where(
            Term.school_id == school_id,
            Term.is_active == True
        )
        term_result = await self.repository.db.execute(term_stmt)
        active_term = term_result.scalar_one_or_none()
        
        term_start = active_term.start_date if active_term else (date.today() - __import__("datetime").timedelta(days=90))
        
        visits = await self.repository.list_sick_bay_visits(
            school_id=school_id,
            student_id=student_id,
            start_date=term_start
        )
"""

content = content.replace(old_code, new_code)

with open(file_path, 'w') as f:
    f.write(content)

print("Patched health service")
