import { apiClient } from '../../shared/api/client';

export interface Hostel {
  id: string;
  school_id: string;
  name: string;
  capacity: number;
  gender: string;
  created_at: string;
  updated_at: string;
}

export interface Room {
  id: string;
  hostel_id: string;
  room_number: string;
  capacity: number;
  created_at: string;
  updated_at: string;
}

export interface BedAllocation {
  id: string;
  room_id: string;
  student_id: string;
  academic_year_id: string;
  created_at: string;
  updated_at: string;
}

export interface CreateHostelPayload {
  school_id: string;
  name: string;
  capacity: number;
  gender: string;
}

export interface CreateRoomPayload {
  hostel_id: string;
  room_number: string;
  capacity: number;
}

export interface CreateAllocationPayload {
  room_id: string;
  student_id: string;
  academic_year_id: string;
}

// Hostels
export async function getHostels(school_id?: string): Promise<Hostel[]> {
  const { data } = await apiClient.get('/hostel/hostels', { params: { school_id } });
  return data;
}

export async function createHostel(payload: CreateHostelPayload): Promise<Hostel> {
  const { data } = await apiClient.post('/hostel/hostels', payload);
  return data;
}

export async function updateHostel(
  id: string,
  payload: Partial<CreateHostelPayload>
): Promise<Hostel> {
  const { data } = await apiClient.patch(`/hostel/hostels/${id}`, payload);
  return data;
}

export async function deleteHostel(id: string): Promise<void> {
  await apiClient.delete(`/hostel/hostels/${id}`);
}

// Rooms
export async function getRooms(hostelId: string): Promise<Room[]> {
  const { data } = await apiClient.get(`/hostel/hostels/${hostelId}/rooms`);
  return data;
}

export async function createRoom(payload: CreateRoomPayload): Promise<Room> {
  const { data } = await apiClient.post('/hostel/rooms', payload);
  return data;
}

export async function updateRoom(id: string, payload: Partial<CreateRoomPayload>): Promise<Room> {
  const { data } = await apiClient.patch(`/hostel/rooms/${id}`, payload);
  return data;
}

export async function deleteRoom(id: string): Promise<void> {
  await apiClient.delete(`/hostel/rooms/${id}`);
}

// Allocations
export async function getAllocationsByRoom(roomId: string): Promise<BedAllocation[]> {
  const { data } = await apiClient.get(`/hostel/rooms/${roomId}/allocations`);
  return data;
}

export async function getAllocationsByStudent(studentId: string): Promise<BedAllocation[]> {
  const { data } = await apiClient.get(`/hostel/students/${studentId}/allocations`);
  return data;
}

export async function createAllocation(payload: CreateAllocationPayload): Promise<BedAllocation> {
  const { data } = await apiClient.post('/hostel/allocations', payload);
  return data;
}

export async function deleteAllocation(id: string): Promise<void> {
  await apiClient.delete(`/hostel/allocations/${id}`);
}
