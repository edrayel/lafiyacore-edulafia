import { apiClient } from '../../shared/api/client';

export interface MinistryReport {
  id: string;
  report_type: string;
  period: string;
  submitted: boolean;
  submitted_at: string | null;
  data: Record<string, unknown>;
  created_at: string;
}

export async function getMinistryReports(params?: { type?: string }): Promise<MinistryReport[]> {
  const { data } = await apiClient.get('/ministry/reports', { params });
  return data;
}

export async function generateReport(payload: {
  report_type: string;
  period: string;
}): Promise<MinistryReport> {
  const { data } = await apiClient.post('/ministry/reports/generate', payload);
  return data;
}

export async function submitReport(id: string): Promise<void> {
  await apiClient.post(`/ministry/reports/${id}/submit`);
}
