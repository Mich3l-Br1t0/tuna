import { api } from "../../lib/apiClient";

export type RegistrationAthlete = {
  id: number;
  name: string;
  gender: "M" | "F";
  eligible_events: { id: number; name: string }[];
  selected_event_ids: number[];
};

export type StageRegistration = {
  status: "Pending" | "Submitted" | "Confirmed" | null;
  registration_open: boolean;
  events: { id: number; name: string; genders: ("M" | "F")[] }[];
  athletes: RegistrationAthlete[];
};

export const fetchStageRegistration = (stageId: number) =>
  api.get<StageRegistration>(`/api/registrations/${stageId}/`);

export const registerStage = (stageId: number) =>
  api.post<unknown>(`/api/registrations/${stageId}/register/`);

export const setAthleteEntry = (
  stageId: number,
  athleteId: number,
  eventIds: number[],
) =>
  api.post<unknown>(
    `/api/registrations/${stageId}/athletes/${athleteId}/set/`,
    { event_ids: eventIds },
  );
