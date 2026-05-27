import { apiClient } from '../../shared/api/client';

export interface Inspection {
  id: string;
  inspection_date: string;
  inspector_name: string;
  status: string;
  compliance_score: number;
  findings: string;
  recommendations: string;
  created_at: string;
}

export interface CreateInspectionPayload {
  inspection_date: string;
  inspector_name: string;
  compliance_score: number;
  findings: string;
  recommendations: string;
}

export async function getInspections(): Promise<Inspection[]> {
  const { data } = await apiClient.get('/inspections');
  return data;
}

export async function createInspection(payload: CreateInspectionPayload): Promise<Inspection> {
  const { data } = await apiClient.post('/inspections', payload);
  return data;
}
