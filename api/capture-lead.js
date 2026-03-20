import { createClient } from '@supabase/supabase-js';

const emailRe = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

function json(res, status, payload) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(payload));
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return json(res, 405, { ok: false, error: 'method_not_allowed' });
  }

  const url = process.env.SUPABASE_URL;
  const secret = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !secret) {
    return json(res, 500, { ok: false, error: 'missing_supabase_env' });
  }

  const supabase = createClient(url, secret);
  let body = req.body || {};
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body || '{}');
    } catch {
      body = {};
    }
  }

  const email = String(body.email || '').trim().toLowerCase();
  const source = String(body.source || 'robotics-brief-download').trim();
  const persona = String(body.persona || 'general').trim();
  const interest = String(body.interest || 'robotics-brief').trim();
  const stage = String(body.stage || 'brief-captured').trim();
  const ip_address = req.headers['x-forwarded-for'] || req.socket?.remoteAddress || null;
  const user_agent = req.headers['user-agent'] || null;

  if (!emailRe.test(email)) {
    return json(res, 400, { ok: false, error: 'invalid_email' });
  }

  const payload = [{ email, source, persona, interest, stage, ip_address, user_agent }];
  const { error } = await supabase.from('leads').upsert(payload, { onConflict: 'email' });

  if (error) {
    return json(res, 500, {
      ok: false,
      error: 'supabase_insert_failed',
      detail: error.message
    });
  }

  return json(res, 200, {
    ok: true,
    thankYouUrl: '/robotics-brief.html',
    downloadUrl: '/assets/pdf/robotics-brief-real.pdf'
  });
}
