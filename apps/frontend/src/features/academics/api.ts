import { apiClient } from '../../shared/api/client';

function unwrapApiData<T>(value: unknown): T {
  if (typeof value === 'object' && value !== null && 'data' in value) {
    return (value as { data: unknown }).data as T;
  }
  return value as T;
}

export interface AcademicMetadataEntity {
  id: string;
  name?: string;
  code?: string;
}

export interface AcademicMetadata {
  school_id?: string;
  school?: AcademicMetadataEntity;
  academic_year?: AcademicMetadataEntity;
  term?: AcademicMetadataEntity;
  class?: AcademicMetadataEntity;
  subject?: AcademicMetadataEntity;
}

export interface AcademicClass {
  id: string;
  name: string;
}

export interface Subject {
  id: string;
  name: string;
  code: string;
  class_id?: string;
  is_core: boolean;
  waec_code?: string;
  neco_code?: string;
}

export interface AcademicResult {
  id: string;
  student_id: string;
  subject_id: string;
  class_id: string;
  term_id: string;
  school_id: string;
  ca_scores?: Record<string, number>;
  ca_total: number;
  exam_score: number;
  total_score: number;
  grade?: string;
  class_rank?: number;
  flag?: string;
  teacher_id?: string;
  submitted_at?: string;
  created_at: string;
  updated_at: string;
}

export interface GradingScale {
  id: string;
  grade: string;
  min_score: number;
  max_score: number;
  remark: string;
}

export interface CreateSubjectPayload {
  name: string;
  code: string;
  class_id?: string;
  is_core: boolean;
  waec_code?: string;
  neco_code?: string;
}

export interface EnterScorePayload {
  student_id: string;
  subject_id: string;
  class_id: string;
  term_id: string;
  academic_year_id: string;
  ca_scores?: Record<string, number>;
  exam_score: number;
  flag?: string;
}

export interface BulkScoreEntryPayload {
  subject_id: string;
  class_id: string;
  term_id: string;
  scores: EnterScorePayload[];
}

export async function getAcademicMetadata(): Promise<AcademicMetadata> {
  const { data } = await apiClient.get<unknown>('/academics/metadata');
  return unwrapApiData<AcademicMetadata>(data);
}

export async function getClasses() {
  const { data } = await apiClient.get<unknown>('/academics/classes');
  return unwrapApiData<AcademicClass[]>(data);
}

export async function getSubjects(params?: { class_id?: string }): Promise<Subject[]> {
  const { data } = await apiClient.get<unknown>('/subjects', { params });
  return unwrapApiData<Subject[]>(data);
}

export async function createSubject(payload: CreateSubjectPayload): Promise<Subject> {
  const { data } = await apiClient.post<unknown>('/subjects', payload);
  return unwrapApiData<Subject>(data);
}

export async function updateSubject(
  id: string,
  payload: Partial<CreateSubjectPayload>
): Promise<Subject> {
  const { data } = await apiClient.patch<unknown>(`/subjects/${id}`, payload);
  return unwrapApiData<Subject>(data);
}

export async function archiveSubject(id: string): Promise<void> {
  await apiClient.delete(`/subjects/${id}`);
}

export async function enterScores(payload: EnterScorePayload): Promise<AcademicResult> {
  const { data } = await apiClient.post<unknown>('/academics/scores', payload);
  return unwrapApiData<AcademicResult>(data);
}

export async function enterScoresBulk(payload: BulkScoreEntryPayload): Promise<AcademicResult[]> {
  const { data } = await apiClient.post<unknown>('/academics/scores/bulk', payload);
  return unwrapApiData<AcademicResult[]>(data);
}

export interface ReportCardSubjectResult {
  subject_id: string;
  subject_name?: string;
  subject_code?: string;
  ca_total: number;
  exam_score: number;
  total_score: number;
  grade?: string;
}

export interface ReportCard {
  subject_results?: ReportCardSubjectResult[];
  average?: number;
  overall_grade?: string;
}

export async function generateReportCard(studentId: string, termId: string): Promise<ReportCard> {
  const { data } = await apiClient.get<unknown>(`/academics/report-cards/${studentId}/${termId}`);
  return unwrapApiData<ReportCard>(data);
}

export async function sendReportCard(
  studentId: string,
  termId: string,
  method: 'whatsapp' | 'sms'
): Promise<void> {
  await apiClient.post(`/academics/report-cards/${studentId}/${termId}/send`, { method });
}

export async function getScores(
  classId: string,
  subjectId: string,
  termId: string
): Promise<AcademicResult[]> {
  const { data } = await apiClient.get<unknown>('/academics/scores', {
    params: { class_id: classId, subject_id: subjectId, term_id: termId },
  });
  return unwrapApiData<AcademicResult[]>(data);
}

export async function computeGrades(classId: string, termId: string): Promise<void> {
  await apiClient.post('/academics/grades/compute', { class_id: classId, term_id: termId });
}

export async function getGradingScales(): Promise<GradingScale[]> {
  const { data } = await apiClient.get<unknown>('/academics/grades/scales');
  const unwrapped = unwrapApiData<unknown>(data);

  if (typeof unwrapped === 'object' && unwrapped !== null && 'scales' in unwrapped) {
    const scales = (unwrapped as { scales?: Array<{ details?: Omit<GradingScale, 'id'>[] }> }).scales;
    const details = scales?.[0]?.details;
    if (details) {
      return details.map((d) => ({ id: d.grade, ...d }));
    }
  }
  return unwrapApiData<GradingScale[]>(unwrapped);
}

export async function getStudentResults(
  studentId: string,
  termId?: string
): Promise<AcademicResult[]> {
  const { data } = await apiClient.get(`/academics/grades/${studentId}`, {
    params: { term_id: termId },
  });
  return data;
}
