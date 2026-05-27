import { apiClient } from '../../shared/api/client';

export interface AlumniProfile {
  id: string;
  student_id: string;
  graduation_year: number;
  current_occupation?: string;
  university?: string;
  linkedin_url?: string;
  contact_email?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateAlumniProfilePayload {
  student_id: string;
  graduation_year: number;
  current_occupation?: string;
  university?: string;
  linkedin_url?: string;
  contact_email?: string;
}

export async function getAlumniProfiles(): Promise<AlumniProfile[]> {
  const { data } = await apiClient.get('/alumni');
  return data;
}

export async function createAlumniProfile(
  payload: CreateAlumniProfilePayload
): Promise<AlumniProfile> {
  const { data } = await apiClient.post('/alumni', payload);
  return data;
}
