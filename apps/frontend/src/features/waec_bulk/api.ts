import { apiClient } from '../../shared/api/client';

export interface WAECBulkRegistration {
  id: string;
  exam_year: number;
  class_id: string;
  class_name: string;
  total_registered: number;
  total_students: number;
  status: string;
  created_at: string;
}

export async function getWAECBulkRegistrations(params?: {
  year?: number;
}): Promise<WAECBulkRegistration[]> {
  const { data } = await apiClient.get('/waec-bulk/registrations', { params });
  return data;
}

export async function createWAECBulkRegistration(payload: {
  exam_year: number;
  class_id: string;
}): Promise<WAECBulkRegistration> {
  const { data } = await apiClient.post('/waec-bulk/registrations', payload);
  return data;
}

export async function submitWAECBulkRegistration(id: string): Promise<void> {
  await apiClient.post(`/waec-bulk/registrations/${id}/submit`);
}
