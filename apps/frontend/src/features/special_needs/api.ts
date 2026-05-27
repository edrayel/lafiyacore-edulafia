import { apiClient } from '../../shared/api/client';

export interface IEP {
  id: string;
  student_id: string;
  student_name: string;
  disability_type: string;
  status: string;
  goals: string;
  accommodations: string;
  review_date: string;
  created_at: string;
}

export interface CreateIEPPayload {
  student_id: string;
  disability_type: string;
  goals: string;
  accommodations: string;
  review_date: string;
}

export async function getIEPs(params?: { status?: string }): Promise<IEP[]> {
  const { data } = await apiClient.get('/special-needs/ieps', { params });
  return data;
}

export async function getIEP(id: string): Promise<IEP> {
  const { data } = await apiClient.get(`/special-needs/ieps/${id}`);
  return data;
}

export async function createIEP(payload: CreateIEPPayload): Promise<IEP> {
  const { data } = await apiClient.post('/special-needs/ieps', payload);
  return data;
}

export async function updateIEP(id: string, payload: Partial<CreateIEPPayload>): Promise<IEP> {
  const { data } = await apiClient.put(`/special-needs/ieps/${id}`, payload);
  return data;
}
