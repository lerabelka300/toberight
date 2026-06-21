-- ═══════════════════════════════════════════════════════════
--  SUPABASE SETUP — выполни в SQL Editor
-- ═══════════════════════════════════════════════════════════

-- ── 1. Таблица задач (канбан) ────────────────────────────
create table if not exists tasks (
  id          uuid primary key default gen_random_uuid(),
  status      text not null default 'backlog',
  position    int  not null default 0,
  title       text not null default '',
  cat         text,
  prio        text,
  date        text,
  time        text,
  description text,
  estimate    text,
  start_date  text,
  start_time  text,
  created_at  timestamptz default now()
);

alter table tasks add column if not exists extra jsonb default '{}';

alter table tasks enable row level security;

create policy "tasks: allow all"
  on tasks for all
  using (true)
  with check (true);

-- ── 2. Таблица записей настроения ───────────────────────
create table if not exists mood_entries (
  id               uuid primary key default gen_random_uuid(),
  date             timestamptz default now(),
  mood             int,
  emotions         text[],
  factors          text[],
  symptoms         text[],
  cycle_day        int,
  cycle_phase      text,
  sleep_hours      numeric,
  sleep_quality    int,
  energy           int,
  stress           int,
  anxiety          int,
  productivity     int,
  note             text,
  main_influence   text,
  support_tomorrow text
);

alter table mood_entries enable row level security;

create policy "mood: allow all"
  on mood_entries for all
  using (true)
  with check (true);

-- ── 3. Состояние приложения (планер, parkinglot и др.) ──
create table if not exists app_state (
  key        text primary key,
  value      jsonb,
  updated_at timestamptz default now()
);

alter table app_state enable row level security;

create policy "app_state: allow all"
  on app_state for all
  using (true)
  with check (true);

-- ── 4. Финансовые транзакции ─────────────────────────────
create table if not exists finance_transactions (
  id          uuid primary key default gen_random_uuid(),
  tx_date     date not null,
  description text,
  amount      numeric(12,2) not null,
  category    text,
  month_key   text,        -- 'YYYY-MM' для группировки
  source      text default 'pdf',  -- 'pdf' | 'manual'
  created_at  timestamptz default now()
);

alter table finance_transactions enable row level security;

create policy "finance: allow all"
  on finance_transactions for all
  using (true)
  with check (true);
