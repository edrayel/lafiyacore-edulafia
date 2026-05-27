import os
import re

file_path = 'apps/frontend/src/features/guardians/GuardianDetailPage.tsx'
with open(file_path, 'r') as f:
    content = f.read()

# 1. Update imports in api.ts to add getGuardianStudents
api_file = 'apps/frontend/src/features/guardians/api.ts'
with open(api_file, 'r') as f:
    api_content = f.read()

if 'export async function getGuardianStudents' not in api_content:
    api_content += """
export async function getGuardianStudents(guardianId: string) {
  const { data } = await apiClient.get(`/guardians/${guardianId}/students`);
  return data;
}
"""
    with open(api_file, 'w') as f:
        f.write(api_content)

# 2. Update GuardianDetailPage
old_import = "import { getGuardian, updateGuardian, archiveGuardian, unlinkFromStudent } from './api';"
new_import = "import { getGuardian, updateGuardian, archiveGuardian, unlinkFromStudent, getGuardianStudents } from './api';"
content = content.replace(old_import, new_import)

# Remove mock
mock_block = """const mockLinkedStudents = [
  { id: '1', name: 'John Doe', class: 'JSS 1', admissionNumber: 'ED-2023-001' },
  { id: '2', name: 'Jane Doe', class: 'SS 2', admissionNumber: 'ED-2021-042' },
];"""
content = content.replace(mock_block, "")

# Add query
old_query = """  const { data: guardian, isLoading } = useQuery({
    queryKey: ['guardian', guardianId],
    queryFn: () => getGuardian(guardianId),
  });"""

new_query = """  const { data: guardian, isLoading } = useQuery({
    queryKey: ['guardian', guardianId],
    queryFn: () => getGuardian(guardianId),
  });

  const { data: linkedStudents = [], isLoading: isLoadingStudents } = useQuery({
    queryKey: ['guardian_students', guardianId],
    queryFn: () => getGuardianStudents(guardianId),
  });"""
content = content.replace(old_query, new_query)

# Update map
content = content.replace("{mockLinkedStudents.map((student: any) => (", "{linkedStudents.map((student: any) => (")
content = content.replace("<TableCell>{student.name}</TableCell>", "<TableCell>{student.first_name} {student.last_name}</TableCell>")
content = content.replace("<TableCell>{student.class}</TableCell>", "<TableCell>{student.class_id || 'Unassigned'}</TableCell>")
content = content.replace("<TableCell>{student.admissionNumber}</TableCell>", "<TableCell>{student.admission_number}</TableCell>")

with open(file_path, 'w') as f:
    f.write(content)
print("Patched guardian UI")
