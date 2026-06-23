import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  type AthleteInput,
  type AthleteListParams,
  createAthlete,
  deleteAthlete,
  fetchAthletes,
  updateAthlete,
} from "./athletesApi";

export type { Athlete, AthleteInput } from "./athletesApi";

/** Paginated, filtered athlete roster (auth required). */
export function useAthletes(params: AthleteListParams) {
  return useQuery({
    queryKey: ["athletes", params],
    queryFn: () => fetchAthletes(params),
    placeholderData: keepPreviousData, // keep the old page visible while fetching the next
  });
}

// After any write, refresh the roster AND the dashboard counts that depend on it.
function useRosterInvalidation() {
  const queryClient = useQueryClient();
  return () => {
    queryClient.invalidateQueries({ queryKey: ["athletes"] });
    queryClient.invalidateQueries({ queryKey: ["dashboard-stats"] });
  };
}

export function useCreateAthlete() {
  const invalidate = useRosterInvalidation();
  return useMutation({
    mutationFn: (data: AthleteInput) => createAthlete(data),
    onSuccess: invalidate,
  });
}

export function useUpdateAthlete() {
  const invalidate = useRosterInvalidation();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: AthleteInput }) =>
      updateAthlete(id, data),
    onSuccess: invalidate,
  });
}

export function useDeleteAthlete() {
  const invalidate = useRosterInvalidation();
  return useMutation({
    mutationFn: (id: number) => deleteAthlete(id),
    onSuccess: invalidate,
  });
}
