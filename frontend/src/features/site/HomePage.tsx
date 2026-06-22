import {
  Anchor,
  Box,
  Button,
  Card,
  Center,
  Container,
  Group,
  Loader,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { Link } from "react-router-dom";

import { SiteFooter } from "./SiteFooter";
import { SiteHeader } from "./SiteHeader";
import { useSiteContent } from "./useSiteContent";

/** Render a text block where paragraphs are separated by blank lines. */
function Paragraphs({ text }: { text: string }) {
  return (
    <>
      {text.split("\n\n").map((p, i) => (
        <Text key={i} c="dimmed" lh={1.7}>
          {p}
        </Text>
      ))}
    </>
  );
}

export function HomePage() {
  const { data, isLoading } = useSiteContent();

  if (isLoading || !data) {
    return (
      <Center mih="100vh">
        <Loader />
      </Center>
    );
  }

  return (
    <>
      <SiteHeader />

      {/* ponytail: gradient hero. Swap `background` for `url(<photo>)` to use the athletes photo. */}
      <Box
        style={{
          background: "linear-gradient(135deg, #006594 0%, #1b9fd6 100%)",
        }}
      >
        <Container size="lg" py={{ base: 72, sm: 112 }}>
          <Stack maw={660} gap="lg">
            <Title c="white" fz={{ base: 34, sm: 54 }} fw={800} lh={1.1}>
              Torneio Universitário de Atletismo
            </Title>
            <Text c="white" fz="lg" opacity={0.92}>
              Desde 1999 reunindo centenas de atletas universitários de São Paulo
              e das regiões Sul e Sudeste em quatro etapas por ano.
            </Text>
            <Group mt="sm" gap="lg">
              <Button
                component={Link}
                to="/inscricao"
                size="md"
                variant="white"
                color="dark"
              >
                Inscreva-se
              </Button>
              <Anchor href="#historico" c="white" fw={600}>
                Conheça o torneio ↓
              </Anchor>
            </Group>
          </Stack>
        </Container>
      </Box>

      <Container size="lg" py={64}>
        <Stack gap={64}>
          <Stack id="historico" gap="md">
            <Title order={2}>Histórico</Title>
            <Paragraphs text={data.historico} />
          </Stack>

          <Stack gap="md">
            <Title order={2}>O Torneio</Title>
            <Paragraphs text={data.o_torneio} />
          </Stack>

          <Card withBorder radius="md" padding="xl" bg="brand.0">
            <Stack gap="sm">
              <Text tt="uppercase" fw={700} c="brand.8" fz="sm" lts={1}>
                Próxima Etapa
              </Text>
              <Text fz="lg" fw={500}>
                {data.proxima_etapa}
              </Text>
              {data.regulamento_url && (
                <Button
                  component="a"
                  href={data.regulamento_url}
                  target="_blank"
                  w="fit-content"
                  mt="xs"
                >
                  Ver regulamento
                </Button>
              )}
            </Stack>
          </Card>
        </Stack>
      </Container>

      <SiteFooter content={data} />
    </>
  );
}
