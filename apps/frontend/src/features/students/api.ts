import { apiClient } from '../../shared/api/client';
import type { Student, ListResponse } from '../../shared/types';

export interface StudentsQueryParams {
  page?: number;
  per_page?: number;
  search?: string;
  class_id?: string;
  status?: string;
  gender?: string;
  guardian_id?: string;
}

export interface CreateStudentPayload {
  first_name: string;
  last_name: string;
  middle_name?: string;
  date_of_birth: string;
  gender: string;
  admission_number: string;
  admission_date: string;
  class_id?: string;
  nationality?: string;
  state_of_origin?: string;
  lga_of_origin?: string;
  nin?: string;
  address?: string;
  medical_conditions?: string;
  special_needs?: string;
}

export interface UpdateStudentPayload extends Partial<CreateStudentPayload> {
  status?: string;
}

export async function getStudents(params?: StudentsQueryParams): Promise<ListResponse<Student>> {
  const { data } = await apiClient.get('/students', { params });
  return data.data || data;
}

export async function getStudent(id: string): Promise<Student> {
  const { data } = await apiClient.get(`/students/${id}`);
  return data;
}

export async function createStudent(payload: CreateStudentPayload): Promise<Student> {
  const { data } = await apiClient.post('/students', payload);
  return data;
}

export async function updateStudent(id: string, payload: UpdateStudentPayload): Promise<Student> {
  const { data } = await apiClient.patch(`/students/${id}`, payload);
  return data;
}

export async function archiveStudent(id: string): Promise<Student> {
  const { data } = await apiClient.delete(`/students/${id}`);
  return data;
}

export async function generateAdmissionNumber(): Promise<{ admission_number: string }> {
  const { data } = await apiClient.post('/students/generate-admission-number');
  return data;
}

export const getStudentDocuments = async (studentId: string): Promise<Array<{ id: string; document_type: string; title: string; filename: string; uploaded_at: string }>> => {
  const { data } = await apiClient.get(`/students/${studentId}/documents`);
  return data.data; // APIResponse structure returns {"status": "success", "data": [...]}
};

export const uploadStudentDocument = async (
  studentId: string,
  formData: FormData
): Promise<{ id: string; filename: string; uploaded_at: string }> => {
  const { data } = await apiClient.post(`/students/${studentId}/documents`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return data.data;
};

export const deleteStudentDocument = async (
  studentId: string,
  documentId: string
): Promise<void> => {
  await apiClient.delete(`/students/${studentId}/documents/${documentId}`);
};

export const batchImportStudents = async (formData: FormData): Promise<{ imported: number; failed: number; errors: string[] }> => {
  const { data } = await apiClient.post('/students/batch-import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return data;
};

export const exportStudentData = async (studentId: string): Promise<Record<string, unknown>> => {
  const { data } = await apiClient.get(`/students/${studentId}/export`);
  return data.data;
};
