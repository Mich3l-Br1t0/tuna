import { useQuery } from "@tanstack/react-query";

import { api } from "../../lib/apiClient";

export type DashboardStats = {
  athletes: number;
  registrations: number;
  universities: number;
};

/** Aggregate counts for the dashboard overview (auth required). */
export function useDashboardStats() {
  return useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: () => api.get<DashboardStats>("/api/dashboard/stats/"),
  });
}
