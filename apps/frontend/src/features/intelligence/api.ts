import { apiClient } from '../../shared/api/client';

export interface SchoolKPI {
  total_students: number;
  total_staff: number;
  attendance_rate: number;
  revenue_collected: number;
  revenue_expected: number;
  average_score: number;
  incidents_count: number;
}

export interface Alert {
  id: string;
  type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  created_at: string;
  resolved: boolean;
  resolved_at?: string;
}

export interface Report {
  id: string;
  type: string;
  title: string;
  status: 'pending' | 'generating' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
  download_url?: string;
}

export interface ReportGenerationPayload {
  type: string;
  title: string;
  date_range?: { start: string; end: string };
  filters?: Record<string, unknown>;
}

export async function verifyCertificate(certificateId: string): Promise<{ valid: boolean; student_name: string; certificate_type: string; issued_date: string }> {
  const { data } = await apiClient.get(`/intelligence/certificates/${certificateId}/verify`);
  return data;
}

export async function getSchoolDashboard(): Promise<{
  kpis: SchoolKPI;
  trends: { period: string; students: number; attendance: number; revenue: number }[];
}> {
  const { data } = await apiClient.get('/intelligence/dashboard');
  return data;
}

export async function getSentinelDashboard(): Promise<{
  alerts: Alert[];
  summary: { total: number; critical: number; high: number; medium: number; low: number };
}> {
  const { data } = await apiClient.get('/intelligence/sentinel');
  return data;
}

export async function generateReport(payload: ReportGenerationPayload): Promise<Report> {
  const { data } = await apiClient.post('/intelligence/reports', payload);
  return data;
}

export async function getReports(): Promise<Report[]> {
  const { data } = await apiClient.get('/intelligence/reports');
  return data;
}

export async function downloadReport(reportId: string): Promise<{ id: string; download_url: string; format: string }> {
  const { data } = await apiClient.get(`/intelligence/reports/${reportId}`);
  return data;
}

export async function syncEMISData(syncType: string): Promise<{ success: boolean; records_synced: number }> {
  const { data } = await apiClient.post('/intelligence/emis/sync', null, {
    params: { sync_type: syncType },
  });
  return data;
}

export async function getIllnessHeatmap(): Promise<Array<{ name: string; intensity: number; lat: number; lng: number; cases: number; pattern?: string }>> {
  const { data } = await apiClient.get('/intelligence/sentinel/heatmap');
  return data.data;
}

export interface DataPortalRequestPayload {
  dataset_type: string;
  purpose: string;
  date_range: { start: string; end: string };
}

export async function requestAnonymisedData(payload: DataPortalRequestPayload): Promise<{ request_id: string; status: string; estimated_completion: string }> {
  const { data } = await apiClient.post('/intelligence/data-portal/request', payload);
  return data;
}
