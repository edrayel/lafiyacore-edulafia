import { apiClient } from '../../shared/api/client';
import type { AttendanceRecord } from '../../shared/types';

export interface AttendanceQueryParams {
  classId?: string;
  date?: string;
}

export interface MarkAttendancePayload {
  student_id: string;
  class_id: string;
  date: string;
  status: string;
  reason_code?: string;
  symptom_codes?: string[];
  notes?: string;
}

export interface AttendanceStats {
  total: number;
  present: number;
  absent: number;
  late: number;
  excused: number;
}

export async function getAttendance(params?: AttendanceQueryParams): Promise<AttendanceRecord[]> {
  const { data } = await apiClient.get('/attendance', { params });
  return data.items || data;
}

export async function markAttendance(
  classId: string,
  dateStr: string,
  records: MarkAttendancePayload[]
): Promise<AttendanceRecord[]> {
  const payload = {
    class_id: classId,
    date: dateStr,
    exceptions: records,
  };
  const { data } = await apiClient.post('/attendance/mark/bulk', payload);
  return data;
}

export async function getAttendanceStats(classId: string, date: string): Promise<AttendanceStats> {
  const { data } = await apiClient.get('/attendance/summary', {
    params: { class_id: classId, start_date: date, end_date: date },
  });
  return data;
}

export async function exportEMISAttendance(
  startDate: string,
  endDate: string,
  classId?: string
): Promise<{ download_url: string; record_count: number }> {
  const { data } = await apiClient.get('/attendance/export/emis', {
    params: { start_date: startDate, end_date: endDate, class_id: classId },
  });
  return data;
}
