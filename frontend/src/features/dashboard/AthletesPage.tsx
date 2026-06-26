import {
  ActionIcon,
  Alert,
  Button,
  Center,
  Group,
  Loader,
  Modal,
  MultiSelect,
  Pagination,
  Select,
  Stack,
  Table,
  Text,
  TextInput,
  Title,
  Tooltip,
} from "@mantine/core";
import { useDebouncedValue, useDisclosure } from "@mantine/hooks";
import { type FormEvent, useEffect, useState } from "react";

import { ApiError } from "../../lib/apiClient";
import {
  type Athlete,
  useAthletes,
  useCreateAthlete,
  useDeleteAthlete,
  useUpdateAthlete,
} from "./useAthletes";
import { useEvents } from "./useEvents";

const GENDER: Record<string, string> = { M: "Masculino", F: "Feminino" };
const GENDER_OPTIONS = [
  { value: "M", label: "Masculino" },
  { value: "F", label: "Feminino" },
];
const PAGE_SIZES = ["25", "50"];

function IconPencil() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" />
    </svg>
  );
}

function IconTrash() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <polyline points="3 6 5 6 21 6" />
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
      <line x1="10" y1="11" x2="10" y2="17" />
      <line x1="14" y1="11" x2="14" y2="17" />
    </svg>
  );
}

/** Pull a human-readable message out of a DRF error response. */
function errorMessage(error: unknown): string | null {
  if (!error) return null;
  if (error instanceof ApiError) {
    const data = error.data;
    if (typeof data === "string") return data;
    if (Array.isArray(data)) return String(data[0]);
    if (data && typeof data === "object") {
      const first = Object.values(data)[0];
      return Array.isArray(first) ? String(first[0]) : String(first);
    }
  }
  return "Não foi possível salvar o atleta.";
}

