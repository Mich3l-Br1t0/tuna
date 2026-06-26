import {
  Alert,
  Anchor,
  Badge,
  Button,
  Card,
  Center,
  Chip,
  Group,
  Loader,
  SegmentedControl,
  Select,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { useState } from "react";
import { Link, useParams } from "react-router-dom";

import { ApiError } from "../../lib/apiClient";
import type { RegistrationAthlete } from "./registrationsApi";
import { useStages } from "./useStages";
import {
  useRegisterStage,
  useSetAthleteEntry,
  useStageRegistration,
} from "./useStageRegistration";

const STATUS_LABEL: Record<string, string> = {
  Pending: "Pendente",
  Submitted: "Enviada",
  Confirmed: "Confirmada",
};

function errorMessage(error: unknown): string | null {
  if (error instanceof ApiError) {
    const data = error.data;
    if (typeof data === "string") return data;
    if (Array.isArray(data)) return String(data[0]);
    if (data && typeof data === "object") {
      const first = Object.values(data)[0];
      return Array.isArray(first) ? String(first[0]) : String(first);
    }
  }
  return error ? "Não foi possível salvar a inscrição." : null;
}

export function StageRegistrationPage() {
  const { stageId: stageIdParam } = useParams();
  const stageId = Number(stageIdParam);

  const { data: stages } = useStages();
  const stage = stages?.find((s) => s.id === stageId);

  const { data, isLoading } = useStageRegistration(stageId);
  const register = useRegisterStage(stageId);
  const setEntry = useSetAthleteEntry(stageId);
  const [view, setView] = useState<"atleta" | "prova">("atleta");

  const error = errorMessage(register.error ?? setEntry.error);

  if (isLoading || !data) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  const open = data.registration_open;
  const enrolled = data.athletes.filter((a) => a.selected_event_ids.length > 0);
  const available = data.athletes.filter(
    (a) => a.selected_event_ids.length === 0,
  );

  const setEvents = (athleteId: number, eventIds: number[]) =>
    setEntry.mutate({ athleteId, eventIds });

  return (
    <Stack gap="lg">
      <div>
        <Anchor component={Link} to="/dashboard/etapas" size="sm">
          ← Etapas
        </Anchor>
        <Group justify="space-between" mt="xs">
          <Title order={2}>{stage?.name ?? "Etapa"}</Title>
          {data.status && (
            <Badge size="lg" variant="light">
              {STATUS_LABEL[data.status] ?? data.status}
            </Badge>
          )}
        </Group>
      </div>

      {error && (
        <Alert color="red" variant="light">
          {error}
        </Alert>
      )}

      {!open && (
        <Alert color="gray" variant="light">
          As inscrições para esta etapa estão encerradas.
        </Alert>
      )}

      {data.status === null ? (
        <Stack align="flex-start">
          <Text c="dimmed">Sua universidade ainda não está inscrita nesta etapa.</Text>
          <Button
            onClick={() => register.mutate()}
            loading={register.isPending}
            disabled={!open}
          >
            Inscrever universidade nesta etapa
          </Button>
        </Stack>
      ) : (
        <>
          <Group justify="space-between" align="center" wrap="nowrap">
            {view === "atleta" && open && available.length > 0 ? (
              <Select
                placeholder="Adicionar atleta…"
                searchable
                value={null}
                data={available.map((a) => ({
                  value: String(a.id),
                  label: a.name,
                }))}
                onChange={(value) => {
                  if (!value) return;
                  const athlete = available.find((a) => String(a.id) === value);
                  if (athlete) {
                    setEvents(
                      athlete.id,
                      athlete.eligible_events.map((e) => e.id),
                    );
                  }
                }}
                w={320}
              />
            ) : (
              <div />
            )}
            <SegmentedControl
              value={view}
              onChange={(v) => setView(v as "atleta" | "prova")}
              data={[
                { label: "Por atleta", value: "atleta" },
                { label: "Por prova", value: "prova" },
              ]}
            />
          </Group>

          {view === "atleta" ? (
            <Stack gap="sm">
              {enrolled.length === 0 ? (
                <Text c="dimmed">Nenhum atleta inscrito ainda.</Text>
              ) : (
                enrolled.map((a) => (
                  <AthleteCard
                    key={a.id}
                    athlete={a}
                    disabled={!open || setEntry.isPending}
                    onChange={(ids) => setEvents(a.id, ids)}
                    onRemove={() => setEvents(a.id, [])}
                  />
                ))
              )}
            </Stack>
          ) : (
            <ProvaView events={data.events} athletes={data.athletes} />
          )}
        </>
      )}
    </Stack>
  );
}

function AthleteCard({
  athlete,
  disabled,
  onChange,
  onRemove,
}: {
  athlete: RegistrationAthlete;
  disabled: boolean;
  onChange: (eventIds: number[]) => void;
  onRemove: () => void;
}) {
  return (
    <Card withBorder padding="sm">
      <Group justify="space-between" mb="xs">
        <Text fw={500}>{athlete.name}</Text>
        <Button
          variant="subtle"
          color="red"
          size="compact-sm"
          disabled={disabled}
          onClick={onRemove}
        >
          Remover
        </Button>
      </Group>
      <Chip.Group
        multiple
        value={athlete.selected_event_ids.map(String)}
        onChange={(values) => onChange(values.map(Number))}
      >
        <Group gap="xs">
          {athlete.eligible_events.map((e) => (
            <Chip key={e.id} value={String(e.id)} disabled={disabled} size="sm">
              {e.name}
            </Chip>
          ))}
        </Group>
      </Chip.Group>
    </Card>
  );
}

const NAIPE_LABEL: Record<"M" | "F", string> = {
  M: "Masculino",
  F: "Feminino",
};

/** Read-only view: every prova the stage offers, grouped by naipe, with its
 * registered athletes. */
function ProvaView({
  events,
  athletes,
}: {
  events: { id: number; name: string; genders: ("M" | "F")[] }[];
  athletes: RegistrationAthlete[];
}) {
  return (
    <Stack gap="sm">
      {events.map((event) => (
        <Card key={event.id} withBorder padding="sm">
          <Text fw={500} mb="xs">
            {event.name}
          </Text>
          <Stack gap="sm">
            {event.genders.map((gender) => {
              const registered = athletes.filter(
                (a) =>
                  a.gender === gender &&
                  a.selected_event_ids.includes(event.id),
              );
              return (
                <div key={gender}>
                  <Group gap="xs" mb={registered.length ? 6 : 0}>
                    <Text size="sm" fw={500} c="dimmed">
                      {NAIPE_LABEL[gender]}
                    </Text>
                    <Badge variant="light" size="sm">
                      {registered.length}{" "}
                      {registered.length === 1 ? "atleta" : "atletas"}
                    </Badge>
                  </Group>
                  {registered.length === 0 ? (
                    <Text size="sm" c="dimmed">
                      Nenhum atleta inscrito.
                    </Text>
                  ) : (
                    <Group gap="xs">
                      {registered.map((a) => (
                        <Badge key={a.id} variant="outline" color="gray">
                          {a.name}
                        </Badge>
                      ))}
                    </Group>
                  )}
                </div>
              );
            })}
          </Stack>
        </Card>
      ))}
    </Stack>
  );
}
