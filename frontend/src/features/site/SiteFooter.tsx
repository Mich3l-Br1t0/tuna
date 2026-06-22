import { Anchor, Box, Container, SimpleGrid, Stack, Text } from "@mantine/core";
import { Link } from "react-router-dom";

import type { SiteContent } from "./useSiteContent";

const SOBRE = [
  { label: "TUNA", to: "/sobre" },
  { label: "História", to: "/sobre" },
  { label: "Regulamento", to: "/sobre" },
  { label: "Próxima Etapa", to: "/" },
  { label: "Contato", to: "/sobre" },
];

export function SiteFooter({ content }: { content: SiteContent }) {
  return (
    <Box bg="dark.8" c="gray.4">
      <Container size="lg" py={48}>
        <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="xl">
          <Stack gap="xs">
            <Text fw={800} fz="xl" c="white">
              TUNA
            </Text>
            <Text fz="sm">Torneio Universitário de Atletismo</Text>
          </Stack>

          <Stack gap="xs">
            <Text fw={700} c="white">
              Sobre
            </Text>
            {SOBRE.map((l) => (
              <Anchor key={l.label} component={Link} to={l.to} c="gray.4" fz="sm">
                {l.label}
              </Anchor>
            ))}
          </Stack>

          <Stack gap="xs">
            <Text fw={700} c="white">
              Contato
            </Text>
            <Anchor href={`mailto:${content.contato_email}`} c="gray.4" fz="sm">
              {content.contato_email}
            </Anchor>
            {content.instagram_url && (
              <Anchor href={content.instagram_url} target="_blank" c="gray.4" fz="sm">
                Instagram
              </Anchor>
            )}
            {content.facebook_url && (
              <Anchor href={content.facebook_url} target="_blank" c="gray.4" fz="sm">
                Facebook
              </Anchor>
            )}
          </Stack>
        </SimpleGrid>
      </Container>

      <Box bg="dark.9">
        <Container size="lg" py="md">
          <Text fz="sm">© TUNA — Torneio Universitário de Atletismo</Text>
        </Container>
      </Box>
    </Box>
  );
}
