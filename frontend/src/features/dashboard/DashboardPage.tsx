import {
  AppShell,
  Burger,
  Button,
  Card,
  Group,
  NavLink,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Link, useNavigate } from "react-router-dom";

import { useAuth, useLogout } from "../auth/useAuth";
import { useSiteContent } from "../site/useSiteContent";
import { useDashboardStats } from "./useDashboardStats";

// Only "Início" is built so far; the rest preview the planned structure.
const NAV = [
  { label: "Início", active: true },
  { label: "Atletas", disabled: true },
  { label: "Etapas", disabled: true },
  { label: "Resultados", disabled: true },
];

export function DashboardPage() {
  const [opened, { toggle }] = useDisclosure();
  const navigate = useNavigate();
  const { user } = useAuth();
  const logout = useLogout();
  const stats = useDashboardStats();
  const site = useSiteContent();

  const handleLogout = () =>
    logout.mutate(undefined, { onSuccess: () => navigate("/login") });

  return (
    <AppShell
      header={{ height: 64 }}
      navbar={{ width: 220, breakpoint: "sm", collapsed: { mobile: !opened } }}
      padding="md"
    >
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Group gap="sm">
            <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
            <Link to="/">
              <img
                src="/tuna-logo.svg"
                alt="TUNA"
                style={{ height: 34, display: "block" }}
              />
            </Link>
          </Group>
          <Group gap="md">
            <Text fz="sm" c="dimmed" visibleFrom="xs">
              Olá, {user?.username ?? ""}
            </Text>
            <Button
              variant="light"
              size="sm"
              onClick={handleLogout}
              loading={logout.isPending}
            >
              Sair
            </Button>
          </Group>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="sm">
        <Stack gap={4}>
          {NAV.map((n) => (
            <NavLink
              key={n.label}
              label={n.label}
              active={n.active}
              disabled={n.disabled}
            />
          ))}
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main>
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
      </AppShell.Main>
    </AppShell>
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
