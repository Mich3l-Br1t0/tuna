import { useQuery } from "@tanstack/react-query";

import { api } from "../../lib/apiClient";

export type SiteContent = {
  historico: string;
  o_torneio: string;
  proxima_etapa: string;
  regulamento_url: string;
  contato_email: string;
  instagram_url: string;
  facebook_url: string;
};

/** Public home-page text, edited in Django admin (django-solo singleton). */
export function useSiteContent() {
  return useQuery({
    queryKey: ["site-content"],
    queryFn: () => api.get<SiteContent>("/api/site-content/"),
    staleTime: 60 * 60 * 1000, // content rarely changes; refetch hourly
  });
}
