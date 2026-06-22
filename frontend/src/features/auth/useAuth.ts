import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { ApiError } from "../../lib/apiClient";
import {
  type LoginCredentials,
  fetchCurrentUser,
  login,
  logout,
} from "./authApi";

const AUTH_USER_KEY = ["auth-user"] as const;

/** The current-user query IS the source of truth for "am I logged in?". */
export function useAuth() {
  const query = useQuery({
    queryKey: AUTH_USER_KEY,
    queryFn: fetchCurrentUser,
    retry: false, // a 401 means "not logged in", not a transient failure
    staleTime: 5 * 60 * 1000,
  });

  return {
    user: query.data ?? null,
    isLoading: query.isLoading,
    isAuthenticated: query.isSuccess,
    isUnauthenticated: query.isError && (query.error as ApiError).status === 401,
  };
}

export function useLogin() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (credentials: LoginCredentials) => login(credentials),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: AUTH_USER_KEY }),
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => logout(),
    onSuccess: () => queryClient.setQueryData(AUTH_USER_KEY, null),
    onSettled: () => queryClient.invalidateQueries({ queryKey: AUTH_USER_KEY }),
  });
}
