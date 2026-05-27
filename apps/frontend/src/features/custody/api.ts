import { apiClient } from '../../shared/api/client';

export interface CustodyOrder {
  id: string;
  student_id: string;
  student_name: string;
  custodial_parent: string;
  non_custodial_parent: string;
  court: string;
  order_date: string;
  status: string;
  notes?: string;
  created_at: string;
}

export interface CreateCustodyPayload {
  student_id: string;
  custodial_parent: string;
  non_custodial_parent: string;
  court: string;
  order_date: string;
  notes?: string;
}

export async function getCustodyOrders(params?: { student_id?: string }): Promise<CustodyOrder[]> {
  const { data } = await apiClient.get('/custody/orders', { params });
  return data;
}

export async function createCustodyOrder(payload: CreateCustodyPayload): Promise<CustodyOrder> {
  const { data } = await apiClient.post('/custody/orders', payload);
  return data;
}
