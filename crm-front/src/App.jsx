// AI GENERATED

import React, { useEffect, useMemo, useState } from "react";

const API_BASE = "/api/v1";
const AUTH_HEADER_PREFIX = "Bearer";

const analyticsEndpoints = {
  leadCustomerConversionRate: "/analytics/from-lead-to-customer-conversion-rate/",
  dealWonConversionRate: "/analytics/from-deal-to-won-conversion-rate/",
  totalPipelineValue: "/analytics/total-pipeline-value/",
  totalRevenue: "/analytics/total-revenue/",
  lastMonthRevenue: "/analytics/last-month-revenue/",
  popularCourses: "/analytics/popular-courses/",
  summary: "/analytics/summary/",
};

const resources = {
  accounts: {
    title: "Accounts",
    singular: "Account",
    path: "/accounts/",
    canWrite: ["manager", "director"],
    canDelete: ["director"],
    fields: [
      ["name", "Name", "text", true],
      ["account_type", "Type", "select", true, ["SCHOOL", "UNIVERSITY", "COMPANY", "OTHER"]],
      ["status", "Status", "select", false, ["new", "active", "customer", "lead"]],
      ["country", "Country", "select", true, ["RUSSIA", "BELARUS", "KAZAKHSTAN", "USA", "EUROPE", "OTHER"]],
      ["city", "City", "text", true],
      ["address", "Address", "text", true],
      ["description", "Description", "textarea", false],
    ],
  },
  contacts: {
    title: "Contacts",
    singular: "Contact",
    path: "/contacts/",
    canWrite: ["manager", "director"],
    canDelete: ["director"],
    fields: [
      ["first_name", "First name", "text", true],
      ["last_name", "Last name", "text", false],
      ["email", "Email", "email", true],
      ["phone", "Phone", "text", false],
      ["account", "Account UUID", "text", true],
    ],
  },
  courses: {
    title: "Courses",
    singular: "Course",
    path: "/courses/",
    canWrite: ["manager", "director"],
    canDelete: ["director"],
    fields: [
      ["name", "Name", "text", true],
      ["description", "Description", "textarea", false],
      ["status", "Status", "select", false, ["active", "archived", "deleted"]],
      ["unit_price", "Unit price", "number", true],
      ["currency", "Currency", "select", true, ["USD", "RUB"]],
      ["lms_course_ref", "LMS course ref", "text", false],
    ],
  },
  deals: {
    title: "Deals",
    singular: "Deal",
    path: "/deals/",
    canWrite: ["manager", "director"],
    canDelete: [],
    fields: [
      ["status", "Status", "select", false, ["open", "won", "lost", "archived"]],
      ["expected_value", "Expected value", "number", false],
      ["expected_close_date", "Expected close date", "date", false],
      ["description", "Description", "textarea", false],
      ["loss_reason", "Loss reason", "text", false],
      ["account", "Account UUID", "text", true],
      ["owner", "Owner UUID", "text", false],
      ["contract", "Contract UUID", "text", false],
      ["primary_contact", "Primary contact UUID", "text", false],
    ],
  },
  contracts: {
    title: "Contracts",
    singular: "Contract",
    path: "/contracts/",
    canWrite: [],
    canDelete: [],
    readonly: true,
    fields: [],
  },
  users: {
    title: "Users",
    singular: "User",
    path: "/users/",
    canWrite: ["director"],
    canDelete: ["director"],
    fields: [
      ["email", "Email", "email", false],
      ["username", "Username", "text", true],
      ["password", "Password", "password", false, null, { createOnly: true }],
    ],
  },
  me: {
    title: "Me",
    singular: "Profile",
    path: "/users/me/",
    canWrite: ["manager", "director", "analyst"],
    canDelete: ["director"],
    singleton: true,
    fields: [
      ["email", "Email", "email", false],
    ],
  },
  role: {
    title: "Roles",
    singular: "Role",
    path: "/role/",
    canWrite: ["director"],
    readonly: true,
    isRoleManager: true,
    fields: [],
  },
  auth: {
    title: "Auth",
    singular: "Auth",
    path: "",
    canWrite: [],
    readonly: true,
    isAuthPanel: true,
    fields: [],
  },
  analytics: {
    title: "Analytics",
    singular: "Analytics",
    path: "",
    canWrite: [],
    canDelete: [],
    readonly: true,
    fields: [],
    isAnalytics: true,
  },
};

const emptyValues = Object.fromEntries(
  Object.entries(resources).flatMap(([key, res]) =>
    res.fields.map(([name]) => [`${key}.${name}`, ""])
  )
);

function tokenFromStorage() {
  return localStorage.getItem("crm_access_token") || "";
}

function refreshTokenFromStorage() {
  return localStorage.getItem("crm_refresh_token") || "";
}

function roleFromStorage() {
  return localStorage.getItem("crm_role") || "manager";
}

