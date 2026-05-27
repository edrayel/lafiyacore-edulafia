import { apiClient } from '../../shared/api/client';
import type { ListResponse } from '../../shared/types';

export interface SyncStatus {
  active_syncs: number;
  pending_megabytes: number;
  failed_syncs_24h: number;
}

export interface SyncHistoryItem {
  id: string;
  school_id: string;
  device_id: string;
  sync_type: string;
  status: string;
  records_synced: number;
  started_at: string;
}

export interface BackupRecord {
  backup_id: string;
  type: string;
  timestamp: string;
  size_mb: number;
  status: string;
}

export interface SystemUpdate {
  id: string;
  version: string;
  title: string;
  release_type: string;
  release_date: string;
  status: string;
  description: string;
}

export interface ProvisioningSchool {
  school_id: string;
  status: string;
  snapshot_date: string;
}

export interface ProvisionSchoolPayload {
  school_name: string;
  school_type: string;
  address?: string;
  state: string;
  lga?: string;
  phone: string;
  email: string;
  principal_name: string;
  principal_phone?: string;
  principal_email: string;
  subscription_tier?: string;
  modules?: string[];
  start_trial?: boolean;
}

export interface ProvisioningResponse {
  school_id: string;
  school_code: string;
  school_name: string;
  provisioning_status: string;
  admin_user_id: string;
  admin_email: string;
  temp_password_sent: boolean;
  onboarding_url: string;
  created_at: string;
}

export interface AdminUser {
  id: string;
  email: string;
  phone?: string | null;
  first_name: string;
  last_name: string;
  role: string;
  is_active: boolean;
  last_login_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateUserPayload {
  email: string;
  phone?: string | null;
  first_name: string;
  last_name: string;
  role: string;
  send_welcome_email?: boolean;
}

export interface SentinelThreshold {
  id: string;
  state?: string | null;
  lga?: string | null;
  symptom_category: string;
  time_window_hours: number;
  cluster_threshold: number;
  school_threshold_percent: number;
  lga_threshold_percent?: number | null;
  baseline_illness_rate?: number | null;
  is_active: boolean;
  effective_from: string;
  change_reason?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateThresholdPayload {
  symptom_category: string;
  time_window_hours: number;
  cluster_threshold: number;
  school_threshold_percent: number;
  lga_threshold_percent?: number | null;
  baseline_illness_rate?: number | null;
  change_reason: string;
}

export interface TrainingResource {
  id: string;
  title: string;
  description?: string;
  url: string;
  resource_type: string;
  category?: string;
  target_role?: string;
  created_at: string;
}

export interface TrainingAssignPayload {
  school_id: string;
  resource_ids: string[];
}

export async function getProvisioningSchools(params?: {
  status?: string;
}): Promise<ListResponse<ProvisioningSchool>> {
  const { data } = await apiClient.get('/admin/schools/provisioning', { params });
  return {
    items: data.items ?? [],
    total: data.total ?? 0,
    page: 1,
    pages: 1,
  };
}

export async function provisionSchool(payload: ProvisionSchoolPayload): Promise<ProvisioningResponse> {
  const { data } = await apiClient.post('/admin/schools/provision', payload);
  return data;
}

export async function getUsers(params?: {
  search?: string;
  role?: string;
  school_id?: string;
  status?: string;
  page?: number;
  per_page?: number;
}): Promise<ListResponse<AdminUser>> {
  const per_page = params?.per_page ?? 50;
  const page = params?.page ?? 1;
  const { data } = await apiClient.get('/admin/users', { params });
  const total = data.total ?? 0;

  return {
    items: data.items ?? [],
    total,
    page: data.page ?? page,
    pages: Math.max(1, Math.ceil(total / per_page)),
  };
}

export async function createUser(payload: CreateUserPayload): Promise<AdminUser> {
  const { data } = await apiClient.post('/admin/users', payload);
  return data;
}

export async function getSentinelThresholds(): Promise<SentinelThreshold[]> {
  const { data } = await apiClient.get('/admin/sentinel/thresholds');
  return data;
}

export async function createThreshold(payload: CreateThresholdPayload): Promise<SentinelThreshold> {
  const { data } = await apiClient.post('/admin/sentinel/thresholds', payload);
  return data;
}

// Sync Monitoring API
export async function getSyncDashboard(): Promise<SyncStatus> {
  const { data } = await apiClient.get('/admin/sync/status');
  return data;
}

export async function getSyncHistory(): Promise<{ items: SyncHistoryItem[] }> {
  const { data } = await apiClient.get('/admin/sync/history');
  return data;
}

export async function triggerSchoolSync(schoolId: string): Promise<{ success: boolean; sync_id: string }> {
  const { data } = await apiClient.post(`/admin/sync/schools/${schoolId}/trigger`);
  return data;
}

// Backup API
export async function listBackups(): Promise<BackupRecord[]> {
  const { data } = await apiClient.get('/admin/backup/list');
  return data.data;
}

export async function createBackup(backupType: string): Promise<BackupRecord> {
  const { data } = await apiClient.post('/admin/backup/create', null, {
    params: { backup_type: backupType },
  });
  return data;
}

export async function restoreBackup(backupId: string): Promise<{ success: boolean; message: string }> {
  const { data } = await apiClient.post(`/admin/backup/${backupId}/restore`);
  return data;
}

// Training API
export async function listTrainingResources(): Promise<TrainingResource[]> {
  const { data } = await apiClient.get('/admin/training/resources');
  return data;
}

export async function createTrainingResource(payload: Omit<TrainingResource, 'id' | 'created_at'>): Promise<TrainingResource> {
  const { data } = await apiClient.post('/admin/training/resources', payload);
  return data;
}

export async function assignTrainingToSchool(payload: TrainingAssignPayload): Promise<{ success: boolean }> {
  const { data } = await apiClient.post('/admin/training/assign', payload);
  return data;
}
export async function listSystemUpdates(): Promise<SystemUpdate[]> {
  const { data } = await apiClient.get('/admin/updates');
  return data;
}

export async function deploySystemUpdate(updateId: string): Promise<{ success: boolean; message: string }> {
  const { data } = await apiClient.post(`/admin/updates/${updateId}/deploy`);
  return data;
}
