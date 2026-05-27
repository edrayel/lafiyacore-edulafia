import { apiClient } from '../../shared/api/client';

export interface LeaveRequest {
  id: string;
  staff_id: string;
  staff_name: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: string;
  approved_by?: string;
  created_at: string;
}

export interface CreateLeavePayload {
  staff_id: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
}

export async function getLeaveRequests(params?: {
  status?: string;
  staff_id?: string;
}): Promise<LeaveRequest[]> {
  const { data } = await apiClient.get('/leave/requests', { params });
  return data;
}

export async function createLeaveRequest(payload: CreateLeavePayload): Promise<LeaveRequest> {
  const { data } = await apiClient.post('/leave/requests', payload);
  return data;
}

export async function approveLeave(id: string): Promise<void> {
  await apiClient.post(`/leave/requests/${id}/approve`);
}

export async function rejectLeave(id: string, reason?: string): Promise<void> {
  await apiClient.post(`/leave/requests/${id}/reject`, { reason });
}
