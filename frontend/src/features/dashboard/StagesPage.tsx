import {
  Badge,
  Button,
  Center,
  Group,
  Loader,
  Stack,
  Table,
  Text,
  Title,
} from "@mantine/core";
import { Link } from "react-router-dom";

import { formatDateBR } from "../../lib/date";
import { useStages } from "./useStages";

function registrationWindow(
  opens: string | null,
  deadline: string | null,
): string {
  if (!deadline) return "—";
  const from = opens ? formatDateBR(opens) : "…";
  return `${from} a ${formatDateBR(deadline)}`;
}

export function StagesPage() {
  const { data: stages, isLoading } = useStages();

  return (
    <Stack gap="lg">
      <Title order={2}>Etapas</Title>

      {isLoading ? (
        <Center py="xl">
          <Loader />
        </Center>
      ) : !stages || stages.length === 0 ? (
        <Text c="dimmed">Nenhuma etapa cadastrada.</Text>
      ) : (
        <Table.ScrollContainer minWidth={520}>
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Etapa</Table.Th>
                <Table.Th>Data</Table.Th>
                <Table.Th>Inscrições</Table.Th>
                <Table.Th>Situação</Table.Th>
                <Table.Th w={140} />
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {stages.map((s) => (
                <Table.Tr key={s.id}>
                  <Table.Td>{s.name}</Table.Td>
                  <Table.Td>{s.date ? formatDateBR(s.date) : "—"}</Table.Td>
                  <Table.Td>
                    {registrationWindow(
                      s.registration_opens,
                      s.registration_deadline,
                    )}
                  </Table.Td>
                  <Table.Td>
                    <Badge color={s.registration_open ? "green" : "gray"}>
                      {s.registration_open ? "Abertas" : "Encerradas"}
                    </Badge>
                  </Table.Td>
                  <Table.Td>
                    <Button
                      component={Link}
                      to={`/dashboard/etapas/${s.id}`}
                      size="xs"
                      variant="light"
                    >
                      Inscrição
                    </Button>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        </Table.ScrollContainer>
      )}
    </Stack>
  );
}
