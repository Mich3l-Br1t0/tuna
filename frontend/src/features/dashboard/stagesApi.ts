import { api } from "../../lib/apiClient";

export type Stage = {
  id: number;
  name: string;
  date: string | null;
  location: string | null;
  registration_opens: string | null;
  registration_deadline: string | null;
  registration_open: boolean;
};

export const fetchStages = () => api.get<Stage[]>("/api/stages/");
