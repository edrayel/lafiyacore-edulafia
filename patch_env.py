import os

file_path = 'apps/backend/alembic/env.py'
with open(file_path, 'r') as f:
    content = f.read()

content = content.replace(
    'from edulafia.database import Base\n\n# Import all models',
    'from edulafia.database import Base\nimport edulafia.main\n\n# Import all models'
)

with open(file_path, 'w') as f:
    f.write(content)

print("Patched env.py")