function normalizeList(payload) {
  if (Array.isArray(payload)) return { items: payload, count: payload.length, next: null, previous: null };
  return {
    items: payload?.results || payload?.items || [],
    count: payload?.count || payload?.total || 0,
    next: payload?.next || null,
    previous: payload?.previous || null,
  };
}

function pickPreview(item) {
  if (!item) return "";
  if (item.name) return item.name;
  if (item.email) return item.email;
  if (item.username) return item.username;
  if (item.expected_value) return `${item.expected_value} · ${item.status || "deal"}`;
  return item.id || "Item";
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "—";
  if (Array.isArray(value)) return `${value.length} item(s)`;
  if (typeof value === "object") return value.id || JSON.stringify(value);
  return String(value);
}

function extractNumber(payload) {
  if (typeof payload === "number") return payload;
  if (typeof payload === "string" && !Number.isNaN(Number(payload))) return Number(payload);
  if (!payload || typeof payload !== "object") return 0;

  const preferredKeys = ["value", "total", "amount", "revenue", "rate", "conversion_rate", "count"];
  for (const key of preferredKeys) {
    if (payload[key] !== undefined && !Number.isNaN(Number(payload[key]))) return Number(payload[key]);
  }

  const firstNumeric = Object.values(payload).find((value) => !Number.isNaN(Number(value)));
  return firstNumeric === undefined ? 0 : Number(firstNumeric);
}

function money(value) {
  const number = Number(value || 0);
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(number);
}

function percent(value) {
  const number = Number(value || 0);
  const normalized = number <= 1 ? number * 100 : number;
  return `${normalized.toFixed(1)}%`;
}

function normalizePopularCourses(payload) {
  if (!payload) return [];

  const raw = Array.isArray(payload)
    ? payload
    : payload.results ||
      payload.items ||
      payload.courses ||
      payload.popular_courses ||
      payload.popularCourses ||
      payload.data ||
      payload.value ||
      payload.values ||
      payload.top ||
      payload.top_courses ||
      null;

  if (Array.isArray(raw)) {
    return raw
      .map((item, index) => {
        if (typeof item === "string") return { name: item, value: 1 };

        if (Array.isArray(item)) {
          return {
            name: String(item[0] ?? `Course ${index + 1}`),
            value: Number(item[1] ?? 0),
          };
        }

        return {
          name:
            item.name ||
            item.course_name ||
            item.course__name ||
            item.course_title ||
            item.title ||
            item.course ||
            item.product ||
            item.product_name ||
            `Course ${index + 1}`,
          value: Number(
            item.value ??
              item.count ??
              item.total ??
              item.quantity ??
              item.sold ??
              item.sales ??
              item.students ??
              item.orders ??
              item.deals ??
              0
          ),
        };
      })
      .filter((row) => row.name && !Number.isNaN(row.value));
  }

  if (raw && typeof raw === "object") {
    return Object.entries(raw)
      .map(([name, value]) => ({ name, value: Number(value) }))
      .filter((row) => row.name && !Number.isNaN(row.value));
  }

  if (typeof payload === "object") {
    return Object.entries(payload)
      .filter(([, value]) => typeof value === "number" || !Number.isNaN(Number(value)))
      .map(([name, value]) => ({ name, value: Number(value) }));
  }

  return [];
}

