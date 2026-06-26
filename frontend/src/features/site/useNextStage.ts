import { useQuery } from "@tanstack/react-query";

import { api } from "../../lib/apiClient";

export type NextStage = {
  name: string;
  date: string;
  location: string | null;
};

/** The next upcoming stage (etapa), computed from the database. Null if none. */
export function useNextStage() {
  return useQuery({
    queryKey: ["next-stage"],
    queryFn: () => api.get<NextStage | null>("/api/stages/next/"),
    staleTime: 60 * 60 * 1000, // refetch hourly
  });
}
