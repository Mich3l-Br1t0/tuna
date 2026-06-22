import { Button, Center, Stack, Text, Title } from "@mantine/core";
import { Link } from "react-router-dom";

import { SiteHeader } from "./SiteHeader";

/** Placeholder for nav destinations not built yet (Mídia, Resultados, ...). */
export function InProgressPage() {
  return (
    <>
      <SiteHeader />
      <Center mih="70vh">
        <Stack align="center" gap="md" px="md">
          <Text tt="uppercase" fw={700} c="brand.6" lts={2}>
            Em construção
          </Text>
          <Title order={1} ta="center">
            Esta página está sendo preparada
          </Title>
          <Text c="dimmed" ta="center" maw={420}>
            Estamos trabalhando nesta seção. Volte em breve para conferir as
            novidades.
          </Text>
          <Button component={Link} to="/" mt="sm">
            Voltar para a Home
          </Button>
        </Stack>
      </Center>
    </>
  );
}
