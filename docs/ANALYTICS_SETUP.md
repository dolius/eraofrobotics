# Analytics Setup

## Supabase table
Run this in Supabase SQL editor:

```sql
create table public.analytics_events (
  id bigint generated always as identity primary key,
  path text,
  title text,
  referrer text,
  event_type text,
  session_id text,
  ip_address text,
  user_agent text,
  created_at timestamptz not null default now()
);

create index analytics_events_created_at_idx on public.analytics_events (created_at desc);
create index analytics_events_path_idx on public.analytics_events (path);
create index analytics_events_event_type_idx on public.analytics_events (event_type);
```

## What exists in the project
- `/api/track-visit`
- `/api/analytics-summary`
- `/visits.html`

## How it works
- `site.js` records page views to Supabase
- `visits.html` requests summary data from the analytics API
- summaries include page views, sessions, top pages, and referrers
