/** Format an ISO date ("2026-08-23") as Brazilian "23/08/2026" without TZ shifts. */
export function formatDateBR(iso: string): string {
  const [y, m, d] = iso.split("-");
  return `${d}/${m}/${y}`;
}
