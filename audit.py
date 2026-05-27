import re
import os

with open("IMPLEMENTATION_PLAN.md", "r") as f:
    lines = f.readlines()

current_phase = None

for line in lines:
    if line.startswith("## Phase"):
        current_phase = line.strip()
    elif "| `" in line and "apps/" in line:
        parts = [p.strip() for p in line.split("|")]
        for p in parts:
            if p.startswith("`apps/"):
                file_path = p.replace("`", "")
                if not os.path.exists(file_path):
                    print(f"MISSING: {current_phase} - {file_path}")
                else:
                    print(f"FOUND: {current_phase} - {file_path}")

