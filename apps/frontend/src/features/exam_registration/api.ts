import { apiClient } from '../../shared/api/client';

export interface ExamRegistration {
  id: string;
  student_id: string;
  student_name: string;
  exam_type: string;
  exam_year: number;
  subjects: string[];
  status: string;
  registration_number?: string;
  created_at: string;
}

export interface CreateExamRegPayload {
  student_id: string;
  exam_type: string;
  exam_year: number;
  subjects: string[];
}

export async function getExamRegistrations(params?: {
  exam_type?: string;
  year?: number;
}): Promise<ExamRegistration[]> {
  const { data } = await apiClient.get('/exam-registrations', { params });
  return data;
}

export async function createExamRegistration(
  payload: CreateExamRegPayload
): Promise<ExamRegistration> {
  const { data } = await apiClient.post('/exam-registrations', payload);
  return data;
}

export async function cancelExamRegistration(id: string): Promise<void> {
  await apiClient.post(`/exam-registrations/${id}/cancel`);
}
