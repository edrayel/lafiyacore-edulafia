import { create } from 'zustand';
import {
  login as apiLogin,
  logout as apiLogout,
  getMe,
  forgotPassword as apiForgotPassword,
  resetPassword as apiResetPassword,
} from '../api/auth';
import type { User } from '../types';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
  clearError: () => void;
  forgotPassword: (email: string) => Promise<void>;
  resetPassword: (token: string, newPassword: string) => Promise<void>;
}

let actionInFlight = false;

export const useAuthStore = create<AuthState>()((set, get) => ({
  user: null,
  isLoading: false,
  error: null,
  login: async (email, password) => {
    if (actionInFlight) return;
    actionInFlight = true;
    set({ isLoading: true, error: null });
    try {
      await apiLogin({ email, password });
      await get().loadUser();
      set({ isLoading: false });
    } catch (err: unknown) {
      const message = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Invalid credentials';
      set({ isLoading: false, error: message });
      throw err;
    } finally {
      actionInFlight = false;
    }
  },
  logout: async () => {
    if (actionInFlight) return;
    actionInFlight = true;
    try {
      await apiLogout();
    } catch (err) {
      console.warn('Logout API call failed, clearing local session anyway', err);
    }
    set({ user: null, error: null });
    actionInFlight = false;
  },
  loadUser: async () => {
    try {
      const { data } = await getMe();
      set({ user: data });
    } catch (e) {
      set({ user: null });
      throw e;
    }
  },
  clearError: () => set({ error: null }),
  forgotPassword: async (email) => {
    set({ isLoading: true, error: null });
    try {
      await apiForgotPassword({ email });
      set({ isLoading: false });
    } catch (e: unknown) {
      set({ isLoading: false, error: (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to send reset email' });
      throw e;
    }
  },
  resetPassword: async (token, newPassword) => {
    set({ isLoading: true, error: null });
    try {
      await apiResetPassword({ token, new_password: newPassword });
      set({ isLoading: false });
    } catch (e: unknown) {
      set({ isLoading: false, error: (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to reset password' });
      throw e;
    }
  },
}));