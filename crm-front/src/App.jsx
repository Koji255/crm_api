// AI GENERATED

import React, { useEffect, useMemo, useState } from "react";

const API_BASE = "/api/v1";
const AUTH_HEADER_PREFIX = "Bearer";
const LOCALE_STORAGE_KEY = "crm_locale";

const analyticsEndpoints = {
  leadCustomerConversionRate: "/analytics/from-lead-to-customer-conversion-rate/",
  dealWonConversionRate: "/analytics/from-deal-to-won-conversion-rate/",
  totalPipelineValue: "/analytics/total-pipeline-value/",
  totalRevenue: "/analytics/total-revenue/",
  lastMonthRevenue: "/analytics/last-month-revenue/",
  popularCourses: "/analytics/popular-courses/",
  summary: "/analytics/summary/",
};

const i18n = {
  en: {
    appTitle: "Minimal CRM",
    appSubtitle: "Django REST API frontend",
    language: "Language",
    login: "Login",
    username: "Username",
    password: "Password",
    signIn: "Sign in",
    logout: "Logout",
    loading: "Loading...",
    signedIn: "Signed in",
    sessionExpired: "Session expired. Please sign in again.",
    accessTokenMissing: "Access token was not returned by backend",
    refreshTokenMissing: "Refresh token was not returned by backend",
    selectPlaceholder: "Select...",
    total: "total",
    role: "role",
    refresh: "Refresh",
    main: "Main",
    status: "Status",
    updated: "Updated",
    actions: "Actions",
    open: "Open",
    archive: "Archive",
    activate: "Activate",
    won: "Won",
    lost: "Lost",
    delete: "Delete",
    noData: "No data",
    prev: "Prev",
    next: "Next",
    page: "Page",
    edit: "Edit",
    create: "Create",
    clear: "Clear",
    saveChanges: "Save changes",
    created: "Created",
    saved: "Updated",
    deleted: "Deleted",
    readOnlyForRole: "Read-only for {role} role",
    rawSelectedObject: "Raw selected object",
    deleteConfirm: "Delete {name}?",
    lossReason: "Loss reason?",
    actionDone: "{action} done",
    itemCount: "{count} item(s)",
    itemFallback: "Item",
    dealFallback: "deal",
    accounts: "Accounts",
    account: "Account",
    contacts: "Contacts",
    contact: "Contact",
    courses: "Courses",
    course: "Course",
    deals: "Deals",
    deal: "Deal",
    contracts: "Contracts",
    contract: "Contract",
    users: "Users",
    user: "User",
    me: "Me",
    profile: "Profile",
    roles: "Roles",
    roleSingular: "Role",
    auth: "Auth",
    analytics: "Analytics",
    fieldName: "Name",
    fieldType: "Type",
    fieldStatus: "Status",
    fieldCountry: "Country",
    fieldCity: "City",
    fieldAddress: "Address",
    fieldDescription: "Description",
    fieldFirstName: "First name",
    fieldLastName: "Last name",
    fieldEmail: "Email",
    fieldPhone: "Phone",
    fieldAccountUuid: "Account UUID",
    fieldUnitPrice: "Unit price",
    fieldCurrency: "Currency",
    fieldLmsCourseRef: "LMS course ref",
    fieldExpectedValue: "Expected value",
    fieldExpectedCloseDate: "Expected close date",
    fieldLossReason: "Loss reason",
    fieldOwnerUuid: "Owner UUID",
    fieldContractUuid: "Contract UUID",
    fieldPrimaryContactUuid: "Primary contact UUID",
    fieldUsername: "Username",
    fieldPassword: "Password",
    dealItems: "Deal items",
    courseUuid: "Course UUID",
    quantity: "Quantity",
    addItem: "Add item",
    dealItemId: "Deal item ID",
    update: "Update",
    remove: "Remove",
    dealItemAdded: "Deal item added",
    dealItemUpdated: "Deal item updated",
    dealItemRemoved: "Deal item removed",
    removeDealItemConfirm: "Remove this deal item?",
    removeDealItemHint: "Remove uses POST /deals/{id}/items/{di_id}/ according to the OpenAPI spec.",
    roleEndpointHint: "PUT/DELETE /api/v1/{user_id}/role/",
    onlyDirectorRoles: "Only director can manage roles",
    userUuid: "User UUID",
    setRole: "Set role",
    revoke: "Revoke",
    revokeRoleConfirm: "Revoke role for this user?",
    roleUpdated: "Role updated",
    roleRevoked: "Role revoked",
    authEndpoints: "Auth endpoints",
    authHint: "JWT verify/refresh plus Djoser user auth endpoints.",
    jwt: "JWT",
    verifyAccess: "Verify access",
    refreshAccess: "Refresh access",
    accessVerified: "Access token verified",
    accessRefreshed: "Access token refreshed",
    activation: "Activation",
    activateUser: "Activate",
    userActivated: "User activated",
    emailFlows: "Email flows",
    resendActivation: "Resend activation",
    resetPasswordEmail: "Reset password email",
    resetUsernameEmail: "Reset username email",
    activationEmailResent: "Activation email resent",
    passwordResetEmailSent: "Password reset email sent",
    usernameResetEmailSent: "Username reset email sent",
    confirmPasswordReset: "Confirm password reset",
    newPassword: "new password",
    confirm: "Confirm",
    passwordResetConfirmed: "Password reset confirmed",
    confirmUsernameReset: "Confirm username reset",
    newUsername: "new username",
    usernameResetConfirmed: "Username reset confirmed",
    setCurrentUserCredentials: "Set current user credentials",
    currentPassword: "current password",
    passwordChanged: "Password changed",
    usernameChanged: "Username changed",
    setPassword: "Set password",
    setUsername: "Set username",
    analyticsHint: "Live metrics from ORM endpoints",
    pipelineValue: "Pipeline value",
    openPipelineTotal: "Open pipeline total",
    totalRevenue: "Total revenue",
    allTimeRevenue: "All-time revenue",
    lastMonthRevenue: "Last month revenue",
    newRevenueLastMonth: "New revenue for last month",
    leadToCustomer: "Lead → Customer",
    dealToWon: "Deal → Won",
    conversionRate: "conversion rate",
    popularCourses: "Popular courses",
    top: "Top",
    noCourseData: "No course data",
    summary: "Summary",
  },
  ru: {
    appTitle: "Мини CRM",
    appSubtitle: "Фронтенд для Django REST API",
    language: "Язык",
    login: "Вход",
    username: "Имя пользователя",
    password: "Пароль",
    signIn: "Войти",
    logout: "Выйти",
    loading: "Загрузка...",
    signedIn: "Вход выполнен",
    sessionExpired: "Сессия истекла. Войдите снова.",
    accessTokenMissing: "Бэкенд не вернул access-токен",
    refreshTokenMissing: "Бэкенд не вернул refresh-токен",
    selectPlaceholder: "Выберите...",
    total: "всего",
    role: "роль",
    refresh: "Обновить",
    main: "Основное",
    status: "Статус",
    updated: "Обновлено",
    actions: "Действия",
    open: "Открыть",
    archive: "В архив",
    activate: "Активировать",
    won: "Выиграна",
    lost: "Проиграна",
    delete: "Удалить",
    noData: "Нет данных",
    prev: "Назад",
    next: "Вперед",
    page: "Страница",
    edit: "Редактировать",
    create: "Создать",
    clear: "Очистить",
    saveChanges: "Сохранить изменения",
    created: "Создано",
    saved: "Обновлено",
    deleted: "Удалено",
    readOnlyForRole: "Для роли {role} доступен только просмотр",
    rawSelectedObject: "Исходный выбранный объект",
    deleteConfirm: "Удалить {name}?",
    lossReason: "Причина проигрыша?",
    actionDone: "Действие {action} выполнено",
    itemCount: "{count} шт.",
    itemFallback: "Элемент",
    dealFallback: "сделка",
    accounts: "Аккаунты",
    account: "Аккаунт",
    contacts: "Контакты",
    contact: "Контакт",
    courses: "Курсы",
    course: "Курс",
    deals: "Сделки",
    deal: "Сделка",
    contracts: "Контракты",
    contract: "Контракт",
    users: "Пользователи",
    user: "Пользователь",
    me: "Мой профиль",
    profile: "Профиль",
    roles: "Роли",
    roleSingular: "Роль",
    auth: "Авторизация",
    analytics: "Аналитика",
    fieldName: "Название",
    fieldType: "Тип",
    fieldStatus: "Статус",
    fieldCountry: "Страна",
    fieldCity: "Город",
    fieldAddress: "Адрес",
    fieldDescription: "Описание",
    fieldFirstName: "Имя",
    fieldLastName: "Фамилия",
    fieldEmail: "Email",
    fieldPhone: "Телефон",
    fieldAccountUuid: "UUID аккаунта",
    fieldUnitPrice: "Цена за единицу",
    fieldCurrency: "Валюта",
    fieldLmsCourseRef: "Ссылка на курс в LMS",
    fieldExpectedValue: "Ожидаемая сумма",
    fieldExpectedCloseDate: "Ожидаемая дата закрытия",
    fieldLossReason: "Причина проигрыша",
    fieldOwnerUuid: "UUID владельца",
    fieldContractUuid: "UUID контракта",
    fieldPrimaryContactUuid: "UUID основного контакта",
    fieldUsername: "Имя пользователя",
    fieldPassword: "Пароль",
    dealItems: "Позиции сделки",
    courseUuid: "UUID курса",
    quantity: "Количество",
    addItem: "Добавить позицию",
    dealItemId: "ID позиции сделки",
    update: "Обновить",
    remove: "Удалить",
    dealItemAdded: "Позиция сделки добавлена",
    dealItemUpdated: "Позиция сделки обновлена",
    dealItemRemoved: "Позиция сделки удалена",
    removeDealItemConfirm: "Удалить эту позицию сделки?",
    removeDealItemHint: "Удаление использует POST /deals/{id}/items/{di_id}/ согласно OpenAPI-спецификации.",
    roleEndpointHint: "PUT/DELETE /api/v1/{user_id}/role/",
    onlyDirectorRoles: "Управлять ролями может только director",
    userUuid: "UUID пользователя",
    setRole: "Назначить роль",
    revoke: "Отозвать",
    revokeRoleConfirm: "Отозвать роль у этого пользователя?",
    roleUpdated: "Роль обновлена",
    roleRevoked: "Роль отозвана",
    authEndpoints: "Эндпоинты авторизации",
    authHint: "JWT verify/refresh и пользовательские auth-эндпоинты Djoser.",
    jwt: "JWT",
    verifyAccess: "Проверить access",
    refreshAccess: "Обновить access",
    accessVerified: "Access-токен проверен",
    accessRefreshed: "Access-токен обновлен",
    activation: "Активация",
    activateUser: "Активировать",
    userActivated: "Пользователь активирован",
    emailFlows: "Email-сценарии",
    resendActivation: "Отправить активацию повторно",
    resetPasswordEmail: "Письмо для сброса пароля",
    resetUsernameEmail: "Письмо для сброса имени пользователя",
    activationEmailResent: "Письмо активации отправлено повторно",
    passwordResetEmailSent: "Письмо для сброса пароля отправлено",
    usernameResetEmailSent: "Письмо для сброса имени пользователя отправлено",
    confirmPasswordReset: "Подтверждение сброса пароля",
    newPassword: "новый пароль",
    confirm: "Подтвердить",
    passwordResetConfirmed: "Сброс пароля подтвержден",
    confirmUsernameReset: "Подтверждение сброса имени пользователя",
    newUsername: "новое имя пользователя",
    usernameResetConfirmed: "Сброс имени пользователя подтвержден",
    setCurrentUserCredentials: "Изменение учетных данных текущего пользователя",
    currentPassword: "текущий пароль",
    passwordChanged: "Пароль изменен",
    usernameChanged: "Имя пользователя изменено",
    setPassword: "Изменить пароль",
    setUsername: "Изменить имя пользователя",
    analyticsHint: "Живые метрики из ORM-эндпоинтов",
    pipelineValue: "Сумма пайплайна",
    openPipelineTotal: "Итого по открытым сделкам",
    totalRevenue: "Общая выручка",
    allTimeRevenue: "Выручка за все время",
    lastMonthRevenue: "Выручка за прошлый месяц",
    newRevenueLastMonth: "Новая выручка за прошлый месяц",
    leadToCustomer: "Лид → Клиент",
    dealToWon: "Сделка → Выиграна",
    conversionRate: "конверсия",
    popularCourses: "Популярные курсы",
    top: "Топ",
    noCourseData: "Нет данных по курсам",
    summary: "Сводка",
  },
};

