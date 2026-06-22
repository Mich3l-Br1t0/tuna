import { api } from "../../lib/apiClient";

export type CurrentUser = {
  pk: number;
  username: string;
  email: string;
};

export type LoginCredentials = {
  username: string;
  password: string;
};

export const login = (credentials: LoginCredentials) =>
  api.post<unknown>("/api/auth/login/", credentials);

export const logout = () => api.post<unknown>("/api/auth/logout/");

export const fetchCurrentUser = () => api.get<CurrentUser>("/api/auth/user/");
