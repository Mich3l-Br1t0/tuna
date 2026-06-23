import { api } from "../../lib/apiClient";

export type Athlete = {
  id: number;
  name: string;
  gender: "M" | "F";
};

export type AthleteInput = {
  name: string;
  gender: "M" | "F";
};

export type Paginated<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export type AthleteListParams = {
  name?: string;
  gender?: "M" | "F" | null;
  limit: number;
  offset: number;
};

export const fetchAthletes = (params: AthleteListParams) => {
  const query = new URLSearchParams();
  query.set("limit", String(params.limit));
  query.set("offset", String(params.offset));
  if (params.name) query.set("name", params.name);
  if (params.gender) query.set("gender", params.gender);
  return api.get<Paginated<Athlete>>(`/api/athletes/?${query.toString()}`);
};

export const createAthlete = (data: AthleteInput) =>
  api.post<unknown>("/api/athletes/create/", data);

export const updateAthlete = (id: number, data: AthleteInput) =>
  api.post<unknown>(`/api/athletes/${id}/update/`, data);

export const deleteAthlete = (id: number) =>
  api.post<unknown>(`/api/athletes/${id}/delete/`);