function BarChart({ rows }) {
  const max = Math.max(...rows.map((row) => row.value), 1);
  return (
    <div className="space-y-3">
      {rows.map((row) => (
        <div key={row.name}>
          <div className="mb-1 flex justify-between gap-3 text-xs">
            <span className="truncate text-slate-600">{row.name}</span>
            <span className="font-medium text-slate-900">{money(row.value)}</span>
          </div>
          <div className="h-3 overflow-hidden rounded-full bg-slate-100">
            <div className="h-full rounded-full bg-slate-900" style={{ width: `${Math.max(4, (row.value / max) * 100)}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

function Donut({ value, label }) {
  const normalized = Math.max(0, Math.min(100, Number(value || 0) <= 1 ? Number(value || 0) * 100 : Number(value || 0)));
  const radius = 42;
  const stroke = 12;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (normalized / 100) * circumference;

  return (
    <div className="flex items-center gap-4">
      <svg width="116" height="116" viewBox="0 0 116 116" className="shrink-0 -rotate-90">
        <circle cx="58" cy="58" r={radius} fill="none" stroke="currentColor" strokeWidth={stroke} className="text-slate-100" />
        <circle
          cx="58"
          cy="58"
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="text-slate-900"
        />
      </svg>
      <div>
        <div className="text-3xl font-semibold">{normalized.toFixed(1)}%</div>
        <div className="text-sm text-slate-500">{label}</div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, hint }) {
  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <div className="text-sm text-slate-500">{title}</div>
      <div className="mt-2 text-3xl font-semibold tracking-tight">{value}</div>
      {hint && <div className="mt-1 text-xs text-slate-400">{hint}</div>}
    </div>
  );
}

function FieldInput({ field, active, value, disabled, onChange }) {
  const [name, label, type, required, options] = field;

  return (
    <label className={type === "textarea" ? "md:col-span-2" : ""}>
      <span className="mb-1 block text-xs font-medium text-slate-600">{label}{required ? " *" : ""}</span>
      {type === "select" ? (
        <select
          className="w-full rounded-lg border px-3 py-2"
          value={value}
          onChange={(e) => onChange(name, e.target.value)}
          disabled={disabled}
        >
          <option value="">Select...</option>
          {options.map((option) => <option key={option} value={option}>{option}</option>)}
        </select>
      ) : type === "textarea" ? (
        <textarea
          className="min-h-24 w-full rounded-lg border px-3 py-2"
          value={value}
          onChange={(e) => onChange(name, e.target.value)}
          disabled={disabled}
        />
      ) : (
        <input
          className="w-full rounded-lg border px-3 py-2"
          type={type}
          value={value}
          onChange={(e) => onChange(name, e.target.value)}
          disabled={disabled}
          autoComplete={type === "password" ? "new-password" : undefined}
        />
      )}
    </label>
  );
}

export default function App() {
  const [token, setToken] = useState(tokenFromStorage);
  const [refreshToken, setRefreshToken] = useState(refreshTokenFromStorage);
  const [role, setRole] = useState(roleFromStorage);
  const [active, setActive] = useState("accounts");
  const [data, setData] = useState({ items: [], count: 0, next: null, previous: null });
  const [analytics, setAnalytics] = useState(null);
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState(emptyValues);
  const [login, setLogin] = useState({ username: "", password: "" });
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const resource = resources[active];
  const canWrite = resource.canWrite.includes(role);
  const canDelete = resource.canDelete?.includes(role);

  const headers = useMemo(() => {
    const h = { "Content-Type": "application/json" };
    if (token) h.Authorization = `${AUTH_HEADER_PREFIX} ${token}`;
    return h;
  }, [token]);

  async function parseResponse(response) {
    let payload = null;
    const text = await response.text();
    if (text) {
      try {
        payload = JSON.parse(text);
      } catch {
        payload = text;
      }
    }
    return payload;
  }

  async function refreshAccessToken() {
    const storedRefresh = refreshToken || refreshTokenFromStorage();
    if (!storedRefresh) return "";

    const response = await fetch(`${API_BASE}/auth/jwt/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: storedRefresh }),
    });

    const payload = await parseResponse(response);
    if (!response.ok || !payload?.access) {
      localStorage.removeItem("crm_access_token");
      localStorage.removeItem("crm_refresh_token");
      setToken("");
      setRefreshToken("");
      throw new Error("Session expired. Please sign in again.");
    }

    localStorage.setItem("crm_access_token", payload.access);
    setToken(payload.access);
    return payload.access;
  }

  async function request(path, options = {}, retry = true) {
    setError("");
    setNotice("");

    const currentToken = localStorage.getItem("crm_access_token") || token;
    const requestHeaders = { "Content-Type": "application/json", ...(options.headers || {}) };
    if (currentToken && !requestHeaders.Authorization) requestHeaders.Authorization = `${AUTH_HEADER_PREFIX} ${currentToken}`;

    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: requestHeaders,
    });

    const payload = await parseResponse(response);

    if (response.status === 401 && retry && path !== "/auth/jwt/create/" && path !== "/auth/jwt/refresh/") {
      const newAccess = await refreshAccessToken();
      return request(path, {
        ...options,
        headers: {
          ...(options.headers || {}),
          Authorization: `${AUTH_HEADER_PREFIX} ${newAccess}`,
        },
      }, false);
    }

    if (!response.ok) {
      const message = typeof payload === "string" ? payload : JSON.stringify(payload, null, 2);
      throw new Error(message || `HTTP ${response.status}`);
    }
    return payload;
  }

  async function signIn(event) {
    event.preventDefault();
    setLoading(true);
    try {
      const payload = await request("/auth/jwt/create/", {
        method: "POST",
        body: JSON.stringify(login),
      });
      const access = payload.access || payload.token || "";
      const refresh = payload.refresh || "";
      if (!access) throw new Error("Access token was not returned by backend");
      if (!refresh) throw new Error("Refresh token was not returned by backend");
      localStorage.setItem("crm_access_token", access);
      localStorage.setItem("crm_refresh_token", refresh);
      localStorage.setItem("crm_role", role);
      setToken(access);
      setRefreshToken(refresh);
      setNotice("Signed in");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  function signOut() {
    localStorage.removeItem("crm_access_token");
    localStorage.removeItem("crm_refresh_token");
    setToken("");
    setRefreshToken("");
    setSelected(null);
    setData({ items: [], count: 0, next: null, previous: null });
  }

  async function loadAnalytics() {
    if (!token) return;
    setLoading(true);
    try {
      const entries = await Promise.all(
        Object.entries(analyticsEndpoints).map(async ([key, path]) => [key, await request(path)])
      );
      setAnalytics(Object.fromEntries(entries));
      setSelected(null);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadMe() {
    if (!token) return;
    setLoading(true);
    try {
      const payload = await request("/users/me/");
      setData({ items: payload ? [payload] : [], count: payload ? 1 : 0, next: null, previous: null });
      setSelected(payload || null);
      if (payload) fillForm(payload, "me");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function load() {
    if (!token) return;
    if (resource.isAnalytics) return loadAnalytics();
    if (resource.isAuthPanel || resource.isRoleManager) return;
    if (resource.singleton) return loadMe();

    setLoading(true);
    try {
      const payload = await request(`${resource.path}?page=${page}&size=${size}`);
      setData(normalizeList(payload || []));
      setSelected(null);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [active, page, size, token]);

  function changeField(name, value) {
    setForm((old) => ({ ...old, [`${active}.${name}`]: value }));
  }

  function currentPayload() {
    const payload = {};
    for (const [name, , type, , , meta] of resource.fields) {
      if (meta?.createOnly && selected?.id) continue;
      const value = form[`${active}.${name}`];
      if (value === "") continue;
      payload[name] = type === "number" ? Number(value) : value;
    }
    return payload;
  }

  function fillForm(item, resourceKey = active) {
    setSelected(item);
    const target = resources[resourceKey];
    setForm((old) => {
      const next = { ...old };
      for (const [name] of target.fields) next[`${resourceKey}.${name}`] = item[name] ?? "";
      return next;
    });
  }

  function clearForm() {
    setSelected(null);
    setForm((old) => {
      const next = { ...old };
      for (const [name] of resource.fields) next[`${active}.${name}`] = "";
      return next;
    });
  }

  async function save(event) {
    event.preventDefault();
    if (!canWrite) return;
    setLoading(true);
    try {
      const isEdit = Boolean(selected?.id) || resource.singleton;
      const path = resource.singleton ? resource.path : isEdit ? `${resource.path}${selected.id}/` : resource.path;
      await request(path, {
        method: isEdit ? "PATCH" : "POST",
        body: JSON.stringify(currentPayload()),
      });
      setNotice(isEdit ? "Updated" : "Created");
      clearForm();
      await load();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function destroyItem(item) {
    if (!canDelete) return;
    if (!window.confirm(`Delete ${pickPreview(item)}?`)) return;
    setLoading(true);
    try {
      const path = resource.singleton ? resource.path : `${resource.path}${item.id}/`;
      await request(path, { method: "DELETE" });
      setNotice("Deleted");
      clearForm();
      await load();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function action(item, actionName, body = null) {
    setLoading(true);
    try {
      await request(`${resource.path}${item.id}/${actionName}/`, {
        method: "POST",
        body: body ? JSON.stringify(body) : undefined,
      });
      setNotice(`${actionName} done`);
      await load();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function closeDeal(item, status) {
    const loss_reason = status === "lost" ? window.prompt("Loss reason?", "") : undefined;
    await action(item, "close", { status, loss_reason });
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <div>
            <h1 className="text-lg font-semibold">Minimal CRM</h1>
            <p className="text-xs text-slate-500">Django REST API frontend</p>
          </div>
          {token && (
            <div className="flex items-center gap-2">
              <select
                className="rounded-lg border px-2 py-1 text-sm"
                value={role}
                onChange={(e) => {
                  setRole(e.target.value);
                  localStorage.setItem("crm_role", e.target.value);
                }}
              >
                <option value="director">director</option>
                <option value="manager">manager</option>
                <option value="analyst">analyst</option>
              </select>
              <button className="rounded-lg border px-3 py-1 text-sm" onClick={signOut}>Logout</button>
            </div>
          )}
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">
        {!token ? (
          <LoginPanel
            login={login}
            setLogin={setLogin}
            role={role}
            setRole={setRole}
            loading={loading}
            error={error}
            notice={notice}
            onSubmit={signIn}
          />
        ) : (
          <div className="grid gap-4 lg:grid-cols-[220px_1fr]">
            <aside className="rounded-2xl border bg-white p-3 shadow-sm">
              {Object.entries(resources).map(([key, value]) => (
                <button
                  key={key}
                  className={`mb-1 w-full rounded-xl px-3 py-2 text-left text-sm ${active === key ? "bg-slate-900 text-white" : "hover:bg-slate-100"}`}
                  onClick={() => {
                    setActive(key);
                    setPage(1);
                    clearForm();
                  }}
                >
                  {value.title}
                </button>
              ))}
            </aside>

            <section className="space-y-4">
              {resource.isAnalytics ? (
                <AnalyticsPanel analytics={analytics} loading={loading} error={error} notice={notice} onRefresh={loadAnalytics} />
              ) : resource.isAuthPanel ? (
                <AuthPanel
                  loading={loading}
                  error={error}
                  notice={notice}
                  token={token}
                  refreshToken={refreshToken}
                  request={request}
                  refreshAccessToken={refreshAccessToken}
                  setLoading={setLoading}
                  setError={setError}
                  setNotice={setNotice}
                />
              ) : resource.isRoleManager ? (
                <RolePanel
                  loading={loading}
                  error={error}
                  notice={notice}
                  canWrite={canWrite}
                  request={request}
                  setLoading={setLoading}
                  setError={setError}
                  setNotice={setNotice}
                />
              ) : (
                <>
                  <ListPanel
                    active={active}
                    resource={resource}
                    role={role}
                    data={data}
                    page={page}
                    size={size}
                    setPage={setPage}
                    setSize={setSize}
                    loading={loading}
                    error={error}
                    notice={notice}
                    canWrite={canWrite}
                    canDelete={canDelete}
                    onRefresh={load}
                    onOpen={fillForm}
                    onDelete={destroyItem}
                    onAction={action}
                    onCloseDeal={closeDeal}
                  />

                  {!resource.readonly && (
                    <form onSubmit={save} className="rounded-2xl border bg-white p-4 shadow-sm">
                      <div className="mb-4 flex items-center justify-between">
                        <h3 className="text-base font-semibold">{selected ? "Edit" : "Create"} {resource.singular}</h3>
                        <button type="button" className="rounded-lg border px-3 py-1 text-sm" onClick={clearForm}>Clear</button>
                      </div>

                      {!canWrite && <div className="mb-3 rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-700">Read-only for {role} role</div>}

                      <div className="grid gap-3 md:grid-cols-2">
                        {resource.fields
                          .filter(([, , , , , meta]) => !(meta?.createOnly && selected?.id))
                          .map((field) => (
                            <FieldInput
                              key={field[0]}
                              field={field}
                              active={active}
                              value={form[`${active}.${field[0]}`]}
                              disabled={!canWrite}
                              onChange={changeField}
                            />
                          ))}
                      </div>

                      <button className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-40" disabled={!canWrite || loading}>
                        {selected ? "Save changes" : "Create"}
                      </button>
                    </form>
                  )}

                  {active === "deals" && selected && canWrite && (
                    <DealItemsPanel
                      deal={selected}
                      request={request}
                      onReload={load}
                      setLoading={setLoading}
                      setError={setError}
                      setNotice={setNotice}
                    />
                  )}

                  {selected && (
                    <details className="rounded-2xl border bg-white p-4 shadow-sm" open>
                      <summary className="cursor-pointer font-semibold">Raw selected object</summary>
                      <pre className="mt-3 overflow-auto rounded-xl bg-slate-950 p-3 text-xs text-slate-50">{JSON.stringify(selected, null, 2)}</pre>
                    </details>
                  )}
                </>
              )}
            </section>
          </div>
        )}
      </main>
    </div>
  );
}

function LoginPanel({ login, setLogin, role, setRole, loading, error, notice, onSubmit }) {
  return (
    <section className="mx-auto max-w-sm rounded-2xl border bg-white p-5 shadow-sm">
      <h2 className="mb-4 text-base font-semibold">Login</h2>
      {notice && <div className="mb-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
      {error && <pre className="mb-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}
      <form onSubmit={onSubmit} className="space-y-3">
        <input
          className="w-full rounded-lg border px-3 py-2"
          placeholder="Username"
          value={login.username}
          onChange={(e) => setLogin({ ...login, username: e.target.value })}
        />
        <input
          className="w-full rounded-lg border px-3 py-2"
          placeholder="Password"
          type="password"
          value={login.password}
          onChange={(e) => setLogin({ ...login, password: e.target.value })}
        />
        <select
          className="w-full rounded-lg border px-3 py-2"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          <option value="manager">manager</option>
          <option value="director">director</option>
          <option value="analyst">analyst</option>
        </select>
        <button className="w-full rounded-lg bg-slate-900 px-3 py-2 text-white" disabled={loading}>
          {loading ? "Loading..." : "Sign in"}
        </button>
      </form>
    </section>
  );
}

function ListPanel({
  active,
  resource,
  role,
  data,
  page,
  size,
  setPage,
  setSize,
  loading,
  error,
  notice,
  canWrite,
  canDelete,
  onRefresh,
  onOpen,
  onDelete,
  onAction,
  onCloseDeal,
}) {
  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="text-base font-semibold">{resource.title}</h2>
          <p className="text-xs text-slate-500">{data.count} total · role: {role}</p>
        </div>
        {!resource.singleton && (
          <div className="flex items-center gap-2">
            <select className="rounded-lg border px-2 py-1 text-sm" value={size} onChange={(e) => setSize(Number(e.target.value))}>
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={50}>50</option>
            </select>
            <button className="rounded-lg border px-3 py-1 text-sm" onClick={onRefresh} disabled={loading}>Refresh</button>
          </div>
        )}
      </div>

      {notice && <div className="mb-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
      {error && <pre className="mb-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b text-xs uppercase text-slate-500">
              <th className="py-2">Main</th>
              <th className="py-2">Status</th>
              <th className="py-2">Updated</th>
              <th className="py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((item) => (
              <tr key={item.id || item.email || "me"} className="border-b last:border-0">
                <td className="py-2">
                  <button className="font-medium hover:underline" onClick={() => onOpen(item)}>
                    {pickPreview(item)}
                  </button>
                  <div className="text-xs text-slate-500">{item.id || "—"}</div>
                </td>
                <td className="py-2">{formatValue(item.status || item.account_type || item.currency || item.username)}</td>
                <td className="py-2">{formatValue(item.updated_at || item.created_at)}</td>
                <td className="py-2">
                  <div className="flex flex-wrap gap-1">
                    <button className="rounded border px-2 py-1 text-xs" onClick={() => onOpen(item)}>Open</button>
                    {active === "courses" && canWrite && item.status === "active" && (
                      <button className="rounded border px-2 py-1 text-xs" onClick={() => onAction(item, "archive")}>Archive</button>
                    )}
                    {active === "courses" && canWrite && item.status === "archived" && (
                      <button className="rounded border px-2 py-1 text-xs" onClick={() => onAction(item, "activate")}>Activate</button>
                    )}
                    {active === "deals" && canWrite && item.status === "open" && (
                      <>
                        <button className="rounded border px-2 py-1 text-xs" onClick={() => onCloseDeal(item, "won")}>Won</button>
                        <button className="rounded border px-2 py-1 text-xs" onClick={() => onCloseDeal(item, "lost")}>Lost</button>
                      </>
                    )}
                    {canDelete && (
                      <button className="rounded border px-2 py-1 text-xs text-red-700" onClick={() => onDelete(item)}>Delete</button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {!data.items.length && (
              <tr>
                <td className="py-8 text-center text-sm text-slate-500" colSpan={4}>
                  {loading ? "Loading..." : "No data"}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {!resource.singleton && (
        <div className="mt-4 flex items-center justify-between text-sm">
          <button className="rounded-lg border px-3 py-1 disabled:opacity-40" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>Prev</button>
          <span>Page {page}</span>
          <button className="rounded-lg border px-3 py-1 disabled:opacity-40" disabled={!data.next && data.items.length < size} onClick={() => setPage((p) => p + 1)}>Next</button>
        </div>
      )}
    </div>
  );
}

function DealItemsPanel({ deal, request, onReload, setLoading, setError, setNotice }) {
  const [item, setItem] = useState({ course: "", quantity: "1" });
  const [diId, setDiId] = useState("");

  async function addDealItem(event) {
    event.preventDefault();
    setLoading(true);
    try {
      await request(`/deals/${deal.id}/items/`, {
        method: "POST",
        body: JSON.stringify({ course: item.course, quantity: Number(item.quantity || 0) }),
      });
      setNotice("Deal item added");
      setItem({ course: "", quantity: "1" });
      await onReload();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function updateDealItem(event) {
    event.preventDefault();
    if (!diId) return;
    setLoading(true);
    try {
      await request(`/deals/${deal.id}/items/${diId}/`, {
        method: "PUT",
        body: JSON.stringify({ course: item.course, quantity: Number(item.quantity || 0) }),
      });
      setNotice("Deal item updated");
      await onReload();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function removeDealItem() {
    if (!diId) return;
    if (!window.confirm("Remove this deal item?")) return;
    setLoading(true);
    try {
      await request(`/deals/${deal.id}/items/${diId}/`, { method: "POST" });
      setNotice("Deal item removed");
      setDiId("");
      await onReload();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <h3 className="mb-4 text-base font-semibold">Deal items</h3>
      <form onSubmit={addDealItem} className="grid gap-3 md:grid-cols-[1fr_140px_auto]">
        <input
          className="rounded-lg border px-3 py-2"
          placeholder="Course UUID"
          value={item.course}
          onChange={(e) => setItem({ ...item, course: e.target.value })}
        />
        <input
          className="rounded-lg border px-3 py-2"
          type="number"
          min="0"
          placeholder="Quantity"
          value={item.quantity}
          onChange={(e) => setItem({ ...item, quantity: e.target.value })}
        />
        <button className="rounded-lg bg-slate-900 px-4 py-2 text-white">Add item</button>
      </form>

      <form onSubmit={updateDealItem} className="mt-3 grid gap-3 md:grid-cols-[1fr_1fr_140px_auto_auto]">
        <input
          className="rounded-lg border px-3 py-2"
          placeholder="Deal item ID"
          value={diId}
          onChange={(e) => setDiId(e.target.value)}
        />
        <input
          className="rounded-lg border px-3 py-2"
          placeholder="Course UUID"
          value={item.course}
          onChange={(e) => setItem({ ...item, course: e.target.value })}
        />
        <input
          className="rounded-lg border px-3 py-2"
          type="number"
          min="0"
          placeholder="Quantity"
          value={item.quantity}
          onChange={(e) => setItem({ ...item, quantity: e.target.value })}
        />
        <button className="rounded-lg border px-4 py-2">Update</button>
        <button type="button" className="rounded-lg border px-4 py-2 text-red-700" onClick={removeDealItem}>Remove</button>
      </form>
      <p className="mt-2 text-xs text-slate-500">Remove uses POST /deals/{'{id}'}/items/{'{di_id}'}/ according to the OpenAPI spec.</p>
    </div>
  );
}

function RolePanel({ loading, error, notice, canWrite, request, setLoading, setError, setNotice }) {
  const [userId, setUserId] = useState("");
  const [role, setRole] = useState("manager");

  async function setUserRole(event) {
    event.preventDefault();
    if (!canWrite) return;
    setLoading(true);
    try {
      await request(`/${userId}/role/`, {
        method: "PUT",
        body: JSON.stringify({ role }),
      });
      setNotice("Role updated");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function revokeUserRole() {
    if (!canWrite || !userId) return;
    if (!window.confirm("Revoke role for this user?")) return;
    setLoading(true);
    try {
      await request(`/${userId}/role/`, { method: "DELETE" });
      setNotice("Role revoked");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold">Roles</h2>
      <p className="mb-4 text-xs text-slate-500">PUT/DELETE /api/v1/{'{user_id}'}/role/</p>
      {notice && <div className="mb-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
      {error && <pre className="mb-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}
      {!canWrite && <div className="mb-3 rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-700">Only director can manage roles</div>}
      <form onSubmit={setUserRole} className="grid gap-3 md:grid-cols-[1fr_180px_auto_auto]">
        <input
          className="rounded-lg border px-3 py-2"
          placeholder="User UUID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          disabled={!canWrite}
        />
        <input
          className="rounded-lg border px-3 py-2"
          placeholder="Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          disabled={!canWrite}
        />
        <button className="rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-40" disabled={!canWrite || loading}>Set role</button>
        <button type="button" className="rounded-lg border px-4 py-2 text-red-700 disabled:opacity-40" disabled={!canWrite || loading} onClick={revokeUserRole}>Revoke</button>
      </form>
    </div>
  );
}

function AuthPanel({ loading, error, notice, token, refreshToken, request, refreshAccessToken, setLoading, setError, setNotice }) {
  const [activation, setActivation] = useState({ uid: "", token: "" });
  const [email, setEmail] = useState("");
  const [passwordReset, setPasswordReset] = useState({ uid: "", token: "", new_password: "" });
  const [usernameReset, setUsernameReset] = useState({ new_username: "" });
  const [setPassword, setSetPassword] = useState({ current_password: "", new_password: "" });
  const [setUsername, setSetUsername] = useState({ current_password: "", new_username: "" });
  const [verifyResult, setVerifyResult] = useState("");

  async function runAuthAction(label, path, body) {
    setLoading(true);
    try {
      const payload = await request(path, { method: "POST", body: JSON.stringify(body) });
      setNotice(label);
      setVerifyResult(JSON.stringify(payload || { ok: true }, null, 2));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function verifyAccessToken() {
    await runAuthAction("Access token verified", "/auth/jwt/verify/", { token });
  }

  async function refreshNow() {
    setLoading(true);
    try {
      const access = await refreshAccessToken();
      setNotice("Access token refreshed");
      setVerifyResult(JSON.stringify({ access }, null, 2));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="rounded-2xl border bg-white p-4 shadow-sm">
        <h2 className="text-base font-semibold">Auth endpoints</h2>
        <p className="text-xs text-slate-500">JWT verify/refresh plus Djoser user auth endpoints.</p>
        {notice && <div className="mt-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
        {error && <pre className="mt-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">JWT</h3>
          <div className="flex flex-wrap gap-2">
            <button className="rounded-lg border px-3 py-2 text-sm" onClick={verifyAccessToken} disabled={loading || !token}>Verify access</button>
            <button className="rounded-lg border px-3 py-2 text-sm" onClick={refreshNow} disabled={loading || !refreshToken}>Refresh access</button>
          </div>
          {verifyResult && <pre className="mt-3 overflow-auto rounded-xl bg-slate-950 p-3 text-xs text-slate-50">{verifyResult}</pre>}
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">Activation</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" placeholder="uid" value={activation.uid} onChange={(e) => setActivation({ ...activation, uid: e.target.value })} />
            <input className="rounded-lg border px-3 py-2" placeholder="token" value={activation.token} onChange={(e) => setActivation({ ...activation, token: e.target.value })} />
            <button className="rounded-lg bg-slate-900 px-3 py-2 text-white" disabled={loading} onClick={() => runAuthAction("User activated", "/users/activation/", activation)}>Activate</button>
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">Email flows</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction("Activation email resent", "/users/resend_activation/", { email })}>Resend activation</button>
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction("Password reset email sent", "/users/reset_password/", { email })}>Reset password email</button>
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction("Username reset email sent", "/users/reset_username/", { email })}>Reset username email</button>
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">Confirm password reset</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" placeholder="uid" value={passwordReset.uid} onChange={(e) => setPasswordReset({ ...passwordReset, uid: e.target.value })} />
            <input className="rounded-lg border px-3 py-2" placeholder="token" value={passwordReset.token} onChange={(e) => setPasswordReset({ ...passwordReset, token: e.target.value })} />
            <input className="rounded-lg border px-3 py-2" type="password" placeholder="new password" value={passwordReset.new_password} onChange={(e) => setPasswordReset({ ...passwordReset, new_password: e.target.value })} />
            <button className="rounded-lg bg-slate-900 px-3 py-2 text-white" disabled={loading} onClick={() => runAuthAction("Password reset confirmed", "/users/reset_password_confirm/", passwordReset)}>Confirm</button>
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">Confirm username reset</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" placeholder="new username" value={usernameReset.new_username} onChange={(e) => setUsernameReset({ new_username: e.target.value })} />
            <button className="rounded-lg bg-slate-900 px-3 py-2 text-white" disabled={loading} onClick={() => runAuthAction("Username reset confirmed", "/users/reset_username_confirm/", usernameReset)}>Confirm</button>
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">Set current user credentials</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" type="password" placeholder="current password" value={setPassword.current_password} onChange={(e) => setSetPassword({ ...setPassword, current_password: e.target.value })} />
            <input className="rounded-lg border px-3 py-2" type="password" placeholder="new password" value={setPassword.new_password} onChange={(e) => setSetPassword({ ...setPassword, new_password: e.target.value })} />
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction("Password changed", "/users/set_password/", setPassword)}>Set password</button>
            <input className="rounded-lg border px-3 py-2" type="password" placeholder="current password" value={setUsername.current_password} onChange={(e) => setSetUsername({ ...setUsername, current_password: e.target.value })} />
            <input className="rounded-lg border px-3 py-2" placeholder="new username" value={setUsername.new_username} onChange={(e) => setSetUsername({ ...setUsername, new_username: e.target.value })} />
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction("Username changed", "/users/set_username/", setUsername)}>Set username</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function AnalyticsPanel({ analytics, loading, error, notice, onRefresh }) {
  const leadRate = extractNumber(analytics?.leadCustomerConversionRate);
  const wonRate = extractNumber(analytics?.dealWonConversionRate);
  const pipeline = extractNumber(analytics?.totalPipelineValue);
  const totalRevenue = extractNumber(analytics?.totalRevenue);
  const lastMonthRevenue = extractNumber(analytics?.lastMonthRevenue);
  const popularCourses = normalizePopularCourses(analytics?.popularCourses).slice(0, 8);
  const summary = analytics?.summary && typeof analytics.summary === "object" ? analytics.summary : null;

  return (
    <div className="space-y-4">
      <div className="rounded-2xl border bg-white p-4 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 className="text-base font-semibold">Analytics</h2>
            <p className="text-xs text-slate-500">Live metrics from ORM endpoints</p>
          </div>
          <button className="rounded-lg border px-3 py-1 text-sm" onClick={onRefresh} disabled={loading}>
            {loading ? "Loading..." : "Refresh"}
          </button>
        </div>
        {notice && <div className="mt-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
        {error && <pre className="mt-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard title="Pipeline value" value={money(pipeline)} hint="Open pipeline total" />
        <MetricCard title="Total revenue" value={money(totalRevenue)} hint="All-time revenue" />
        <MetricCard title="Last month revenue" value={money(lastMonthRevenue)} hint="New revenue for last month" />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <h3 className="mb-4 text-sm font-semibold">Lead → Customer</h3>
          <Donut value={leadRate} label="conversion rate" />
        </div>
        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <h3 className="mb-4 text-sm font-semibold">Deal → Won</h3>
          <Donut value={wonRate} label="conversion rate" />
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-sm font-semibold">Popular courses</h3>
            <span className="text-xs text-slate-400">Top {popularCourses.length}</span>
          </div>
          {popularCourses.length ? (
            <BarChart rows={popularCourses} />
          ) : (
            <div className="rounded-xl bg-slate-50 p-6 text-center text-sm text-slate-500">No course data</div>
          )}
        </div>

        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <h3 className="mb-4 text-sm font-semibold">Summary</h3>
          {summary ? (
            <div className="space-y-2">
              {Object.entries(summary).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between gap-3 rounded-xl bg-slate-50 px-3 py-2 text-sm">
                  <span className="text-slate-500">{key.replaceAll("_", " ")}</span>
                  <span className="font-medium">{formatValue(value)}</span>
                </div>
              ))}
            </div>
          ) : (
            <pre className="overflow-auto rounded-xl bg-slate-950 p-3 text-xs text-slate-50">{JSON.stringify(analytics?.summary || {}, null, 2)}</pre>
          )}
        </div>
      </div>
    </div>
  );
}
