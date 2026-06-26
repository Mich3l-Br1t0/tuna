import { useQuery } from "@tanstack/react-query";

import { fetchEvents } from "./eventsApi";

export type { Event } from "./eventsApi";

/** All events ("provas"), for selection. Rarely changes; refetch hourly. */
export function useEvents() {
  return useQuery({
    queryKey: ["events"],
    queryFn: fetchEvents,
    staleTime: 60 * 60 * 1000,
  });
}
