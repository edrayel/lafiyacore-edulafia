import { apiClient } from '../../shared/api/client';

export interface MealPlan {
  id: string;
  name: string;
  description?: string;
  price: number;
  is_active: boolean;
  meals_per_day: number;
  created_at: string;
}

export interface CreateMealPlanPayload {
  name: string;
  description?: string;
  price: number;
  meals_per_day: number;
}

export async function getMealPlans(params?: { active_only?: boolean }): Promise<MealPlan[]> {
  const { data } = await apiClient.get('/cafeteria/meal-plans', { params });
  return data;
}

export async function createMealPlan(payload: CreateMealPlanPayload): Promise<MealPlan> {
  const { data } = await apiClient.post('/cafeteria/meal-plans', payload);
  return data;
}
