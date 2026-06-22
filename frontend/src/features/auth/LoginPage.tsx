import {
  Alert,
  Button,
  Card,
  Center,
  PasswordInput,
  Stack,
  TextInput,
  Title,
} from "@mantine/core";
import { type FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";

import { ApiError } from "../../lib/apiClient";
import { useLogin } from "./useAuth";

export function LoginPage() {
  const navigate = useNavigate();
  const loginMutation = useLogin();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    loginMutation.mutate(
      { username, password },
      { onSuccess: () => navigate("/dashboard") },
    );
  };

  const errorMessage =
    loginMutation.error instanceof ApiError
      ? "Invalid username or password."
      : loginMutation.error
        ? "Something went wrong. Please try again."
        : null;

  return (
    <Center mih="100vh">
      <Card withBorder shadow="sm" padding="xl" radius="md" w={360}>
        <form onSubmit={handleSubmit}>
          <Stack>
            <Title order={2} ta="center">
              TUNA
            </Title>
            {errorMessage && (
              <Alert color="red" variant="light">
                {errorMessage}
              </Alert>
            )}
            <TextInput
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.currentTarget.value)}
              required
              autoFocus
            />
            <PasswordInput
              label="Password"
              value={password}
              onChange={(e) => setPassword(e.currentTarget.value)}
              required
            />
            <Button type="submit" loading={loginMutation.isPending} fullWidth>
              Log in
            </Button>
          </Stack>
        </form>
      </Card>
    </Center>
  );
}
