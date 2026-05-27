import { apiClient } from './client';
import type { User } from '../types';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ForgotPasswordResponse {
  message: string;
}

export interface ResetPasswordRequest {
  token: string;
  new_password: string;
}

export interface ResetPasswordResponse {
  message: string;
}

export const login = (data: LoginRequest) => apiClient.post<TokenResponse>('/auth/login', data);
export const logout = () => apiClient.post('/auth/logout');
export const getMe = () => apiClient.get<User>('/auth/me');
export const forgotPassword = (data: ForgotPasswordRequest) =>
  apiClient.post<ForgotPasswordResponse>('/auth/forgot-password', data);
export const resetPassword = (data: ResetPasswordRequest) =>
  apiClient.post<ResetPasswordResponse>('/auth/reset-password', data);
