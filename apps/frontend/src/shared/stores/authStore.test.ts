import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useAuthStore } from './authStore';
import * as authApi from '../api/auth';

vi.mock('../api/auth', () => ({
  login: vi.fn(),
  logout: vi.fn(),
  getMe: vi.fn(),
  forgotPassword: vi.fn(),
  resetPassword: vi.fn(),
}));

describe('Auth Store', () => {
  beforeEach(() => {
    // Reset store state before each test
    useAuthStore.setState({ user: null, isLoading: false, error: null });
    vi.clearAllMocks();
  });

  describe('login', () => {
    it('successfully logs in and sets user state', async () => {
      (authApi.login as any).mockResolvedValue({});
      (authApi.getMe as any).mockResolvedValue({
        data: { email: 'admin@edulafia.com', role: 'admin' },
      });

      const { login } = useAuthStore.getState();

      await login('admin@edulafia.com', 'password123');

      const state = useAuthStore.getState();
      expect(state.error).toBeNull();
      expect(state.isLoading).toBe(false);
      expect(state.user).toMatchObject({
        email: 'admin@edulafia.com',
        role: 'admin',
      });
    });

    it('handles login failure and sets error state', async () => {
      const mockError = {
        response: { data: { detail: 'Incorrect email or password' } },
      };
      (authApi.login as any).mockRejectedValue(mockError);

      const { login } = useAuthStore.getState();

      try {
        await login('wrong@email.com', 'badpass');
      } catch {
        // Expected to throw
      }

      const state = useAuthStore.getState();
      expect(state.user).toBeNull();
      expect(state.isLoading).toBe(false);
      expect(state.error).toBe('Incorrect email or password');
    });
  });

  describe('logout', () => {
    it('clears user state on logout', async () => {
      (authApi.logout as any).mockResolvedValue({});

      // Set initial logged-in state
      useAuthStore.setState({
        user: {
          id: '1',
          email: 'test@test.com',
          role: 'teacher',
          first_name: 'T',
          last_name: 'T',
          status: 'active',
          school_id: 'school-1',
        } as any,
      });

      const { logout } = useAuthStore.getState();
      await logout();

      const state = useAuthStore.getState();
      expect(state.user).toBeNull();
    });
  });
});
