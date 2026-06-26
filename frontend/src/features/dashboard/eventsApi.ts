import { api } from "../../lib/apiClient";

export type Event = {
  id: number;
  name: string;
  category: string;
};

export const fetchEvents = () => api.get<Event[]>("/api/events/");
