import { apiClient } from '../../shared/api/client';
import type { ListResponse } from '../../shared/types';

export interface Application {
  id: string;
  first_name: string;
  last_name: string;
  class_applied: string;
  status: string;
  exam_score: number;
  parent_name: string;
  parent_phone: string;
  created_at: string;
}

export interface CreateApplicationPayload {
  first_name: string;
  last_name: string;
  class_applied: string;
  parent_name: string;
  parent_phone: string;
  date_of_birth: string;
  gender: string;
}

export async function getApplications(params?: {
  status?: string;
  class_id?: string;
  page?: number;
  per_page?: number;
}): Promise<ListResponse<Application>> {
  const { data } = await apiClient.get('/admissions/applications', { params });
  return data;
}

export async function getApplication(id: string): Promise<Application> {
  const { data } = await apiClient.get(`/admissions/applications/${id}`);
  return data;
}

export async function createApplication(payload: CreateApplicationPayload): Promise<Application> {
  const { data } = await apiClient.post('/admissions/applications', payload);
  return data;
}

export async function approveApplication(id: string): Promise<void> {
  await apiClient.post(`/admissions/applications/${id}/approve`);
}

export async function rejectApplication(id: string, reason?: string): Promise<void> {
  await apiClient.post(`/admissions/applications/${id}/reject`, { reason });
}

export async function enrollApplication(id: string): Promise<void> {
  await apiClient.post(`/admissions/applications/${id}/enroll`);
}
