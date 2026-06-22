import { Center, Loader } from "@mantine/core";
import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";

import { useAuth } from "./useAuth";

export function RequireAuth({ children }: { children: ReactNode }) {
  const { isLoading, isAuthenticated } = useAuth();

  if (isLoading) {
    return (
      <Center mih="100vh">
        <Loader />
      </Center>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
