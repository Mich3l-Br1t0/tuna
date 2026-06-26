import {
  AppShell,
  Burger,
  Button,
  Group,
  NavLink,
  Stack,
  Text,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";

import { useAuth, useLogout } from "../auth/useAuth";

const NAV = [
  { label: "Início", to: "/dashboard" },
  { label: "Atletas", to: "/dashboard/atletas" },
  { label: "Etapas", to: "/dashboard/etapas" },
  { label: "Resultados", to: "/dashboard/resultados", disabled: true },
];

export function DashboardLayout() {
  const [opened, { toggle, close }] = useDisclosure();
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();
  const logout = useLogout();

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
          {NAV.map((n) =>
            n.disabled ? (
              <NavLink key={n.to} label={n.label} disabled />
            ) : (
              <NavLink
                key={n.to}
                component={Link}
                to={n.to}
                label={n.label}
                active={location.pathname === n.to}
                onClick={close}
              />
            ),
          )}
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
