import { apiClient } from '../../shared/api/client';

export interface KPIResponse {
  code: string;
  name: string;
  value: number;
  unit: string;
  trend: string | null;
  status: string;
}

export interface AlertResponse {
  id: string;
  alert_type: string;
  title: string;
  message: string;
  severity: string;
  status: string;
  created_at: string;
}

export interface TrendResponse {
  kpi_code: string;
  kpi_name: string;
  data: Array<{
    date: string;
    value: number;
  }>;
}

export interface QuickStatsResponse {
  total_students: number;
  total_teachers: number;
  total_classes: number;
  active_alerts: number;
}

export interface SchoolDashboardResponse {
  kpis: KPIResponse[];
  alerts: AlertResponse[];
  trends: TrendResponse[];
  quick_stats: QuickStatsResponse;
  date: string;
  last_updated: string;
  cache_expires_at: string;
}

export interface DashboardFilters {
  date?: string;
  term_id?: string;
}

export async function getSchoolDashboard(
  schoolId: string,
  filters?: DashboardFilters
): Promise<SchoolDashboardResponse> {
  const { data } = await apiClient.get(`/intelligence/school/${schoolId}/dashboard`, {
    params: filters,
  });
  return data;
}
