import { apiClient } from '../../shared/api/client';

export interface BusRoute {
  id: string;
  name: string;
  driver_name: string;
  capacity: number;
  current_riders: number;
  route_description: string;
  is_active: boolean;
  created_at: string;
}

export interface CreateBusRoutePayload {
  name: string;
  driver_name: string;
  capacity: number;
  route_description: string;
}

export async function getBusRoutes(params?: { active_only?: boolean }): Promise<BusRoute[]> {
  const { data } = await apiClient.get('/bus-tracking/routes', { params });
  return data;
}

export async function createBusRoute(payload: CreateBusRoutePayload): Promise<BusRoute> {
  const { data } = await apiClient.post('/bus-tracking/routes', payload);
  return data;
}
