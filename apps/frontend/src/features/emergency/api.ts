import { apiClient } from '../../shared/api/client';

export interface Emergency {
  id: string;
  title: string;
  description: string;
  status: string;
  activated_at: string;
  deactivated_at: string | null;
  activated_by: string;
}

export interface ActivateEmergencyPayload {
  title: string;
  description: string;
}

export async function getEmergencies(): Promise<Emergency[]> {
  const { data } = await apiClient.get('/emergency');
  return data;
}

export async function getActiveEmergency(): Promise<Emergency | null> {
  const { data } = await apiClient.get('/emergency/active');
  return data;
}

export async function activateEmergency(payload: ActivateEmergencyPayload): Promise<Emergency> {
  const { data } = await apiClient.post('/emergency/activate', payload);
  return data;
}

export async function deactivateEmergency(id: string): Promise<void> {
  await apiClient.post(`/emergency/${id}/deactivate`);
}
