import React, { useEffect, useMemo, useState } from "react";

const API_BASE = "/api/v1";

const resources = {
  accounts: {
    title: "Accounts",
    path: "/accounts/",
    canWrite: ["manager", "director"],
    fields: [
      ["name", "Name", "text", true],
      ["account_type", "Type", "select", true, ["SCHOOL", "UNIVERSITY", "COMPANY", "OTHER"]],
      ["status", "Status", "select", true, ["new", "active", "customer", "lead"]],
      ["country", "Country", "text", false],
      ["city", "City", "text", false],
      ["address", "Address", "text", false],
      ["description", "Description", "textarea", false],
    ],
  },
  contacts: {
    title: "Contacts",
    path: "/contacts/",
    canWrite: ["manager", "director"],
    fields: [
      ["first_name", "First name", "text", true],
      ["last_name", "Last name", "text", false],
      ["email", "Email", "email", true],
      ["phone", "Phone", "text", false],
      ["account", "Account UUID", "text", false],
    ],
  },
  courses: {
    title: "Courses",
    path: "/courses/",
    canWrite: ["manager", "director"],
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
    path: "/deals/",
    canWrite: ["manager", "director"],
    fields: [
      ["status", "Status", "select", false, ["open", "won", "lost", "archived"]],
      ["expected_value", "Expected value", "number", true],
      ["expected_close_date", "Expected close date", "date", true],
      ["description", "Description", "textarea", false],
      ["loss_reason", "Loss reason", "text", false],
      ["account", "Account UUID", "text", true],
      ["owner", "Owner UUID", "text", false],
      ["primary_contact", "Primary contact UUID", "text", false],
    ],
  },
  contracts: {
    title: "Contracts",
    path: "/contracts/",
    canWrite: [],
    readonly: true,
    fields: [],
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

function roleFromStorage() {
  return localStorage.getItem("crm_role") || "manager";
}

function normalizeList(payload) {
  if (Array.isArray(payload)) return { items: payload, count: payload.length, next: null, previous: null };
  return {
    items: payload.results || payload.items || [],
    count: payload.count || payload.total || 0,
    next: payload.next || null,
    previous: payload.previous || null,
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

export default function App() {
  const [token, setToken] = useState(tokenFromStorage);
  const [role, setRole] = useState(roleFromStorage);
  const [active, setActive] = useState("accounts");
  const [data, setData] = useState({ items: [], count: 0, next: null, previous: null });
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

  const headers = useMemo(() => {
    const h = { "Content-Type": "application/json" };
    if (token) h.Authorization = `Bearer ${token}`;
    return h;
  }, [token]);

  async function request(path, options = {}) {
    setError("");
    setNotice("");
    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: { ...headers, ...(options.headers || {}) },
    });

    let payload = null;
    const text = await response.text();
    if (text) {
      try {
        payload = JSON.parse(text);
      } catch {
        payload = text;
      }
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
      if (!access) throw new Error("Token was not returned by backend");
      localStorage.setItem("crm_access_token", access);
      localStorage.setItem("crm_role", role);
      setToken(access);
      setNotice("Signed in");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  function signOut() {
    localStorage.removeItem("crm_access_token");
    setToken("");
    setSelected(null);
    setData({ items: [], count: 0, next: null, previous: null });
  }

  async function load() {
    if (!token) return;
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
    for (const [name, , type] of resource.fields) {
      const value = form[`${active}.${name}`];
      if (value === "") continue;
      payload[name] = type === "number" ? Number(value) : value;
    }
    return payload;
  }

  function fillForm(item) {
    setSelected(item);
    setForm((old) => {
      const next = { ...old };
      for (const [name] of resource.fields) next[`${active}.${name}`] = item[name] ?? "";
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
      const isEdit = Boolean(selected?.id);
      const path = isEdit ? `${resource.path}${selected.id}/` : resource.path;
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
    const loss_reason = status === "LOST" ? window.prompt("Loss reason?", "") : undefined;
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
          <section className="mx-auto max-w-sm rounded-2xl border bg-white p-5 shadow-sm">
            <h2 className="mb-4 text-base font-semibold">Login</h2>
            <form onSubmit={signIn} className="space-y-3">
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
              <div className="rounded-2xl border bg-white p-4 shadow-sm">
                <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <h2 className="text-base font-semibold">{resource.title}</h2>
                    <p className="text-xs text-slate-500">{data.count} total · role: {role}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <select className="rounded-lg border px-2 py-1 text-sm" value={size} onChange={(e) => setSize(Number(e.target.value))}>
                      <option value={10}>10</option>
                      <option value={20}>20</option>
                      <option value={50}>50</option>
                    </select>
                    <button className="rounded-lg border px-3 py-1 text-sm" onClick={load} disabled={loading}>Refresh</button>
                  </div>
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
                        <tr key={item.id} className="border-b last:border-0">
                          <td className="py-2">
                            <button className="font-medium hover:underline" onClick={() => fillForm(item)}>
                              {pickPreview(item)}
                            </button>
                            <div className="text-xs text-slate-500">{item.id}</div>
                          </td>
                          <td className="py-2">{formatValue(item.status || item.account_type || item.currency)}</td>
                          <td className="py-2">{formatValue(item.updated_at || item.created_at)}</td>
                          <td className="py-2">
                            <div className="flex flex-wrap gap-1">
                              <button className="rounded border px-2 py-1 text-xs" onClick={() => fillForm(item)}>Open</button>
                              {active === "courses" && canWrite && item.status === "active" && (
                                <button className="rounded border px-2 py-1 text-xs" onClick={() => action(item, "archive")}>Archive</button>
                              )}
                              {active === "courses" && canWrite && item.status === "archived" && (
                                <button className="rounded border px-2 py-1 text-xs" onClick={() => action(item, "activate")}>Activate</button>
                              )}
                              {active === "deals" && canWrite && item.status === "open" && (
                                <>
                                  <button className="rounded border px-2 py-1 text-xs" onClick={() => closeDeal(item, "won")}>Won</button>
                                  <button className="rounded border px-2 py-1 text-xs" onClick={() => closeDeal(item, "lost")}>Lost</button>
                                </>
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

                <div className="mt-4 flex items-center justify-between text-sm">
                  <button className="rounded-lg border px-3 py-1 disabled:opacity-40" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>Prev</button>
                  <span>Page {page}</span>
                  <button className="rounded-lg border px-3 py-1 disabled:opacity-40" disabled={!data.next && data.items.length < size} onClick={() => setPage((p) => p + 1)}>Next</button>
                </div>
              </div>

              {!resource.readonly && (
                <form onSubmit={save} className="rounded-2xl border bg-white p-4 shadow-sm">
                  <div className="mb-4 flex items-center justify-between">
                    <h3 className="text-base font-semibold">{selected ? "Edit" : "Create"} {resource.title.slice(0, -1)}</h3>
                    <button type="button" className="rounded-lg border px-3 py-1 text-sm" onClick={clearForm}>Clear</button>
                  </div>

                  {!canWrite && <div className="mb-3 rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-700">Read-only for analyst role</div>}

                  <div className="grid gap-3 md:grid-cols-2">
                    {resource.fields.map(([name, label, type, required, options]) => (
                      <label key={name} className={type === "textarea" ? "md:col-span-2" : ""}>
                        <span className="mb-1 block text-xs font-medium text-slate-600">{label}{required ? " *" : ""}</span>
                        {type === "select" ? (
                          <select
                            className="w-full rounded-lg border px-3 py-2"
                            value={form[`${active}.${name}`]}
                            onChange={(e) => changeField(name, e.target.value)}
                            disabled={!canWrite}
                          >
                            <option value="">Select...</option>
                            {options.map((option) => <option key={option} value={option}>{option}</option>)}
                          </select>
                        ) : type === "textarea" ? (
                          <textarea
                            className="min-h-24 w-full rounded-lg border px-3 py-2"
                            value={form[`${active}.${name}`]}
                            onChange={(e) => changeField(name, e.target.value)}
                            disabled={!canWrite}
                          />
                        ) : (
                          <input
                            className="w-full rounded-lg border px-3 py-2"
                            type={type}
                            value={form[`${active}.${name}`]}
                            onChange={(e) => changeField(name, e.target.value)}
                            disabled={!canWrite}
                          />
                        )}
                      </label>
                    ))}
                  </div>

                  <button className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-40" disabled={!canWrite || loading}>
                    {selected ? "Save changes" : "Create"}
                  </button>
                </form>
              )}

              {selected && (
                <details className="rounded-2xl border bg-white p-4 shadow-sm" open>
                  <summary className="cursor-pointer font-semibold">Raw selected object</summary>
                  <pre className="mt-3 overflow-auto rounded-xl bg-slate-950 p-3 text-xs text-slate-50">{JSON.stringify(selected, null, 2)}</pre>
                </details>
              )}
            </section>
          </div>
        )}
      </main>
    </div>
  );
}
