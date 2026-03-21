import { createClient } from '@supabase/supabase-js';

function json(res, status, payload) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(payload));
}

export default async function handler(req, res) {
  const url = process.env.SUPABASE_URL;
  const secret = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !secret) return json(res, 500, { ok: false, error: 'missing_supabase_env' });

  const supabase = createClient(url, secret);
  const { data, error } = await supabase
    .from('analytics_events')
    .select('path,title,referrer,event_type,session_id,created_at')
    .order('created_at', { ascending: false })
    .limit(5000);

  if (error) return json(res, 500, { ok: false, error: 'analytics_query_failed', detail: error.message });

  const rows = data || [];
  const pageViews = rows.filter(r => r.event_type === 'page_view');
  const uniqueSessions = new Set(pageViews.map(r => r.session_id).filter(Boolean)).size;
  const topPagesMap = new Map();
  const refMap = new Map();
  for (const r of pageViews) {
    topPagesMap.set(r.path, (topPagesMap.get(r.path) || 0) + 1);
    if (r.referrer) refMap.set(r.referrer, (refMap.get(r.referrer) || 0) + 1);
  }
  const topPages = [...topPagesMap.entries()].sort((a,b)=>b[1]-a[1]).slice(0,10).map(([path,views])=>({path,views}));
  const topReferrers = [...refMap.entries()].sort((a,b)=>b[1]-a[1]).slice(0,10).map(([referrer,visits])=>({referrer,visits}));

  const dailyMap = new Map();
  for (const r of pageViews) {
    const day = String(r.created_at).slice(0,10);
    dailyMap.set(day, (dailyMap.get(day) || 0) + 1);
  }
  const daily = [...dailyMap.entries()].sort((a,b)=>a[0].localeCompare(b[0])).map(([date,views])=>({date,views}));

  return json(res, 200, {
    ok: true,
    totals: {
      pageViews: pageViews.length,
      uniqueSessions,
      capturedEvents: rows.length
    },
    topPages,
    topReferrers,
    daily
  });
}
