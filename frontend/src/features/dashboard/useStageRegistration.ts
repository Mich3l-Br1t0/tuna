import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  fetchStageRegistration,
  registerStage,
  setAthleteEntry,
} from "./registrationsApi";

export type { RegistrationAthlete, StageRegistration } from "./registrationsApi";

export function useStageRegistration(stageId: number) {
  return useQuery({
    queryKey: ["stage-registration", stageId],
    queryFn: () => fetchStageRegistration(stageId),
  });
}

export function useRegisterStage(stageId: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => registerStage(stageId),
    onSuccess: () =>
      queryClient.invalidateQueries({
        queryKey: ["stage-registration", stageId],
      }),
  });
}

export function useSetAthleteEntry(stageId: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      athleteId,
      eventIds,
    }: {
      athleteId: number;
      eventIds: number[];
    }) => setAthleteEntry(stageId, athleteId, eventIds),
    onSuccess: () =>
      queryClient.invalidateQueries({
        queryKey: ["stage-registration", stageId],
      }),
  });
}
