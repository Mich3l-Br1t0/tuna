import "@mantine/core/styles.css";

import { MantineProvider } from "@mantine/core";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";

import { LoginPage } from "./features/auth/LoginPage";
import { RequireAuth } from "./features/auth/RequireAuth";
import { AthletesPage } from "./features/dashboard/AthletesPage";
import { DashboardLayout } from "./features/dashboard/DashboardLayout";
import { DashboardPage } from "./features/dashboard/DashboardPage";
import { HomePage } from "./features/site/HomePage";
import { InProgressPage } from "./features/site/InProgressPage";
import { theme } from "./theme";

const queryClient = new QueryClient();

const router = createBrowserRouter([
  { path: "/", element: <HomePage /> },
  { path: "/login", element: <LoginPage /> },
  {
    path: "/dashboard",
    element: (
      <RequireAuth>
        <DashboardLayout />
      </RequireAuth>
    ),
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "atletas", element: <AthletesPage /> },
    ],
  },
  // Nav destinations not built yet — shared placeholder.
  { path: "/midia", element: <InProgressPage /> },
  { path: "/resultados", element: <InProgressPage /> },
  { path: "/recordes", element: <InProgressPage /> },
  { path: "/inscricao", element: <InProgressPage /> },
  { path: "/sobre", element: <InProgressPage /> },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MantineProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
        <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
    </MantineProvider>
  </StrictMode>,
);
