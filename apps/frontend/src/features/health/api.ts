import { apiClient } from '../../shared/api/client';
import type { ListResponse } from '../../shared/types';

export interface HealthProfile {
  id: string;
  student_id: string;
  school_id: string;
  blood_group?: string;
  genotype?: string;
  chronic_conditions?: string[] | null;
  allergies?: string[] | null;
  disability_status?: string;
  current_medications?: string[] | null;
  emergency_notes?: string | null;
  vision_left?: number | string | null;
  vision_right?: number | string | null;
  hearing_left?: string | null;
  hearing_right?: string | null;
  parental_consent_given: boolean;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface SickBayVisit {
  id: string;
  student_id: string;
  school_id: string;
  visit_date: string;
  visit_time: string;
  presenting_complaint_codes: string[];
  presenting_complaint_notes?: string | null;
  temperature?: number;
  blood_pressure_systolic?: number | null;
  blood_pressure_diastolic?: number | null;
  pulse_rate?: number;
  treatment_given?: string | null;
  outcome: string;
  referred_to?: string | null;
  parent_notified: boolean;
  is_sentinel_relevant: boolean;
  recorded_by: string;
  created_at: string;
  updated_at: string;
}

export interface Referral {
  id: string;
  student_id: string;
  school_id: string;
  referral_date: string;
  destination_facility: string;
  reason: string;
  priority: string;
  status: string;
  follow_up_due_date: string;
  outcome_notes?: string | null;
  outcome_date?: string | null;
  reminder_sent: boolean;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface Vaccination {
  id: string;
  student_id: string;
  school_id: string;
  vaccine_name: string;
  vaccine_code?: string | null;
  dose_number: number;
  administration_date: string;
  lot_number?: string;
  administering_facility?: string | null;
  created_at: string;
  updated_at: string;
}

export interface SentinelAlert {
  id: string;
  symptom_profile: Record<string, number>;
  students_affected: number;
  threshold_type?: string;
  alert_tier: string;
  status: string;
  date_generated: string;
}

export interface CreateSickBayVisitPayload {
  student_id: string;
  presenting_complaint_codes: string[];
  presenting_complaint_notes?: string;
  temperature?: number;
  blood_pressure_systolic?: number;
  blood_pressure_diastolic?: number;
  pulse_rate?: number;
  treatment_given?: string;
  outcome: string;
  referred_to?: string;
}

export interface CreateReferralPayload {
  student_id: string;
  destination_facility: string;
  reason: string;
  priority: string;
  follow_up_due_date: string;
}

export interface CreateVaccinationPayload {
  student_id: string;
  vaccine_name: string;
  vaccine_code?: string;
  dose_number: number;
  administration_date: string;
  lot_number?: string;
  administering_facility?: string;
}

export async function getHealthProfile(studentId: string): Promise<HealthProfile | null> {
  try {
    const { data } = await apiClient.get(`/health/students/${studentId}/profile`);
    return data;
  } catch (error: unknown) {
    if (error && typeof error === 'object' && 'response' in error) {
      const err = error as { response: { status: number } };
      if (err.response?.status === 404) return null;
    }
    throw error;
  }
}

export async function createHealthProfile(
  studentId: string,
  payload: Omit<HealthProfile, 'id' | 'created_at' | 'updated_at' | 'version'>
): Promise<HealthProfile> {
  const { data } = await apiClient.post(`/health/students/${studentId}/profile`, payload);
  return data;
}

export async function updateHealthProfile(
  studentId: string,
  payload: Partial<Omit<HealthProfile, 'id' | 'student_id' | 'school_id' | 'created_at' | 'updated_at'>>
): Promise<HealthProfile> {
  const { data } = await apiClient.patch(`/health/students/${studentId}/profile`, payload);
  return data;
}

export async function getSickBayVisits(params?: {
  student_id?: string;
  start_date?: string;
  end_date?: string;
  page?: number;
  per_page?: number;
}): Promise<ListResponse<SickBayVisit> & { per_page: number }> {
  const { data } = await apiClient.get('/health/sick-bay-visits', { params });
  return data;
}

export async function createSickBayVisit(
  payload: CreateSickBayVisitPayload
): Promise<SickBayVisit> {
  const { data } = await apiClient.post('/health/sick-bay-visits', payload);
  return data;
}

export async function getReferrals(params?: { status?: string }): Promise<Referral[]> {
  const { data } = await apiClient.get('/health/referrals', { params });
  return data;
}

export async function createReferral(payload: CreateReferralPayload): Promise<Referral> {
  const { data } = await apiClient.post('/health/referrals', payload);
  return data;
}

export async function updateReferral(id: string, payload: { status: string }): Promise<Referral> {
  const { data } = await apiClient.patch(`/health/referrals/${id}`, payload);
  return data;
}

export async function getVaccinations(studentId: string): Promise<Vaccination[]> {
  const { data } = await apiClient.get(`/health/vaccinations/${studentId}`);
  return data;
}

export async function createVaccination(payload: CreateVaccinationPayload): Promise<Vaccination> {
  const { data } = await apiClient.post('/health/vaccinations', payload);
  return data;
}

export async function getSentinelAlerts(params?: {
  status?: string;
  alert_tier?: string;
}): Promise<ListResponse<SentinelAlert>> {
  const { data } = await apiClient.get('/sentinel/alerts', { params });
  if (Array.isArray(data)) {
    return { items: data, total: data.length, page: 1, pages: 1 };
  }
  return data;
}

export async function acknowledgeAlert(id: string): Promise<void> {
  await apiClient.patch(`/sentinel/alerts/${id}/acknowledge`, { response_notes: '' });
}

export interface Screening {
  id: string;
  student_id: string;
  screening_date: string;
  screening_type: string;
  height?: number;
  weight?: number;
  bmi?: number | null;
  muac?: number | null;
  vision_left?: number;
  vision_right?: number;
  hearing_left?: string;
  hearing_right?: string;
  blood_pressure_systolic?: number | null;
  blood_pressure_diastolic?: number | null;
  dental_notes?: string | null;
  sickle_cell_test_result?: string | null;
  phq_a_score?: number;
  sdq_score?: number;
  flags?: string[] | null;
  follow_up_required: boolean;
  follow_up_notes?: string | null;
  conducted_by: string;
  created_at: string;
  updated_at: string;
}

export async function createScreening(payload: Partial<Screening>): Promise<Screening> {
  const { data } = await apiClient.post('/health/screenings', payload);
  return data;
}

// Offline-first sync capabilities for health data (for rural medical camps)
const PENDING_SCREENINGS_KEY = 'edulafia_pending_screenings';

// Derive a temporary symmetric key from sessionStorage to encrypt offline data
// This ensures data is unreadable if the tab is closed, protecting shared devices.
async function getEncryptionKey(): Promise<CryptoKey> {
  const keyStr = sessionStorage.getItem('edulafia_sync_key');
  if (!keyStr) {
    const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, [
      'encrypt',
      'decrypt',
    ]);
    const exported = await crypto.subtle.exportKey('jwk', key);
    sessionStorage.setItem('edulafia_sync_key', JSON.stringify(exported));
    return key;
  }
  try {
    const parsed = JSON.parse(keyStr);
    return await crypto.subtle.importKey('jwk', parsed, { name: 'AES-GCM' }, true, [
      'encrypt',
      'decrypt',
    ]);
  } catch {
    sessionStorage.removeItem('edulafia_sync_key');
    const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, [
      'encrypt',
      'decrypt',
    ]);
    const exported = await crypto.subtle.exportKey('jwk', key);
    sessionStorage.setItem('edulafia_sync_key', JSON.stringify(exported));
    return key;
  }
}

