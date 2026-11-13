const configuredBase = (
  import.meta.env.VITE_API_URL || "http://localhost:8000/api"
)
  .trim()
  .replace(/\/+$/, "");

const API_BASE = configuredBase.endsWith("/api")
  ? configuredBase
  : `${configuredBase}/api`;

async function request(path, options = {}, token = "") {
  const headers = new Headers(options.headers || {});

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    if (!response.ok) {
      throw new Error("La operación no pudo completarse");
    }
    return null;
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Ocurrió un error en la solicitud");
  }

  return data;
}

export const api = {
  getProducts: () => request("/products"),
  getCurrentUser: (token) => request("/auth/me", {}, token),
  getMyOrders: (token) => request("/orders/me", {}, token),
  getAdminSummary: (token) => request("/admin/summary", {}, token),
  getAdminOrders: (token) => request("/admin/orders", {}, token),

  login: (email, password) =>
    request("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username: email, password }),
    }),

  register: (payload) =>
    request("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),

  checkout: (items, token) =>
    request(
      "/orders/checkout",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items, payment_method: "simulated" }),
      },
      token,
    ),

  saveProduct: (payload, productId, token) =>
    request(
      productId ? `/products/${productId}` : "/products",
      {
        method: productId ? "PATCH" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      },
      token,
    ),

  deleteProduct: (productId, token) =>
    request(`/products/${productId}`, { method: "DELETE" }, token),
};
