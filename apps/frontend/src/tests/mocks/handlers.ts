import { http, HttpResponse } from 'msw';

export const handlers = [
  // Authentication Handlers
  http.post('*/api/v1/auth/login', () => {
    return HttpResponse.json({
      access_token: 'mock-access-token',
      refresh_token: 'mock-refresh-token',
      token_type: 'bearer',
      user: {
        id: '123e4567-e89b-12d3-a456-426614174000',
        email: 'admin@edulafia.com',
        role: 'admin',
        first_name: 'Admin',
        last_name: 'User',
      },
    });
  }),

  http.post('*/api/v1/auth/logout', () => {
    return HttpResponse.json({ message: 'Successfully logged out' });
  }),

  http.post('*/api/v1/auth/refresh', () => {
    return HttpResponse.json({ detail: 'Invalid refresh token' }, { status: 401 });
  }),

  http.get('*/api/v1/auth/me', () => {
    return HttpResponse.json({
      id: '123e4567-e89b-12d3-a456-426614174000',
      email: 'admin@edulafia.com',
      role: 'admin',
      first_name: 'Admin',
      last_name: 'User',
    });
  }),
];
