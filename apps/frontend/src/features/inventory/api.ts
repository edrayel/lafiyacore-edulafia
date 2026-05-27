import { apiClient } from '../../shared/api/client';

export interface InventoryItem {
  id: string;
  name: string;
  category: string;
  quantity: number;
  location: string;
  condition: string;
  assigned_to?: string;
  created_at: string;
}

export interface CreateInventoryPayload {
  name: string;
  category: string;
  quantity: number;
  location: string;
  condition: string;
}

export async function getInventory(params?: { category?: string }): Promise<InventoryItem[]> {
  const { data } = await apiClient.get('/inventory', { params });
  return data;
}

export async function getInventoryItem(id: string): Promise<InventoryItem> {
  const { data } = await apiClient.get(`/inventory/${id}`);
  return data;
}

export async function createInventoryItem(payload: CreateInventoryPayload): Promise<InventoryItem> {
  const { data } = await apiClient.post('/inventory', payload);
  return data;
}

export async function updateInventoryItem(
  id: string,
  payload: Partial<CreateInventoryPayload>
): Promise<InventoryItem> {
  const { data } = await apiClient.put(`/inventory/${id}`, payload);
  return data;
}

export async function deleteInventoryItem(id: string): Promise<void> {
  await apiClient.delete(`/inventory/${id}`);
}
