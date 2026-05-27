import { apiClient } from '../../shared/api/client';
import type { Guardian, ListResponse } from '../../shared/types';

export interface GuardiansQueryParams {
  page?: number;
  per_page?: number;
  search?: string;
}

export interface CreateGuardianPayload {
  first_name: string;
  last_name: string;
  phone_number: string;
  relationship_type: string;
  email?: string;
  whatsapp_number?: string;
  occupation?: string;
  address?: string;
  nin?: string;
}

export interface UpdateGuardianPayload extends Partial<CreateGuardianPayload> {
  portal_access?: boolean;
}

export async function getGuardians(params?: GuardiansQueryParams): Promise<ListResponse<Guardian>> {
  const { data } = await apiClient.get('/guardians', { params });
  return data;
}

export async function getGuardian(id: string): Promise<Guardian> {
  const { data } = await apiClient.get(`/guardians/${id}`);
  return data;
}

export async function createGuardian(payload: CreateGuardianPayload): Promise<Guardian> {
  const { data } = await apiClient.post('/guardians', payload);
  return data;
}

export async function updateGuardian(
  id: string,
  payload: UpdateGuardianPayload
): Promise<Guardian> {
  const { data } = await apiClient.patch(`/guardians/${id}`, payload);
  return data;
}

export async function archiveGuardian(id: string): Promise<Guardian> {
  const { data } = await apiClient.delete(`/guardians/${id}`);
  return data;
}

export async function linkToStudent(
  guardianId: string,
  studentId: string,
  options?: { is_primary?: boolean; is_emergency_contact?: boolean; can_pickup?: boolean }
): Promise<void> {
  await apiClient.post(`/guardians/${guardianId}/students/${studentId}`, null, { params: options });
}

export async function unlinkFromStudent(guardianId: string, studentId: string): Promise<void> {
  await apiClient.delete(`/guardians/${guardianId}/students/${studentId}`);
}

export async function getStudentGuardians(studentId: string): Promise<Guardian[]> {
  const { data } = await apiClient.get(`/guardians/students/${studentId}`);
  return data;
}
