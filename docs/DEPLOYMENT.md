# Deployment steps for Era of Robotics

## Vercel env vars
Add these in Vercel project settings:
- `SUPABASE_URL`
- `SUPABASE_PUBLISHABLE_KEY`
- `SUPABASE_SECRET_KEY`

## Supabase SQL schema
Run this in the Supabase SQL editor:

```sql
create table public.leads (
  id bigint generated always as identity primary key,
  email text not null unique,
  source text,
  persona text,
  interest text,
  stage text,
  created_at timestamptz not null default now(),
  ip_address text,
  user_agent text
);

create index leads_created_at_idx on public.leads (created_at desc);
create index leads_persona_idx on public.leads (persona);
create index leads_interest_idx on public.leads (interest);
create index leads_stage_idx on public.leads (stage);
```

## Production capture flow
- frontend form posts to `/api/capture-lead`
- API route writes to Supabase
- user is redirected to `brief-unlocked.html`
- premium upsell is `premium-robotics-brief.html`
