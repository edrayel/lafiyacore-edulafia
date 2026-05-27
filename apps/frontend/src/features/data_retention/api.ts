import { apiClient } from '../../shared/api/client';

export interface RetentionPolicy {
  id: string;
  data_type: string;
  retention_years: number;
  auto_delete: boolean;
  last_reviewed: string;
  created_at: string;
}

export interface CreateRetentionPolicyPayload {
  data_type: string;
  retention_years: number;
  auto_delete: boolean;
}

export async function getRetentionPolicies(): Promise<RetentionPolicy[]> {
  const { data } = await apiClient.get('/data-retention/policies');
  return data;
}

export async function createRetentionPolicy(
  payload: CreateRetentionPolicyPayload
): Promise<RetentionPolicy> {
  const { data } = await apiClient.post('/data-retention/policies', payload);
  return data;
}
