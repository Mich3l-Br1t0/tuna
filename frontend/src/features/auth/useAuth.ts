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
    // true whenever a request is in flight (initial load OR a refetch), so guards
    // can wait instead of acting on stale cached data.
    isFetching: query.isFetching,
    isAuthenticated: query.isSuccess,
    isUnauthenticated: query.isError && (query.error as ApiError).status === 401,
  };
}

export function useLogin() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (credentials: LoginCredentials) => login(credentials),
    // Drop any cached "401 / unauthenticated" error from before login, so the
    // next observer (RequireAuth) refetches fresh instead of reading a stale miss.
    onSuccess: () => queryClient.removeQueries({ queryKey: AUTH_USER_KEY }),
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
