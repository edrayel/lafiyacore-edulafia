import os

file_path = 'apps/backend/src/edulafia/database.py'
with open(file_path, 'r') as f:
    content = f.read()

content = content.replace("from edulafia.models.base import SoftDeleteMixin", "")

old_hook = """            if entity is not None and issubclass(entity, SoftDeleteMixin):"""
new_hook = """            from edulafia.models.base import SoftDeleteMixin
            if entity is not None and isinstance(entity, type) and issubclass(entity, SoftDeleteMixin):"""

content = content.replace(old_hook, new_hook)

with open(file_path, 'w') as f:
    f.write(content)

print("Patched database.py")