const optionLabels = {
  en: {},
  ru: {
    SCHOOL: "Школа",
    UNIVERSITY: "Университет",
    COMPANY: "Компания",
    OTHER: "Другое",
    RUSSIA: "Россия",
    BELARUS: "Беларусь",
    KAZAKHSTAN: "Казахстан",
    USA: "США",
    EUROPE: "Европа",
    USD: "USD",
    RUB: "RUB",
    new: "Новый",
    active: "Активный",
    customer: "Клиент",
    lead: "Лид",
    archived: "В архиве",
    deleted: "Удален",
    open: "Открыта",
    won: "Выиграна",
    lost: "Проиграна",
    manager: "manager",
    director: "director",
    analyst: "analyst",
  },
};

const resources = {
  accounts: {
    titleKey: "accounts",
    singularKey: "account",
    path: "/accounts/",
    canWrite: ["manager", "director"],
    canDelete: ["director"],
    fields: [
      ["name", "fieldName", "text", true],
      ["account_type", "fieldType", "select", true, ["SCHOOL", "UNIVERSITY", "COMPANY", "OTHER"]],
      ["status", "fieldStatus", "select", false, ["new", "active", "customer", "lead"]],
      ["country", "fieldCountry", "select", true, ["RUSSIA", "BELARUS", "KAZAKHSTAN", "USA", "EUROPE", "OTHER"]],
      ["city", "fieldCity", "text", true],
      ["address", "fieldAddress", "text", true],
      ["description", "fieldDescription", "textarea", false],
    ],
  },
  contacts: {
    titleKey: "contacts",
    singularKey: "contact",
    path: "/contacts/",
    canWrite: ["manager", "director"],
    canDelete: ["director"],
    fields: [
      ["first_name", "fieldFirstName", "text", true],
      ["last_name", "fieldLastName", "text", false],
      ["email", "fieldEmail", "email", true],
      ["phone", "fieldPhone", "text", false],
      ["account", "fieldAccountUuid", "text", true],
    ],
  },
  courses: {
    titleKey: "courses",
    singularKey: "course",
    path: "/courses/",
    canWrite: ["manager", "director"],
    canDelete: ["director"],
    fields: [
      ["name", "fieldName", "text", true],
      ["description", "fieldDescription", "textarea", false],
      ["status", "fieldStatus", "select", false, ["active", "archived", "deleted"]],
      ["unit_price", "fieldUnitPrice", "number", true],
      ["currency", "fieldCurrency", "select", true, ["USD", "RUB"]],
      ["lms_course_ref", "fieldLmsCourseRef", "text", false],
    ],
  },
  deals: {
    titleKey: "deals",
    singularKey: "deal",
    path: "/deals/",
    canWrite: ["manager", "director"],
    canDelete: [],
    fields: [
      ["status", "fieldStatus", "select", false, ["open", "won", "lost", "archived"]],
      ["expected_value", "fieldExpectedValue", "number", false],
      ["expected_close_date", "fieldExpectedCloseDate", "date", false],
      ["description", "fieldDescription", "textarea", false],
      ["loss_reason", "fieldLossReason", "text", false],
      ["account", "fieldAccountUuid", "text", true],
      ["owner", "fieldOwnerUuid", "text", false],
      ["contract", "fieldContractUuid", "text", false],
      ["primary_contact", "fieldPrimaryContactUuid", "text", false],
    ],
  },
  contracts: {
    titleKey: "contracts",
    singularKey: "contract",
    path: "/contracts/",
    canWrite: [],
    canDelete: [],
    readonly: true,
    fields: [],
  },
  users: {
    titleKey: "users",
    singularKey: "user",
    path: "/users/",
    canWrite: ["director"],
    canDelete: ["director"],
    fields: [
      ["email", "fieldEmail", "email", false],
      ["username", "fieldUsername", "text", true],
      ["password", "fieldPassword", "password", false, null, { createOnly: true }],
    ],
  },
  me: {
    titleKey: "me",
    singularKey: "profile",
    path: "/users/me/",
    canWrite: ["manager", "director", "analyst"],
    canDelete: ["director"],
    singleton: true,
    fields: [["email", "fieldEmail", "email", false]],
  },
  role: {
    titleKey: "roles",
    singularKey: "roleSingular",
    path: "/role/",
    canWrite: ["director"],
    canDelete: [],
    readonly: true,
    isRoleManager: true,
    fields: [],
  },
  auth: {
    titleKey: "auth",
    singularKey: "auth",
    path: "",
    canWrite: [],
    canDelete: [],
    readonly: true,
    isAuthPanel: true,
    fields: [],
  },
  analytics: {
    titleKey: "analytics",
    singularKey: "analytics",
    path: "",
    canWrite: [],
    canDelete: [],
    readonly: true,
    fields: [],
    isAnalytics: true,
  },
};

