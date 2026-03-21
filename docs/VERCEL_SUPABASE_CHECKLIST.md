# Vercel + Supabase deployment checklist

## 1) Supabase setup
Open the Supabase SQL editor and run:
- `supabase/leads_schema.sql`

Verify the table exists:
- `public.leads`

Recommended quick check:
```sql
select column_name, data_type
from information_schema.columns
where table_schema = 'public' and table_name = 'leads'
order by ordinal_position;
```

## 2) Vercel environment variables
Set these environment variables in Vercel for the project:
- `SUPABASE_URL`
- `SUPABASE_SECRET_KEY`

Do not expose the secret key to client-side code.

## 3) Deploy shape
This repo expects:
- static files served from repo root
- serverless endpoint at `api/capture-lead.js`

Public form target:
- `/api/capture-lead`

## 4) Post-deploy smoke test
Once deployed, test the endpoint with:
```bash
curl -i -X POST "https://YOUR-DOMAIN/api/capture-lead" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "email=test+eraofrobotics@example.com&persona=operator&source=robotics-brief-download&interest=robotics-brief&stage=brief-captured"
```

Expected behavior:
- HTTP `303`
- `Location: /brief-unlocked.html`

Then verify the row exists in Supabase:
```sql
select email, source, persona, interest, stage, created_at
from public.leads
order by created_at desc
limit 10;
```

## 5) Browser flow test
Open:
- `/robotics-brief-download.html`

Submit a test email and verify:
1. redirect to `brief-unlocked.html`
2. brief button works
3. premium page button works
4. row appears in Supabase

## 6) Failure cases to test
- invalid email
- duplicate email submit
- missing env vars in deployment
- Supabase table missing

## 7) Notes
- The endpoint normalizes emails to lowercase before write.
- The endpoint is intended for server-side writes using the Supabase service role key.
- Legacy local SQLite capture still exists for offline/local-only testing, but production should use Supabase.
