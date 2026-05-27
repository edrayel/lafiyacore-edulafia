import { apiClient } from '../../shared/api/client';

export interface ProprietorDashboard {
  total_students: number;
  total_revenue: number;
  attendance_rate: number;
  active_alerts: number;
  total_staff: number;
  collection_rate: number;
}

export async function getProprietorDashboard(): Promise<ProprietorDashboard> {
  const { data } = await apiClient.get('/proprietor/dashboard');
  return data;
}

export async function getSchoolOverview(): Promise<{
  schools: { id: string; name: string; students: number; revenue: number }[];
}> {
  const { data } = await apiClient.get('/proprietor/schools');
  return data;
}
