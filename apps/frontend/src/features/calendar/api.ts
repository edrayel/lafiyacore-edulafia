import { apiClient } from '../../shared/api/client';

export interface CalendarEvent {
  id: string;
  title: string;
  description?: string;
  start_date: string;
  end_date: string;
  event_type: string;
}

export interface CreateEventPayload {
  title: string;
  description?: string;
  start_date: string;
  end_date: string;
  event_type: string;
}

export type UpdateEventPayload = Partial<CreateEventPayload>;

export async function getEvents(params?: {
  page?: number;
  per_page?: number;
  start_date?: string;
  end_date?: string;
}): Promise<{ items: CalendarEvent[]; total: number }> {
  const { data } = await apiClient.get('/calendar/events', { params });
  return data;
}

export async function createEvent(payload: CreateEventPayload): Promise<CalendarEvent> {
  const { data } = await apiClient.post('/calendar/events', payload);
  return data;
}

export async function updateEvent(id: string, payload: UpdateEventPayload): Promise<CalendarEvent> {
  const { data } = await apiClient.patch(`/calendar/events/${id}`, payload);
  return data;
}

export async function archiveEvent(id: string): Promise<void> {
  await apiClient.delete(`/calendar/events/${id}`);
}
