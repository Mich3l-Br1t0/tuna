const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const REFRESH_PATH = "/api/auth/token/refresh/";

function readCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

export class ApiError extends Error {
  readonly status: number;
  readonly data: unknown;

  constructor(status: number, data: unknown) {
    super(`API error ${status}`);
    this.status = status;
    this.data = data;
  }
}

type RequestOptions = {
  method?: string;
  json?: unknown;
};

async function rawRequest(path: string, options: RequestOptions): Promise<Response> {
  const method = options.method ?? "GET";
  const headers: Record<string, string> = {};

  if (options.json !== undefined) {
    headers["Content-Type"] = "application/json";
  }
  // dj-rest-auth's cookie JWT auth enforces CSRF on unsafe methods.
  if (method !== "GET" && method !== "HEAD") {
    const csrf = readCookie("csrftoken");
    if (csrf) headers["X-CSRFToken"] = csrf;
  }

  return fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    credentials: "include",
    body: options.json !== undefined ? JSON.stringify(options.json) : undefined,
  });
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  let response = await rawRequest(path, options);

  // One-shot refresh-then-retry on an expired access cookie.
  if (response.status === 401 && path !== REFRESH_PATH) {
    const refreshed = await rawRequest(REFRESH_PATH, { method: "POST" });
    if (refreshed.ok) {
      response = await rawRequest(path, options);
    }
  }

  const data = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) {
    throw new ApiError(response.status, data);
  }
  return data as T;
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, json?: unknown) => request<T>(path, { method: "POST", json }),
};
