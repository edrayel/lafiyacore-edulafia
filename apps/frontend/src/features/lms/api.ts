import { apiClient } from '../../shared/api/client';

export interface Assignment {
  id: string;
  course_id: string;
  title: string;
  description?: string;
  due_date?: string;
  max_score?: number;
  file_path?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateAssignmentPayload {
  title: string;
  description?: string;
  course_id: string;
  due_date: string;
  max_score?: number;
  file_path?: string;
}

export type UpdateAssignmentPayload = Partial<CreateAssignmentPayload>;

export async function getAssignments(params?: {
  course_id?: string;
  class_id?: string;
}): Promise<Assignment[]> {
  const { data } = await apiClient.get('/lms/assignments', { params });
  return data;
}

export async function getAssignment(id: string): Promise<Assignment> {
  const { data } = await apiClient.get(`/lms/assignments/${id}`);
  return data;
}

export async function createAssignment(payload: CreateAssignmentPayload): Promise<Assignment> {
  const { data } = await apiClient.post('/lms/assignments', payload);
  return data;
}

export async function updateAssignment(
  id: string,
  payload: UpdateAssignmentPayload
): Promise<Assignment> {
  const { data } = await apiClient.patch(`/lms/assignments/${id}`, payload);
  return data;
}

export async function deleteAssignment(id: string): Promise<void> {
  await apiClient.delete(`/lms/assignments/${id}`);
}

export async function uploadAssignmentFile(
  file: File
): Promise<{ file_path: string; filename: string }> {
  const formData = new FormData();
  formData.append('file', file);

  const { data } = await apiClient.post('/lms/uploads/assignments', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return data;
}
