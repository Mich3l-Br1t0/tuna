import { Button, Card, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { Link } from "react-router-dom";

import { useAuth } from "../auth/useAuth";
import { useSiteContent } from "../site/useSiteContent";
import { useDashboardStats } from "./useDashboardStats";

export function DashboardPage() {
  const { user } = useAuth();
  const stats = useDashboardStats();
  const site = useSiteContent();

  return (
    <Stack gap="lg">
      <Title order={2}>Olá, {user?.username ?? ""} 👋</Title>

      <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="md">
        <Card withBorder radius="md" padding="lg" bg="brand.0">
          <Text tt="uppercase" fw={700} c="brand.8" fz="xs" lts={1}>
            Próxima etapa
          </Text>
          <Text fw={500} mt="xs">
            {site.data?.proxima_etapa ?? "—"}
          </Text>
        </Card>

        <StatCard label="Atletas" value={stats.data?.athletes} />
        <StatCard label="Inscrições" value={stats.data?.registrations} />

        <Card withBorder radius="md" padding="lg">
          <Text tt="uppercase" fw={700} c="dimmed" fz="xs" lts={1}>
            Resultados
          </Text>
          <Button component={Link} to="/resultados" variant="light" mt="md">
            Ver resultados →
          </Button>
        </Card>
      </SimpleGrid>
    </Stack>
  );
}

function StatCard({ label, value }: { label: string; value?: number }) {
  return (
    <Card withBorder radius="md" padding="lg">
      <Text tt="uppercase" fw={700} c="dimmed" fz="xs" lts={1}>
        {label}
      </Text>
      <Text fz={36} fw={800} c="brand.7">
        {value ?? "—"}
      </Text>
    </Card>
  );
}
