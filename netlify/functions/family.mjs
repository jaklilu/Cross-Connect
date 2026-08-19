import { getStore } from "@netlify/blobs";

const STORE = "crossconnect";
const KEY = "family";

async function fallbackData(req) {
  const origin = process.env.URL || new URL(req.url).origin;
  const res = await fetch(`${origin}/data/family.json`);
  if (!res.ok) throw new Error("Family data not found.");
  return res.json();
}

async function readFamily(req) {
  const store = getStore(STORE);
  const saved = await store.get(KEY, { type: "json" });
  if (saved) return saved;
  return fallbackData(req);
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type, X-Admin-Password",
    "Access-Control-Allow-Methods": "GET, PUT, OPTIONS",
  };
}

export default async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders() });
  }

  if (req.method === "GET") {
    try {
      const data = await readFamily(req);
      return Response.json(data, { headers: corsHeaders() });
    } catch (err) {
      return new Response(err.message, { status: 500, headers: corsHeaders() });
    }
  }

  if (req.method === "PUT") {
    const expected = process.env.ADMIN_PASSWORD || "familyadmin";
    const provided = req.headers.get("x-admin-password") || "";
    if (provided !== expected) {
      return new Response("Unauthorized", { status: 401, headers: corsHeaders() });
    }
    try {
      const data = await req.json();
      const store = getStore(STORE);
      await store.setJSON(KEY, data);
      return Response.json({ ok: true }, { headers: corsHeaders() });
    } catch (err) {
      return new Response(err.message, { status: 500, headers: corsHeaders() });
    }
  }

  return new Response("Method not allowed", { status: 405, headers: corsHeaders() });
};
