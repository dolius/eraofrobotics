import { createClient } from '@supabase/supabase-js';

function json(res, status, payload) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(payload));
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { ok: false, error: 'method_not_allowed' });

  const url = process.env.SUPABASE_URL;
  const secret = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !secret) return json(res, 500, { ok: false, error: 'missing_supabase_env' });

  const supabase = createClient(url, secret);
  let body = req.body || {};
  if (typeof body === 'string') {
    try { body = JSON.parse(body || '{}'); } catch { body = {}; }
  }

  const path = String(body.path || '/').slice(0, 500);
  const title = String(body.title || '').slice(0, 500);
  const referrer = String(body.referrer || '').slice(0, 1000);
  const event_type = String(body.event_type || 'page_view').slice(0, 100);
  const session_id = String(body.session_id || '').slice(0, 200);
  const ip_address = req.headers['x-forwarded-for'] || req.socket?.remoteAddress || null;
  const user_agent = req.headers['user-agent'] || null;

  const payload = [{ path, title, referrer, event_type, session_id, ip_address, user_agent }];
  const { error } = await supabase.from('analytics_events').insert(payload);
  if (error) return json(res, 500, { ok: false, error: 'analytics_insert_failed', detail: error.message });
  return json(res, 200, { ok: true });
}
