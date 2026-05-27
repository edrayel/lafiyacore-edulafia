export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  status: string;
  school_id: string | null;
}
export interface Student {
  id: string;
  first_name: string;
  last_name: string;
  middle_name?: string;
  date_of_birth: string;
  gender: string;
  admission_number: string;
  admission_date: string;
  class_id?: string;
  nationality?: string;
  state_of_origin?: string;
  lga_of_origin?: string;
  nin?: string;
  address?: string;
  medical_conditions?: string;
  special_needs?: string;
  status: string;
}
export interface Guardian {
  id: string;
  school_id: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  relationship_type: string;
  email?: string;
  whatsapp_number?: string;
  occupation?: string;
  address?: string;
  nin?: string;
  portal_access: boolean;
}
export interface AttendanceRecord {
  id: string;
  student_id: string;
  class_id: string;
  date: string;
  status: string;
  reason_code?: string;
  symptom_codes?: string[];
  notes?: string;
}
export interface Subject {
  id: string;
  name: string;
  code: string;
  class_id?: string;
  is_core: boolean;
}
export interface SickBayVisit {
  id: string;
  student_id: string;
  visit_date: string;
  visit_time: string;
  presenting_complaint_codes: string[];
  temperature?: number;
  outcome: string;
  is_sentinel_relevant: boolean;
}
export interface FeeSchedule {
  id: string;
  class_id: string;
  term_id?: string;
  fee_type: string;
  amount: number;
  due_date: string;
  is_mandatory: boolean;
}
export interface Payment {
  id: string;
  student_id: string;
  fee_schedule_id: string;
  amount_paid: number;
  payment_method: string;
  receipt_number: string;
  status: string;
  payment_date: string;
}
export interface Staff {
  id: string;
  staff_id: string;
  first_name: string;
  last_name: string;
  email?: string;
  phone: string;
  role: string;
  department?: string;
  status: string;
}
export interface School {
  id: string;
  name: string;
  code: string;
  state: string;
  lga: string;
  phone: string;
  email: string;
  status: string;
}
export interface SentinelAlert {
  id: string;
  symptom_profile: Record<string, number>;
  students_affected: number;
  alert_tier: string;
  status: string;
  date_generated: string;
}
export interface Notification {
  id: string;
  notification_type: string;
  title: string;
  message: string;
  channel: string;
  status: string;
  sent_at: string;
  read_at: string | null;
}
export interface ChildSummary {
  student_id: string;
  first_name: string;
  last_name: string;
  admission_number: string;
  class_name: string;
  status: string;
}
export interface KPIResponse {
  code: string;
  name: string;
  value: number;
  unit: string;
  trend: string | null;
  status: string;
}
export interface DashboardQuickStats {
  total_students: number;
  total_teachers: number;
  total_classes: number;
  active_alerts: number;
}
export interface ListResponse<T> {
  items: T[];
  total: number;
  page: number;
  pages: number;
}
