import os
import re

files = [
    "attendance/schemas.py",
    "payroll/schemas.py",
    "data_retention/schemas.py",
    "ministry_reporting/schemas.py",
    "library/schemas.py",
    "inspection_tracking/schemas.py",
    "leave_management/schemas.py",
    "inventory/schemas.py",
    "smc_reporting/schemas.py",
    "waec_bulk/schemas.py",
    "custody/schemas.py",
    "accreditation/schemas.py",
    "bus_tracking/schemas.py"
]

base_path = "apps/backend/src/edulafia/modules/"

for file_name in files:
    full_path = os.path.join(base_path, file_name)
    with open(full_path, "r") as f:
        content = f.read()

    # Regex to match a newline, optional spaces, and 'pass' at the end of a class docstring
    # Actually, we can just replace "\n    pass\n" with "\n"
    # But wait, it's safer to just replace '    pass\n'
    
    # We want to remove the '    pass' and any preceding empty lines.
    # Pattern: \n\n    pass\n -> \n
    new_content = re.sub(r'\n\s*\n\s*pass\n', '\n', content)
    
    # Also handle the case where it might be just \n    pass\n
    new_content = re.sub(r'\n\s*pass\n', '\n', new_content)
    
    with open(full_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed {file_name}")
