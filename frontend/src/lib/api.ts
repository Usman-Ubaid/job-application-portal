const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

interface ApiResponse<T> {
  success: string;
  message: string;
  data: T;
}

interface ApiError {
  errors: Record<string, string[]>;
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<ApiResponse<T>> {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    credentials: "include",
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw errorData;
  }

  return response.json();
}

export const api = {
  post: <T>(endpoint: string, body: unknown) => {
    return apiRequest<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },
  get: <T>(endpoint: string) => {
    return apiRequest<T>(endpoint, {
      method: "GET",
    });
  },
};

export type { ApiResponse, ApiError };