const emptyValues = Object.fromEntries(
  Object.entries(resources).flatMap(([key, res]) => res.fields.map(([name]) => [`${key}.${name}`, ""]))
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

function localeFromStorage() {
  return localStorage.getItem(LOCALE_STORAGE_KEY) || "ru";
}

function makeTranslator(locale) {
  return function translate(key, params = {}) {
    const template = i18n[locale]?.[key] ?? i18n.en[key] ?? key;
    return Object.entries(params).reduce((text, [name, value]) => text.replaceAll(`{${name}}`, String(value)), template);
  };
}

function getOptionLabel(locale, value) {
  return optionLabels[locale]?.[value] || value;
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

function pickPreview(item, t) {
  if (!item) return "";
  if (item.name) return item.name;
  if (item.email) return item.email;
  if (item.username) return item.username;
  if (item.expected_value) return `${item.expected_value} · ${item.status || t("dealFallback")}`;
  return item.id || t("itemFallback");
}

function formatValue(value, t, locale = "ru") {
  if (value === null || value === undefined || value === "") return "—";
  if (Array.isArray(value)) return t("itemCount", { count: value.length });
  if (typeof value === "object") return value.id || JSON.stringify(value);
  return getOptionLabel(locale, String(value));
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

function money(value, locale = "ru") {
  const number = Number(value || 0);
  const intlLocale = locale === "ru" ? "ru-RU" : "en-US";
  return new Intl.NumberFormat(intlLocale, { maximumFractionDigits: 0 }).format(number);
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

function BarChart({ rows, locale }) {
  const max = Math.max(...rows.map((row) => row.value), 1);
  return (
    <div className="space-y-3">
      {rows.map((row) => (
        <div key={row.name}>
          <div className="mb-1 flex justify-between gap-3 text-xs">
            <span className="truncate text-slate-600">{row.name}</span>
            <span className="font-medium text-slate-900">{money(row.value, locale)}</span>
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

function FieldInput({ field, value, disabled, onChange, t, locale }) {
  const [name, labelKey, type, required, options] = field;

  return (
    <label className={type === "textarea" ? "md:col-span-2" : ""}>
      <span className="mb-1 block text-xs font-medium text-slate-600">
        {t(labelKey)}{required ? " *" : ""}
      </span>
      {type === "select" ? (
        <select
          className="w-full rounded-lg border px-3 py-2"
          value={value}
          onChange={(event) => onChange(name, event.target.value)}
          disabled={disabled}
        >
          <option value="">{t("selectPlaceholder")}</option>
          {options.map((option) => (
            <option key={option} value={option}>{getOptionLabel(locale, option)}</option>
          ))}
        </select>
      ) : type === "textarea" ? (
        <textarea
          className="min-h-24 w-full rounded-lg border px-3 py-2"
          value={value}
          onChange={(event) => onChange(name, event.target.value)}
          disabled={disabled}
        />
      ) : (
        <input
          className="w-full rounded-lg border px-3 py-2"
          type={type}
          value={value}
          onChange={(event) => onChange(name, event.target.value)}
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
  const [locale, setLocale] = useState(localeFromStorage);
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

  const t = useMemo(() => makeTranslator(locale), [locale]);
  const resource = resources[active];
  const canWrite = resource.canWrite.includes(role);
  const canDelete = resource.canDelete?.includes(role);

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
      throw new Error(t("sessionExpired"));
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
      return request(
        path,
        {
          ...options,
          headers: {
            ...(options.headers || {}),
            Authorization: `${AUTH_HEADER_PREFIX} ${newAccess}`,
          },
        },
        false
      );
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
      if (!access) throw new Error(t("accessTokenMissing"));
      if (!refresh) throw new Error(t("refreshTokenMissing"));
      localStorage.setItem("crm_access_token", access);
      localStorage.setItem("crm_refresh_token", refresh);
      localStorage.setItem("crm_role", role);
      setToken(access);
      setRefreshToken(refresh);
      setNotice(t("signedIn"));
    } catch (errorObject) {
      setError(errorObject.message);
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

  function changeLocale(nextLocale) {
    setLocale(nextLocale);
    localStorage.setItem(LOCALE_STORAGE_KEY, nextLocale);
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
    } catch (errorObject) {
      setError(errorObject.message);
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
    } catch (errorObject) {
      setError(errorObject.message);
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
    } catch (errorObject) {
      setError(errorObject.message);
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
      setNotice(isEdit ? t("saved") : t("created"));
      clearForm();
      await load();
    } catch (errorObject) {
      setError(errorObject.message);
    } finally {
      setLoading(false);
    }
  }

  async function destroyItem(item) {
    if (!canDelete) return;
    if (!window.confirm(t("deleteConfirm", { name: pickPreview(item, t) }))) return;
    setLoading(true);
    try {
      const path = resource.singleton ? resource.path : `${resource.path}${item.id}/`;
      await request(path, { method: "DELETE" });
      setNotice(t("deleted"));
      clearForm();
      await load();
    } catch (errorObject) {
      setError(errorObject.message);
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
      setNotice(t("actionDone", { action: actionName }));
      await load();
    } catch (errorObject) {
      setError(errorObject.message);
    } finally {
      setLoading(false);
    }
  }

  async function closeDeal(item, status) {
    const loss_reason = status === "lost" ? window.prompt(t("lossReason"), "") : undefined;
    await action(item, "close", { status, loss_reason });
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <div>
            <h1 className="text-lg font-semibold">{t("appTitle")}</h1>
            <p className="text-xs text-slate-500">{t("appSubtitle")}</p>
          </div>
          <div className="flex items-center gap-2">
            <select
              className="rounded-lg border px-2 py-1 text-sm"
              value={locale}
              aria-label={t("language")}
              onChange={(event) => changeLocale(event.target.value)}
            >
              <option value="ru">RU</option>
              <option value="en">EN</option>
            </select>
            {token && (
              <>
                <select
                  className="rounded-lg border px-2 py-1 text-sm"
                  value={role}
                  onChange={(event) => {
                    setRole(event.target.value);
                    localStorage.setItem("crm_role", event.target.value);
                  }}
                >
                  <option value="director">director</option>
                  <option value="manager">manager</option>
                  <option value="analyst">analyst</option>
                </select>
                <button className="rounded-lg border px-3 py-1 text-sm" onClick={signOut}>{t("logout")}</button>
              </>
            )}
          </div>
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
            t={t}
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
                  {t(value.titleKey)}
                </button>
              ))}
            </aside>

            <section className="space-y-4">
              {resource.isAnalytics ? (
                <AnalyticsPanel analytics={analytics} loading={loading} error={error} notice={notice} onRefresh={loadAnalytics} t={t} locale={locale} />
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
                  t={t}
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
                  t={t}
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
                    t={t}
                    locale={locale}
                  />

                  {!resource.readonly && (
                    <form onSubmit={save} className="rounded-2xl border bg-white p-4 shadow-sm">
                      <div className="mb-4 flex items-center justify-between">
                        <h3 className="text-base font-semibold">
                          {selected ? t("edit") : t("create")} {t(resource.singularKey)}
                        </h3>
                        <button type="button" className="rounded-lg border px-3 py-1 text-sm" onClick={clearForm}>{t("clear")}</button>
                      </div>

                      {!canWrite && <div className="mb-3 rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-700">{t("readOnlyForRole", { role })}</div>}

                      <div className="grid gap-3 md:grid-cols-2">
                        {resource.fields
                          .filter(([, , , , , meta]) => !(meta?.createOnly && selected?.id))
                          .map((field) => (
                            <FieldInput
                              key={field[0]}
                              field={field}
                              value={form[`${active}.${field[0]}`]}
                              disabled={!canWrite}
                              onChange={changeField}
                              t={t}
                              locale={locale}
                            />
                          ))}
                      </div>

                      <button className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-40" disabled={!canWrite || loading}>
                        {selected ? t("saveChanges") : t("create")}
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
                      t={t}
                    />
                  )}

                  {selected && (
                    <details className="rounded-2xl border bg-white p-4 shadow-sm" open>
                      <summary className="cursor-pointer font-semibold">{t("rawSelectedObject")}</summary>
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

function LoginPanel({ login, setLogin, role, setRole, loading, error, notice, onSubmit, t }) {
  return (
    <section className="mx-auto max-w-sm rounded-2xl border bg-white p-5 shadow-sm">
      <h2 className="mb-4 text-base font-semibold">{t("login")}</h2>
      {notice && <div className="mb-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
      {error && <pre className="mb-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}
      <form onSubmit={onSubmit} className="space-y-3">
        <input
          className="w-full rounded-lg border px-3 py-2"
          placeholder={t("username")}
          value={login.username}
          onChange={(event) => setLogin({ ...login, username: event.target.value })}
        />
        <input
          className="w-full rounded-lg border px-3 py-2"
          placeholder={t("password")}
          type="password"
          value={login.password}
          onChange={(event) => setLogin({ ...login, password: event.target.value })}
        />
        <select className="w-full rounded-lg border px-3 py-2" value={role} onChange={(event) => setRole(event.target.value)}>
          <option value="manager">manager</option>
          <option value="director">director</option>
          <option value="analyst">analyst</option>
        </select>
        <button className="w-full rounded-lg bg-slate-900 px-3 py-2 text-white" disabled={loading}>
          {loading ? t("loading") : t("signIn")}
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
  t,
  locale,
}) {
  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="text-base font-semibold">{t(resource.titleKey)}</h2>
          <p className="text-xs text-slate-500">{data.count} {t("total")} · {t("role")}: {role}</p>
        </div>
        {!resource.singleton && (
          <div className="flex items-center gap-2">
            <select className="rounded-lg border px-2 py-1 text-sm" value={size} onChange={(event) => setSize(Number(event.target.value))}>
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={50}>50</option>
            </select>
            <button className="rounded-lg border px-3 py-1 text-sm" onClick={onRefresh} disabled={loading}>{t("refresh")}</button>
          </div>
        )}
      </div>

      {notice && <div className="mb-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
      {error && <pre className="mb-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b text-xs uppercase text-slate-500">
              <th className="py-2">{t("main")}</th>
              <th className="py-2">{t("status")}</th>
              <th className="py-2">{t("updated")}</th>
              <th className="py-2">{t("actions")}</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((item) => (
              <tr key={item.id || item.email || "me"} className="border-b last:border-0">
                <td className="py-2">
                  <button className="font-medium hover:underline" onClick={() => onOpen(item)}>
                    {pickPreview(item, t)}
                  </button>
                  <div className="text-xs text-slate-500">{item.id || "—"}</div>
                </td>
                <td className="py-2">{formatValue(item.status || item.account_type || item.currency || item.username, t, locale)}</td>
                <td className="py-2">{formatValue(item.updated_at || item.created_at, t, locale)}</td>
                <td className="py-2">
                  <div className="flex flex-wrap gap-1">
                    <button className="rounded border px-2 py-1 text-xs" onClick={() => onOpen(item)}>{t("open")}</button>
                    {active === "courses" && canWrite && item.status === "active" && (
                      <button className="rounded border px-2 py-1 text-xs" onClick={() => onAction(item, "archive")}>{t("archive")}</button>
                    )}
                    {active === "courses" && canWrite && item.status === "archived" && (
                      <button className="rounded border px-2 py-1 text-xs" onClick={() => onAction(item, "activate")}>{t("activate")}</button>
                    )}
                    {active === "deals" && canWrite && item.status === "open" && (
                      <>
                        <button className="rounded border px-2 py-1 text-xs" onClick={() => onCloseDeal(item, "won")}>{t("won")}</button>
                        <button className="rounded border px-2 py-1 text-xs" onClick={() => onCloseDeal(item, "lost")}>{t("lost")}</button>
                      </>
                    )}
                    {canDelete && (
                      <button className="rounded border px-2 py-1 text-xs text-red-700" onClick={() => onDelete(item)}>{t("delete")}</button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {!data.items.length && (
              <tr>
                <td className="py-8 text-center text-sm text-slate-500" colSpan={4}>
                  {loading ? t("loading") : t("noData")}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {!resource.singleton && (
        <div className="mt-4 flex items-center justify-between text-sm">
          <button className="rounded-lg border px-3 py-1 disabled:opacity-40" disabled={page <= 1} onClick={() => setPage((oldPage) => oldPage - 1)}>{t("prev")}</button>
          <span>{t("page")} {page}</span>
          <button className="rounded-lg border px-3 py-1 disabled:opacity-40" disabled={!data.next && data.items.length < size} onClick={() => setPage((oldPage) => oldPage + 1)}>{t("next")}</button>
        </div>
      )}
    </div>
  );
}

function DealItemsPanel({ deal, request, onReload, setLoading, setError, setNotice, t }) {
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
      setNotice(t("dealItemAdded"));
      setItem({ course: "", quantity: "1" });
      await onReload();
    } catch (errorObject) {
      setError(errorObject.message);
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
      setNotice(t("dealItemUpdated"));
      await onReload();
    } catch (errorObject) {
      setError(errorObject.message);
    } finally {
      setLoading(false);
    }
  }

  async function removeDealItem() {
    if (!diId) return;
    if (!window.confirm(t("removeDealItemConfirm"))) return;
    setLoading(true);
    try {
      await request(`/deals/${deal.id}/items/${diId}/`, { method: "POST" });
      setNotice(t("dealItemRemoved"));
      setDiId("");
      await onReload();
    } catch (errorObject) {
      setError(errorObject.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <h3 className="mb-4 text-base font-semibold">{t("dealItems")}</h3>
      <form onSubmit={addDealItem} className="grid gap-3 md:grid-cols-[1fr_140px_auto]">
        <input
          className="rounded-lg border px-3 py-2"
          placeholder={t("courseUuid")}
          value={item.course}
          onChange={(event) => setItem({ ...item, course: event.target.value })}
        />
        <input
          className="rounded-lg border px-3 py-2"
          type="number"
          min="0"
          placeholder={t("quantity")}
          value={item.quantity}
          onChange={(event) => setItem({ ...item, quantity: event.target.value })}
        />
        <button className="rounded-lg bg-slate-900 px-4 py-2 text-white">{t("addItem")}</button>
      </form>

      <form onSubmit={updateDealItem} className="mt-3 grid gap-3 md:grid-cols-[1fr_1fr_140px_auto_auto]">
        <input
          className="rounded-lg border px-3 py-2"
          placeholder={t("dealItemId")}
          value={diId}
          onChange={(event) => setDiId(event.target.value)}
        />
        <input
          className="rounded-lg border px-3 py-2"
          placeholder={t("courseUuid")}
          value={item.course}
          onChange={(event) => setItem({ ...item, course: event.target.value })}
        />
        <input
          className="rounded-lg border px-3 py-2"
          type="number"
          min="0"
          placeholder={t("quantity")}
          value={item.quantity}
          onChange={(event) => setItem({ ...item, quantity: event.target.value })}
        />
        <button className="rounded-lg border px-4 py-2">{t("update")}</button>
        <button type="button" className="rounded-lg border px-4 py-2 text-red-700" onClick={removeDealItem}>{t("remove")}</button>
      </form>
      <p className="mt-2 text-xs text-slate-500">{t("removeDealItemHint")}</p>
    </div>
  );
}

function RolePanel({ loading, error, notice, canWrite, request, setLoading, setError, setNotice, t }) {
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
      setNotice(t("roleUpdated"));
    } catch (errorObject) {
      setError(errorObject.message);
    } finally {
      setLoading(false);
    }
  }

  async function revokeUserRole() {
    if (!canWrite || !userId) return;
    if (!window.confirm(t("revokeRoleConfirm"))) return;
    setLoading(true);
    try {
      await request(`/${userId}/role/`, { method: "DELETE" });
      setNotice(t("roleRevoked"));
    } catch (errorObject) {
      setError(errorObject.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold">{t("roles")}</h2>
      <p className="mb-4 text-xs text-slate-500">{t("roleEndpointHint")}</p>
      {notice && <div className="mb-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
      {error && <pre className="mb-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}
      {!canWrite && <div className="mb-3 rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-700">{t("onlyDirectorRoles")}</div>}
      <form onSubmit={setUserRole} className="grid gap-3 md:grid-cols-[1fr_180px_auto_auto]">
        <input
          className="rounded-lg border px-3 py-2"
          placeholder={t("userUuid")}
          value={userId}
          onChange={(event) => setUserId(event.target.value)}
          disabled={!canWrite}
        />
        <input
          className="rounded-lg border px-3 py-2"
          placeholder={t("role")}
          value={role}
          onChange={(event) => setRole(event.target.value)}
          disabled={!canWrite}
        />
        <button className="rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-40" disabled={!canWrite || loading}>{t("setRole")}</button>
        <button type="button" className="rounded-lg border px-4 py-2 text-red-700 disabled:opacity-40" disabled={!canWrite || loading} onClick={revokeUserRole}>{t("revoke")}</button>
      </form>
    </div>
  );
}

function AuthPanel({ loading, error, notice, token, refreshToken, request, refreshAccessToken, setLoading, setError, setNotice, t }) {
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
    } catch (errorObject) {
      setError(errorObject.message);
    } finally {
      setLoading(false);
    }
  }

  async function verifyAccessToken() {
    await runAuthAction(t("accessVerified"), "/auth/jwt/verify/", { token });
  }

  async function refreshNow() {
    setLoading(true);
    try {
      const access = await refreshAccessToken();
      setNotice(t("accessRefreshed"));
      setVerifyResult(JSON.stringify({ access }, null, 2));
    } catch (errorObject) {
      setError(errorObject.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="rounded-2xl border bg-white p-4 shadow-sm">
        <h2 className="text-base font-semibold">{t("authEndpoints")}</h2>
        <p className="text-xs text-slate-500">{t("authHint")}</p>
        {notice && <div className="mt-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
        {error && <pre className="mt-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">{t("jwt")}</h3>
          <div className="flex flex-wrap gap-2">
            <button className="rounded-lg border px-3 py-2 text-sm" onClick={verifyAccessToken} disabled={loading || !token}>{t("verifyAccess")}</button>
            <button className="rounded-lg border px-3 py-2 text-sm" onClick={refreshNow} disabled={loading || !refreshToken}>{t("refreshAccess")}</button>
          </div>
          {verifyResult && <pre className="mt-3 overflow-auto rounded-xl bg-slate-950 p-3 text-xs text-slate-50">{verifyResult}</pre>}
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">{t("activation")}</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" placeholder="uid" value={activation.uid} onChange={(event) => setActivation({ ...activation, uid: event.target.value })} />
            <input className="rounded-lg border px-3 py-2" placeholder="token" value={activation.token} onChange={(event) => setActivation({ ...activation, token: event.target.value })} />
            <button className="rounded-lg bg-slate-900 px-3 py-2 text-white" disabled={loading} onClick={() => runAuthAction(t("userActivated"), "/users/activation/", activation)}>{t("activateUser")}</button>
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">{t("emailFlows")}</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" placeholder="email" value={email} onChange={(event) => setEmail(event.target.value)} />
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction(t("activationEmailResent"), "/users/resend_activation/", { email })}>{t("resendActivation")}</button>
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction(t("passwordResetEmailSent"), "/users/reset_password/", { email })}>{t("resetPasswordEmail")}</button>
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction(t("usernameResetEmailSent"), "/users/reset_username/", { email })}>{t("resetUsernameEmail")}</button>
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">{t("confirmPasswordReset")}</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" placeholder="uid" value={passwordReset.uid} onChange={(event) => setPasswordReset({ ...passwordReset, uid: event.target.value })} />
            <input className="rounded-lg border px-3 py-2" placeholder="token" value={passwordReset.token} onChange={(event) => setPasswordReset({ ...passwordReset, token: event.target.value })} />
            <input className="rounded-lg border px-3 py-2" type="password" placeholder={t("newPassword")} value={passwordReset.new_password} onChange={(event) => setPasswordReset({ ...passwordReset, new_password: event.target.value })} />
            <button className="rounded-lg bg-slate-900 px-3 py-2 text-white" disabled={loading} onClick={() => runAuthAction(t("passwordResetConfirmed"), "/users/reset_password_confirm/", passwordReset)}>{t("confirm")}</button>
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">{t("confirmUsernameReset")}</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" placeholder={t("newUsername")} value={usernameReset.new_username} onChange={(event) => setUsernameReset({ new_username: event.target.value })} />
            <button className="rounded-lg bg-slate-900 px-3 py-2 text-white" disabled={loading} onClick={() => runAuthAction(t("usernameResetConfirmed"), "/users/reset_username_confirm/", usernameReset)}>{t("confirm")}</button>
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-sm font-semibold">{t("setCurrentUserCredentials")}</h3>
          <div className="grid gap-2">
            <input className="rounded-lg border px-3 py-2" type="password" placeholder={t("currentPassword")} value={setPassword.current_password} onChange={(event) => setSetPassword({ ...setPassword, current_password: event.target.value })} />
            <input className="rounded-lg border px-3 py-2" type="password" placeholder={t("newPassword")} value={setPassword.new_password} onChange={(event) => setSetPassword({ ...setPassword, new_password: event.target.value })} />
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction(t("passwordChanged"), "/users/set_password/", setPassword)}>{t("setPassword")}</button>
            <input className="rounded-lg border px-3 py-2" type="password" placeholder={t("currentPassword")} value={setUsername.current_password} onChange={(event) => setSetUsername({ ...setUsername, current_password: event.target.value })} />
            <input className="rounded-lg border px-3 py-2" placeholder={t("newUsername")} value={setUsername.new_username} onChange={(event) => setSetUsername({ ...setUsername, new_username: event.target.value })} />
            <button className="rounded-lg border px-3 py-2 text-sm" disabled={loading} onClick={() => runAuthAction(t("usernameChanged"), "/users/set_username/", setUsername)}>{t("setUsername")}</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function AnalyticsPanel({ analytics, loading, error, notice, onRefresh, t, locale }) {
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
            <h2 className="text-base font-semibold">{t("analytics")}</h2>
            <p className="text-xs text-slate-500">{t("analyticsHint")}</p>
          </div>
          <button className="rounded-lg border px-3 py-1 text-sm" onClick={onRefresh} disabled={loading}>
            {loading ? t("loading") : t("refresh")}
          </button>
        </div>
        {notice && <div className="mt-3 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">{notice}</div>}
        {error && <pre className="mt-3 whitespace-pre-wrap rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">{error}</pre>}
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard title={t("pipelineValue")} value={money(pipeline, locale)} hint={t("openPipelineTotal")} />
        <MetricCard title={t("totalRevenue")} value={money(totalRevenue, locale)} hint={t("allTimeRevenue")} />
        <MetricCard title={t("lastMonthRevenue")} value={money(lastMonthRevenue, locale)} hint={t("newRevenueLastMonth")} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <h3 className="mb-4 text-sm font-semibold">{t("leadToCustomer")}</h3>
          <Donut value={leadRate} label={t("conversionRate")} />
        </div>
        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <h3 className="mb-4 text-sm font-semibold">{t("dealToWon")}</h3>
          <Donut value={wonRate} label={t("conversionRate")} />
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-sm font-semibold">{t("popularCourses")}</h3>
            <span className="text-xs text-slate-400">{t("top")} {popularCourses.length}</span>
          </div>
          {popularCourses.length ? (
            <BarChart rows={popularCourses} locale={locale} />
          ) : (
            <div className="rounded-xl bg-slate-50 p-6 text-center text-sm text-slate-500">{t("noCourseData")}</div>
          )}
        </div>

        <div className="rounded-2xl border bg-white p-5 shadow-sm">
          <h3 className="mb-4 text-sm font-semibold">{t("summary")}</h3>
          {summary ? (
            <div className="space-y-2">
              {Object.entries(summary).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between gap-3 rounded-xl bg-slate-50 px-3 py-2 text-sm">
                  <span className="text-slate-500">{key.replaceAll("_", " ")}</span>
                  <span className="font-medium">{formatValue(value, t, locale)}</span>
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
