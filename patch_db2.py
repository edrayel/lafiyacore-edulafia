import os

file_path = 'apps/backend/src/edulafia/database.py'
with open(file_path, 'r') as f:
    content = f.read()

content = content.replace('@event.listens_for(AsyncSession, "do_orm_execute")', '@event.listens_for(Session, "do_orm_execute")')

if 'from sqlalchemy.orm import Session' not in content:
    content = content.replace('from sqlalchemy.orm import DeclarativeBase', 'from sqlalchemy.orm import DeclarativeBase, Session')

with open(file_path, 'w') as f:
    f.write(content)

print("Patched database.py")
