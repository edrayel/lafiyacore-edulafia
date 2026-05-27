import { apiClient } from '../../shared/api/client';

export interface Book {
  id: string;
  title: string;
  author: string;
  category: string;
  isbn?: string;
  total_copies: number;
  available_copies: number;
  created_at: string;
}

export interface LendRecord {
  id: string;
  book_id: string;
  student_id: string;
  student_name: string;
  borrow_date: string;
  due_date: string;
  return_date: string | null;
  status: string;
}

export interface CreateBookPayload {
  title: string;
  author: string;
  category: string;
  isbn?: string;
  total_copies: number;
}

export interface LendBookPayload {
  book_id: string;
  student_id: string;
  due_date: string;
}

export async function getBooks(params?: { category?: string }): Promise<Book[]> {
  const { data } = await apiClient.get('/library/books', { params });
  return data;
}

export async function createBook(payload: CreateBookPayload): Promise<Book> {
  const { data } = await apiClient.post('/library/books', payload);
  return data;
}

export async function lendBook(payload: LendBookPayload): Promise<LendRecord> {
  const { data } = await apiClient.post('/library/lend', payload);
  return data;
}

export async function returnBook(id: string): Promise<void> {
  await apiClient.post(`/library/return/${id}`);
}

export async function getLendRecords(params?: { student_id?: string }): Promise<LendRecord[]> {
  const { data } = await apiClient.get('/library/lend-records', { params });
  return data;
}
