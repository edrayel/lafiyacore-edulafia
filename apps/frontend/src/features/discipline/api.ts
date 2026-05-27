import { apiClient } from '../../shared/api/client';

export interface DisciplineRecord {
  id: string;
  student_id: string;
  student_name: string;
  offense: string;
  action_taken: string;
  severity: string;
  reported_by: string;
  incident_date: string;
  notes?: string;
  created_at: string;
}

export interface CreateDisciplinePayload {
  student_id: string;
  offense: string;
  action_taken: string;
  severity: string;
  incident_date: string;
  notes?: string;
}

export async function getDisciplineRecords(params?: {
  student_id?: string;
}): Promise<DisciplineRecord[]> {
  const { data } = await apiClient.get('/discipline/records', { params });
  return data;
}

export async function createDisciplineRecord(
  payload: CreateDisciplinePayload
): Promise<DisciplineRecord> {
  const { data } = await apiClient.post('/discipline/records', payload);
  return data;
}
