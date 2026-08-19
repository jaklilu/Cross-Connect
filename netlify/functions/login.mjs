export default async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const expected = process.env.ADMIN_PASSWORD || "familyadmin";
  let body = {};
  try {
    body = await req.json();
  } catch (_) {
    return new Response("Bad request", { status: 400 });
  }

  if ((body.password || "") !== expected) {
    return new Response("Unauthorized", { status: 401 });
  }

  return Response.json({ ok: true });
};
