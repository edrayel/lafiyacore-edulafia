import { apiClient } from '../../shared/api/client';

export interface BuildingProject {
  id: string;
  name: string;
  project_type: string;
  budget: number;
  spent: number;
  progress: number;
  status: string;
  start_date: string;
  estimated_completion: string;
  created_at: string;
}

export interface CreateProjectPayload {
  name: string;
  project_type: string;
  budget: number;
  start_date: string;
  estimated_completion: string;
}

export async function getProjects(params?: { status?: string }): Promise<BuildingProject[]> {
  const { data } = await apiClient.get('/building-projects', { params });
  return data;
}

export async function createProject(payload: CreateProjectPayload): Promise<BuildingProject> {
  const { data } = await apiClient.post('/building-projects', payload);
  return data;
}

export async function updateProgress(id: string, progress: number): Promise<void> {
  await apiClient.put(`/building-projects/${id}/progress`, { progress });
}