export function AthletesPage() {
  const [search, setSearch] = useState("");
  const [debouncedSearch] = useDebouncedValue(search, 300);
  const [gender, setGender] = useState<string | null>(null);
  const [event, setEvent] = useState<string | null>(null);
  const [pageSize, setPageSize] = useState(25);
  const [page, setPage] = useState(1);

  const { data: events } = useEvents();

  // Any filter / page-size change resets to the first page.
  useEffect(() => {
    setPage(1);
  }, [debouncedSearch, gender, event, pageSize]);

  const { data, isLoading } = useAthletes({
    name: debouncedSearch || undefined,
    gender: gender as "M" | "F" | null,
    event: event ? Number(event) : null,
    limit: pageSize,
    offset: (page - 1) * pageSize,
  });

  const athletes = data?.results ?? [];
  const count = data?.count ?? 0;
  const totalPages = Math.max(1, Math.ceil(count / pageSize));

  const deleteMutation = useDeleteAthlete();
  const [formOpened, form] = useDisclosure(false);
  const [deleteOpened, del] = useDisclosure(false);
  const [editing, setEditing] = useState<Athlete | null>(null);
  const [deleting, setDeleting] = useState<Athlete | null>(null);

  const openCreate = () => {
    setEditing(null);
    form.open();
  };
  const openEdit = (a: Athlete) => {
    setEditing(a);
    form.open();
  };
  const openDelete = (a: Athlete) => {
    setDeleting(a);
    del.open();
  };
  const confirmDelete = () => {
    if (deleting) deleteMutation.mutate(deleting.id, { onSuccess: del.close });
  };

  return (
    <Stack gap="lg">
      <Group justify="space-between">
        <Title order={2}>Atletas</Title>
        <Button onClick={openCreate}>Novo atleta</Button>
      </Group>

      <Group align="flex-end">
        <TextInput
          label="Buscar"
          placeholder="Buscar por nome…"
          value={search}
          onChange={(e) => setSearch(e.currentTarget.value)}
          flex={1}
          maw={360}
        />
        <Select
          label="Gênero"
          placeholder="Todos"
          data={GENDER_OPTIONS}
          value={gender}
          onChange={setGender}
          clearable
          w={180}
        />
        <Select
          label="Prova"
          placeholder="Todas"
          data={(events ?? []).map((e) => ({
            value: String(e.id),
            label: e.name,
          }))}
          value={event}
          onChange={setEvent}
          searchable
          clearable
          w={220}
        />
        <Select
          label="Por página"
          data={PAGE_SIZES}
          value={String(pageSize)}
          onChange={(v) => v && setPageSize(Number(v))}
          w={120}
          allowDeselect={false}
        />
      </Group>

      {isLoading ? (
        <Center py="xl">
          <Loader />
        </Center>
      ) : athletes.length === 0 ? (
        <Text c="dimmed">Nenhum atleta encontrado.</Text>
      ) : (
        <>
          <Table.ScrollContainer minWidth={420}>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Nome</Table.Th>
                  <Table.Th>Gênero</Table.Th>
                  <Table.Th w={100}>Ações</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {athletes.map((a) => (
                  <Table.Tr key={a.id}>
                    <Table.Td>{a.name}</Table.Td>
                    <Table.Td>{GENDER[a.gender] ?? a.gender}</Table.Td>
                    <Table.Td>
                      <Group gap="xs">
                        <Tooltip label="Editar">
                          <ActionIcon
                            variant="subtle"
                            aria-label="Editar"
                            onClick={() => openEdit(a)}
                          >
                            <IconPencil />
                          </ActionIcon>
                        </Tooltip>
                        <Tooltip label="Excluir">
                          <ActionIcon
                            variant="subtle"
                            color="red"
                            aria-label="Excluir"
                            onClick={() => openDelete(a)}
                          >
                            <IconTrash />
                          </ActionIcon>
                        </Tooltip>
                      </Group>
                    </Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
          </Table.ScrollContainer>

          <Group justify="space-between">
            <Text size="sm" c="dimmed">
              {count} {count === 1 ? "atleta" : "atletas"}
            </Text>
            {totalPages > 1 && (
              <Pagination value={page} onChange={setPage} total={totalPages} />
            )}
          </Group>
        </>
      )}

      <AthleteFormModal
        key={editing?.id ?? "new"}
        opened={formOpened}
        onClose={form.close}
        athlete={editing}
      />

      <Modal
        opened={deleteOpened}
        onClose={del.close}
        title="Excluir atleta"
        centered
      >
        <Stack>
          <Text>
            Tem certeza que deseja excluir <b>{deleting?.name}</b>?
          </Text>
          <Group justify="flex-end">
            <Button variant="default" onClick={del.close}>
              Cancelar
            </Button>
            <Button
              color="red"
              loading={deleteMutation.isPending}
              onClick={confirmDelete}
            >
              Excluir
            </Button>
          </Group>
        </Stack>
      </Modal>
    </Stack>
  );
}

function AthleteFormModal({
  opened,
  onClose,
  athlete,
}: {
  opened: boolean;
  onClose: () => void;
  athlete: Athlete | null;
}) {
  const isEdit = athlete !== null;
  const createMutation = useCreateAthlete();
  const updateMutation = useUpdateAthlete();

  const [name, setName] = useState(athlete?.name ?? "");
  const [gender, setGender] = useState<string | null>(athlete?.gender ?? null);
  const [eventIds, setEventIds] = useState<string[]>(
    athlete?.events.map((e) => String(e.id)) ?? [],
  );

  const { data: events } = useEvents();

  const pending = createMutation.isPending || updateMutation.isPending;
  const valid = name.trim() !== "" && gender !== null;
  const error = errorMessage(createMutation.error ?? updateMutation.error);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!valid) return;
    const data = {
      name: name.trim(),
      gender: gender as "M" | "F",
      event_ids: eventIds.map(Number),
    };
    if (isEdit) {
      updateMutation.mutate({ id: athlete.id, data }, { onSuccess: onClose });
    } else {
      createMutation.mutate(data, { onSuccess: onClose });
    }
  };

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={isEdit ? "Editar atleta" : "Novo atleta"}
      centered
    >
      <form onSubmit={handleSubmit}>
        <Stack>
          {error && (
            <Alert color="red" variant="light">
              {error}
            </Alert>
          )}
          <TextInput
            label="Nome"
            value={name}
            onChange={(e) => setName(e.currentTarget.value)}
            required
            autoFocus
          />
          <Select
            label="Gênero"
            placeholder="Selecione…"
            data={GENDER_OPTIONS}
            value={gender}
            onChange={setGender}
            required
          />
          <MultiSelect
            label="Provas"
            placeholder="Selecione as provas…"
            data={(events ?? []).map((e) => ({
              value: String(e.id),
              label: e.name,
            }))}
            value={eventIds}
            onChange={setEventIds}
            searchable
            clearable
          />
          <Button type="submit" loading={pending} disabled={!valid} mt="sm">
            {isEdit ? "Salvar" : "Criar"}
          </Button>
        </Stack>
      </form>
    </Modal>
  );
}
