import axios from 'axios';

const API_BASE_URL = (import.meta.env.VITE_API_URL || '').replace(/\/+$/, '');

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 30000,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
});

let refreshPromise: Promise<void> | null = null;

apiClient.interceptors.response.use(
  (r) => r,
  async (error) => {
    if (error.response?.status !== 401 || error.config._retried) {
      return Promise.reject(error);
    }

    if (error.config?.url === '/auth/refresh') {
      window.location.href = '/login';
      return Promise.reject(error);
    }

    if (!refreshPromise) {
      refreshPromise = (async () => {
        try {
          await apiClient.post('/auth/refresh');
        } finally {
          refreshPromise = null;
        }
      })();
    }

    try {
      await refreshPromise;
      error.config._retried = true;
      return apiClient(error.config);
    } catch {
      window.location.href = '/login';
      return Promise.reject(error);
    }
  }
);