export async function getPendingScreenings(): Promise<Partial<Screening>[]> {
  const stored = localStorage.getItem(PENDING_SCREENINGS_KEY);
  if (!stored) return [];
  try {
    const key = await getEncryptionKey();
    const { iv, data } = JSON.parse(stored);
    const decrypted = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: new Uint8Array(iv) },
      key,
      new Uint8Array(data)
    );
    return JSON.parse(new TextDecoder().decode(decrypted));
  } catch (e) {
    console.error('Failed to decrypt offline screenings. Key may have been lost.', e);
    return [];
  }
}

export async function savePendingScreenings(payload: Partial<Screening>[]): Promise<void> {
  const key = await getEncryptionKey();
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encoded = new TextEncoder().encode(JSON.stringify(payload));
  const encrypted = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, encoded);
  const encryptedStr = JSON.stringify({
    iv: Array.from(iv),
    data: Array.from(new Uint8Array(encrypted)),
  });
  localStorage.setItem(PENDING_SCREENINGS_KEY, encryptedStr);
}

export function clearPendingScreenings(): void {
  localStorage.removeItem(PENDING_SCREENINGS_KEY);
}

export async function syncPendingScreenings(): Promise<void> {
  if (!navigator.onLine) return;

  const pending = await getPendingScreenings();
  if (pending.length === 0) return;

  try {
    await apiClient.post('/health/screenings/bulk', pending);
    clearPendingScreenings();
  } catch (error) {
    console.error('Failed to sync pending screenings', error);
  }
}

export async function batchCreateScreenings(payload: Partial<Screening>[]): Promise<Screening[]> {
  if (!navigator.onLine) {
    // Store locally if offline
    const pending = await getPendingScreenings();
    await savePendingScreenings([...pending, ...payload]);
    console.warn('Offline mode: Screenings saved locally and will sync when online.');

    // Return mock data for UI optimism
    return payload.map((p) => ({
      ...p,
      id: crypto.randomUUID(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    })) as Screening[];
  }

  // If online, try to sync any existing pending data first
  await syncPendingScreenings();

  // Then send current payload
  const { data } = await apiClient.post('/health/screenings/bulk', payload);
  return data;
}
