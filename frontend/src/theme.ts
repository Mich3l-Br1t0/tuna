import { createTheme, type MantineColorsTuple } from "@mantine/core";

// TUNA brand cyan, built around the logo blue (#29ABE2).
const brand: MantineColorsTuple = [
  "#e6f7ff",
  "#cdeeff",
  "#9ddcfb",
  "#69caf7",
  "#41baf4",
  "#29abe2",
  "#1b9fd6",
  "#0d8bc0",
  "#007aab",
  "#006594",
];

export const theme = createTheme({
  primaryColor: "brand",
  primaryShade: 6,
  colors: { brand },
});
