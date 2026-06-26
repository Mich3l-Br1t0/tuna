import { useQuery } from "@tanstack/react-query";

import { fetchStages } from "./stagesApi";

export type { Stage } from "./stagesApi";

/** All stages with their registration window status. */
export function useStages() {
  return useQuery({
    queryKey: ["stages"],
    queryFn: fetchStages,
    staleTime: 5 * 60 * 1000,
  });
}
