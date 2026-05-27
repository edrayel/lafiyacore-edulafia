import { apiClient } from '../../shared/api/client';

export interface AccreditationItem {
  id: string;
  category: string;
  requirement: string;
  status: string;
  evidence?: string;
  last_reviewed: string;
  notes?: string;
}

export interface UpdateAccreditationPayload {
  status: string;
  evidence?: string;
  notes?: string;
}

export async function getAccreditationItems(params?: {
  category?: string;
}): Promise<AccreditationItem[]> {
  const { data } = await apiClient.get('/accreditation/items', { params });
  return data;
}

export async function updateAccreditationItem(
  id: string,
  payload: UpdateAccreditationPayload
): Promise<AccreditationItem> {
  const { data } = await apiClient.put(`/accreditation/items/${id}`, payload);
  return data;
}
