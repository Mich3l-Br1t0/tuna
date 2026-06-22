import { Button, Container, Group, Stack, Text, Title } from "@mantine/core";
import { useNavigate } from "react-router-dom";

import { useAuth, useLogout } from "../auth/useAuth";

export function DashboardPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const logoutMutation = useLogout();

  const handleLogout = () => {
    logoutMutation.mutate(undefined, {
      onSuccess: () => navigate("/login"),
    });
  };

  return (
    <Container size="sm" py="xl">
      <Stack>
        <Group justify="space-between">
          <Title order={2}>Dashboard</Title>
          <Button
            variant="light"
            onClick={handleLogout}
            loading={logoutMutation.isPending}
          >
            Log out
          </Button>
        </Group>
        <Text>Welcome{user ? `, ${user.username}` : ""}. You are signed in.</Text>
      </Stack>
    </Container>
  );
}
