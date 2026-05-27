import { apiClient } from '../../shared/api/client';
import type { ListResponse } from '../../shared/types';

export interface StaffProfile {
  id: string;
  staff_id: string;
  first_name: string;
  last_name: string;
  middle_name?: string;
  email?: string;
  phone: string;
  whatsapp_phone?: string;
  role: string;
  department?: string;
  employment_type: string;
  status: string;
  qualifications?: Record<string, string>;
  documents?: Record<string, string>;
}

export interface StaffMember {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  role: string;
  department: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface StaffQueryParams {
  page?: number;
  per_page?: number;
  search?: string;
  role?: string;
  status?: string;
}

export interface CreateStaffPayload {
  first_name: string;
  last_name: string;
  middle_name?: string;
  email?: string;
  phone: string;
  whatsapp_phone?: string;
  date_of_birth?: string;
  gender: string;
  address?: string;
  role: string;
  department?: string;
  qualifications?: Record<string, string>;
  documents?: Record<string, string>;
  subjects?: string[];
  employment_type?: string;
  employment_date?: string;
  salary?: number;
}

export interface UpdateStaffPayload extends Partial<CreateStaffPayload> {
  status?: string;
}

export async function getStaff(params?: StaffQueryParams): Promise<ListResponse<StaffMember>> {
  const { data } = await apiClient.get('/staff', { params });
  return data;
}

export async function uploadStaffDocument(staffId: string, formData: FormData): Promise<{ id: string; filename: string; uploaded_at: string }> {
  const { data } = await apiClient.post(`/staff/${staffId}/documents`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return data;
}

export async function deleteStaffDocument(staffId: string, docKey: string): Promise<void> {
  await apiClient.delete(`/staff/${staffId}/documents/${docKey}`);
}

export async function getStaffMember(id: string): Promise<StaffMember> {
  const { data } = await apiClient.get(`/staff/${id}`);
  return data;
}

export async function createStaff(payload: CreateStaffPayload): Promise<StaffMember> {
  const { data } = await apiClient.post('/staff', payload);
  return data;
}

export async function updateStaff(id: string, payload: UpdateStaffPayload): Promise<StaffMember> {
  const { data } = await apiClient.patch(`/staff/${id}`, payload);
  return data;
}

export async function archiveStaff(id: string): Promise<StaffMember> {
  const { data } = await apiClient.delete(`/staff/${id}`);
  return data;
}

export interface StaffAssignment {
  id: string;
  staff_id: string;
  class_id: string;
  subject_id?: string;
  academic_year_id: string;
  term_id?: string;
  assignment_type: string;
  is_form_teacher: boolean;
  start_date?: string;
  end_date?: string;
  is_active: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateStaffAssignmentPayload {
  staff_id: string;
  class_id: string;
  subject_id?: string;
  academic_year_id: string;
  term_id?: string;
  assignment_type?: string;
  is_form_teacher?: boolean;
  start_date?: string;
  end_date?: string;
  notes?: string;
}

export async function getStaffAssignments(params?: {
  staff_id?: string;
  class_id?: string;
  academic_year_id?: string;
}): Promise<StaffAssignment[]> {
  const { data } = await apiClient.get('/staff/assignments', { params });
  return data;
}

export async function createStaffAssignment(
  payload: CreateStaffAssignmentPayload
): Promise<StaffAssignment> {
  const { data } = await apiClient.post('/staff/assignments', payload);
  return data;
}

export async function deleteStaffAssignment(assignmentId: string): Promise<void> {
  await apiClient.delete(`/staff/assignments/${assignmentId}`);
}
export interface Timetable {
  id: string;
  name: string;
  academic_year: string;
  term: string;
  status: 'draft' | 'published' | 'archived';
  created_at: string;
  updated_at: string;
}

export interface TimetableEntry {
  id: string;
  timetable_id: string;
  staff_id: string;
  class_id: string;
  subject_id: string;
  day_of_week: number;
  start_time: string;
  end_time: string;
  room: string;
  staff_name?: string;
  subject_name?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTimetablePayload {
  name: string;
  academic_year: string;
  term: string;
}

export interface CreateTimetableEntryPayload {
  staff_id: string;
  class_id: string;
  subject_id: string;
  day_of_week: number;
  start_time: string;
  end_time: string;
  room?: string;
}

export async function getTimetables(): Promise<ListResponse<Timetable>> {
  const { data } = await apiClient.get('/staff/timetables');
  return data;
}

export async function getTimetable(id: string): Promise<Timetable> {
  const { data } = await apiClient.get(`/staff/timetables/${id}`);
  return data;
}

export async function createTimetable(payload: CreateTimetablePayload): Promise<Timetable> {
  const { data } = await apiClient.post('/staff/timetables', payload);
  return data;
}

export async function updateTimetable(
  id: string,
  payload: Partial<CreateTimetablePayload>
): Promise<Timetable> {
  const { data } = await apiClient.patch(`/staff/timetables/${id}`, payload);
  return data;
}

export async function deleteTimetable(id: string): Promise<void> {
  await apiClient.delete(`/staff/timetables/${id}`);
}

export async function getTimetableEntries(
  timetableId: string,
  includeNames?: boolean
): Promise<TimetableEntry[]> {
  const { data } = await apiClient.get(`/staff/timetables/${timetableId}/entries`, {
    params: includeNames ? { include_names: true } : undefined,
  });
  return data;
}

export async function addTimetableEntry(
  timetableId: string,
  payload: CreateTimetableEntryPayload
): Promise<TimetableEntry> {
  const { data } = await apiClient.post(`/staff/timetables/${timetableId}/entries`, payload);
  return data;
}

export async function updateTimetableEntry(
  timetableId: string,
  entryId: string,
  payload: Partial<CreateTimetableEntryPayload>
): Promise<TimetableEntry> {
  const { data } = await apiClient.patch(
    `/staff/timetables/${timetableId}/entries/${entryId}`,
    payload
  );
  return data;
}

export async function deleteTimetableEntry(timetableId: string, entryId: string): Promise<void> {
  await apiClient.delete(`/staff/timetables/${timetableId}/entries/${entryId}`);
}

export async function publishTimetable(id: string): Promise<Timetable> {
  const { data } = await apiClient.post(`/staff/timetables/${id}/publish`);
  return data;
}

export async function checkTimetableClashes(id: string): Promise<{ clashes: Array<{ time: string; subject: string; teacher: string }> }> {
  const { data } = await apiClient.get(`/staff/timetables/${id}/clashes`);
  return data;
}

// Staff Attendance API
export interface StaffAttendance {
  id: string;
  staff_id: string;
  check_in: string;
  check_out?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface CheckInPayload {
  latitude?: number;
  longitude?: number;
}

export interface CheckOutPayload {
  latitude?: number;
  longitude?: number;
}

export async function checkIn(payload: CheckInPayload): Promise<StaffAttendance> {
  const { data } = await apiClient.post('/staff/attendance/check-in', payload);
  return data;
}

export async function checkOut(payload: CheckOutPayload): Promise<StaffAttendance> {
  const { data } = await apiClient.post('/staff/attendance/check-out', payload);
  return data;
}

export async function getStaffAttendance(params?: {
  staff_id?: string;
  date?: string;
  start_date?: string;
  end_date?: string;
}): Promise<ListResponse<StaffAttendance>> {
  const { data } = await apiClient.get('/staff/attendance', { params });
  return data;
}
