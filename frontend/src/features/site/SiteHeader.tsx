import {
  Anchor,
  Box,
  Burger,
  Button,
  Container,
  Drawer,
  Group,
  Stack,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Link } from "react-router-dom";

import { useAuth } from "../auth/useAuth";

const NAV = [
  { label: "Home", to: "/" },
  { label: "Mídia", to: "/midia" },
  { label: "Resultados", to: "/resultados" },
  { label: "Recordes", to: "/recordes" },
  { label: "Inscrição", to: "/inscricao" },
  { label: "Sobre", to: "/sobre" },
];

export function SiteHeader() {
  const [opened, { toggle, close }] = useDisclosure(false);
  const { isAuthenticated } = useAuth();
  const entrar = isAuthenticated
    ? { to: "/dashboard", label: "Dashboard" }
    : { to: "/login", label: "Entrar" };

  return (
    <Box
      component="header"
      style={{
        position: "sticky",
        top: 0,
        zIndex: 100,
        background: "white",
        borderBottom: "1px solid var(--mantine-color-gray-2)",
      }}
    >
      <Container size="lg">
        <Group h={64} justify="space-between">
          <Anchor component={Link} to="/" underline="never">
            <img
              src="/tuna-logo.svg"
              alt="TUNA — Torneio Universitário de Atletismo"
              style={{ height: 40, display: "block" }}
            />
          </Anchor>

          <Group gap="lg" visibleFrom="sm">
            {NAV.map((n) => (
              <Anchor
                key={n.to}
                component={Link}
                to={n.to}
                c="dark"
                fw={500}
                fz="sm"
                underline="never"
              >
                {n.label}
              </Anchor>
            ))}
            <Button component={Link} to={entrar.to} size="sm">
              {entrar.label}
            </Button>
          </Group>

          <Burger opened={opened} onClick={toggle} hiddenFrom="sm" aria-label="Menu" />
        </Group>
      </Container>

      <Drawer
        opened={opened}
        onClose={close}
        title="TUNA"
        hiddenFrom="sm"
        position="right"
        size="xs"
      >
        <Stack>
          {NAV.map((n) => (
            <Anchor
              key={n.to}
              component={Link}
              to={n.to}
              onClick={close}
              c="dark"
              fw={500}
            >
              {n.label}
            </Anchor>
          ))}
          <Button component={Link} to={entrar.to} onClick={close} fullWidth mt="sm">
            {entrar.label}
          </Button>
        </Stack>
      </Drawer>
    </Box>
  );
}
