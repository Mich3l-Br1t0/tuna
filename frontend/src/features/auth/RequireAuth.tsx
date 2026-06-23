import { Center, Loader } from "@mantine/core";
import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";

import { useAuth } from "./useAuth";

export function RequireAuth({ children }: { children: ReactNode }) {
  const { isLoading, isFetching, isAuthenticated } = useAuth();

  // Already authenticated — render even if a background refetch is running.
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // Still determining (initial load or an in-flight refetch) — wait, don't bounce.
  if (isLoading || isFetching) {
    return (
      <Center mih="100vh">
        <Loader />
      </Center>
    );
  }

  // Settled and not authenticated.
  return <Navigate to="/login" replace />;
}
