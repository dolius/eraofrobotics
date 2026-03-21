const https = require('https');
const { URL } = require('url');

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

function json(res, status, payload) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(payload));
}

function redirect(res, location) {
  res.statusCode = 303;
  res.setHeader('Location', location);
  res.end();
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => {
      raw += chunk;
      if (raw.length > 1000000) reject(new Error('body_too_large'));
    });
    req.on('end', () => {
      const contentType = String(req.headers['content-type'] || '').toLowerCase();
      try {
        if (contentType.indexOf('application/json') !== -1) {
          resolve({ payload: JSON.parse(raw || '{}'), wantsJson: true });
          return;
        }
        const params = new URLSearchParams(raw);
        const payload = {};
        for (const pair of params.entries()) payload[pair[0]] = pair[1];
        resolve({ payload, wantsJson: false });
      } catch (error) {
        reject(error);
      }
    });
    req.on('error', reject);
  });
}

function httpRequest(urlString, options, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlString);
    const req = https.request({
      protocol: url.protocol,
      hostname: url.hostname,
      port: url.port || 443,
      path: (url.pathname || '/') + (url.search || ''),
      method: options.method || 'GET',
      headers: options.headers || {},
    }, (res) => {
      let raw = '';
      res.on('data', chunk => { raw += chunk; });
      res.on('end', () => {
        resolve({ statusCode: res.statusCode || 0, body: raw, headers: res.headers || {} });
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function saveLead(input) {
  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseSecret = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!supabaseUrl || !supabaseSecret) {
    throw new Error('missing_supabase_env');
  }

  const createdAt = new Date().toISOString();
  const endpoint = supabaseUrl.replace(/\/$/, '') + '/rest/v1/leads?on_conflict=email';
  const body = JSON.stringify([{
    email: input.email.toLowerCase(),
    source: input.source,
    persona: input.persona,
    interest: input.interest,
    stage: input.stage,
    created_at: createdAt,
    ip_address: input.ip,
    user_agent: input.userAgent,
  }]);

  const response = await httpRequest(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(body),
      'apikey': supabaseSecret,
      'Authorization': 'Bearer ' + supabaseSecret,
      'Prefer': 'resolution=merge-duplicates,return=representation',
    },
  }, body);

  if (response.statusCode < 200 || response.statusCode >= 300) {
    throw new Error('supabase_insert_failed:' + response.statusCode + ':' + response.body);
  }
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    res.end();
    return;
  }

  if (req.method !== 'POST') {
    json(res, 405, { ok: false, error: 'method_not_allowed' });
    return;
  }

  try {
    const parsed = await parseBody(req);
    const payload = parsed.payload || {};
    const wantsJson = !!parsed.wantsJson;

    const email = String(payload.email || '').trim();
    const source = String(payload.source || 'robotics-brief-download').trim();
    const persona = String(payload.persona || 'general').trim();
    const interest = String(payload.interest || 'robotics-brief').trim();
    const stage = String(payload.stage || 'brief-captured').trim();

    if (!EMAIL_RE.test(email)) {
      if (wantsJson) return json(res, 400, { ok: false, error: 'invalid_email' });
      return redirect(res, '/brief-unlocked.html?error=invalid_email');
    }

    const forwardedFor = req.headers['x-forwarded-for'];
    const ip = forwardedFor ? String(forwardedFor).split(',')[0].trim() : ((req.socket && req.socket.remoteAddress) || null);

    await saveLead({
      email,
      source,
      persona,
      interest,
      stage,
      ip,
      userAgent: req.headers['user-agent'] || null,
    });

    if (wantsJson) {
      return json(res, 200, {
        ok: true,
        thankYouUrl: '/robotics-brief.html',
        downloadUrl: '/assets/pdf/robotics-brief-real.pdf',
        premiumUrl: '/premium-robotics-brief.html'
      });
    }

    return redirect(res, '/brief-unlocked.html');
  } catch (error) {
    const message = error && error.message ? error.message : 'unknown_error';
    return json(res, 500, { ok: false, error: message });
  }
};
