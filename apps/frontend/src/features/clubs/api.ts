import { apiClient } from '../../shared/api/client';

export interface Club {
  id: string;
  name: string;
  category: string;
  advisor_name: string;
  member_count: number;
  meeting_day: string;
  is_active: boolean;
  created_at: string;
}

export interface CreateClubPayload {
  name: string;
  category: string;
  advisor_name: string;
  meeting_day: string;
}

export async function getClubs(params?: { category?: string }): Promise<Club[]> {
  const { data } = await apiClient.get('/clubs', { params });
  return data;
}

export async function createClub(payload: CreateClubPayload): Promise<Club> {
  const { data } = await apiClient.post('/clubs', payload);
  return data;
}
