const ADMIN_KEY = "cc_admin_password";

export function getAdminPassword() {
  return sessionStorage.getItem(ADMIN_KEY) || "";
}

export function setAdminPassword(password) {
  sessionStorage.setItem(ADMIN_KEY, password);
}

export function clearAdminPassword() {
  sessionStorage.removeItem(ADMIN_KEY);
}

export async function fetchFamily() {
  try {
    const res = await fetch("/.netlify/functions/family");
    if (res.ok) return res.json();
  } catch (_) {
    /* local preview without functions */
  }
  const fallback = await fetch("/data/family.json");
  if (!fallback.ok) throw new Error("Could not load family data.");
  return fallback.json();
}

export async function saveFamily(data) {
  const password = getAdminPassword();
  const res = await fetch("/.netlify/functions/family", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "X-Admin-Password": password,
    },
    body: JSON.stringify(data),
  });
  if (res.status === 401) throw new Error("Session expired. Sign in again.");
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Could not save changes.");
  }
  return res.json();
}

export async function login(password) {
  const res = await fetch("/.netlify/functions/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });
  if (!res.ok) return false;
  setAdminPassword(password);
  return true;
}
