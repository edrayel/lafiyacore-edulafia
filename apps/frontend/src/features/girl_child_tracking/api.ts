import { apiClient } from '../../shared/api/client';

export interface GirlChildRecord {
  id: string;
  student_id: string;
  student_name: string;
  risk_level: string;
  attendance_rate: number;
  academic_performance: number;
  interventions: string[];
  notes?: string;
  last_reviewed: string;
}

export interface UpdateGirlChildPayload {
  risk_level: string;
  interventions: string[];
  notes?: string;
}

export async function getGirlChildRecords(): Promise<GirlChildRecord[]> {
  const { data } = await apiClient.get('/girl-child/records');
  return data;
}

export async function updateGirlChildRecord(
  id: string,
  payload: UpdateGirlChildPayload
): Promise<GirlChildRecord> {
  const { data } = await apiClient.put(`/girl-child/records/${id}`, payload);
  return data;
}
