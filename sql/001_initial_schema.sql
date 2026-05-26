CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS search_runs (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  job_description text NOT NULL,
  profile jsonb NOT NULL,
  status text NOT NULL DEFAULT 'created',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS candidates (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  source text NOT NULL,
  source_id text NOT NULL,
  full_name text NOT NULL,
  title text,
  location text,
  languages text[] NOT NULL DEFAULT '{}',
  skills text[] NOT NULL DEFAULT '{}',
  domains text[] NOT NULL DEFAULT '{}',
  education text,
  publications integer NOT NULL DEFAULT 0,
  citations integer NOT NULL DEFAULT 0,
  h_index integer NOT NULL DEFAULT 0,
  github_stars integer NOT NULL DEFAULT 0,
  leadership integer NOT NULL DEFAULT 0,
  years_experience integer NOT NULL DEFAULT 0,
  profile_url text,
  raw_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  embedding vector(384),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (source, source_id)
);

CREATE TABLE IF NOT EXISTS candidate_evaluations (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  run_id uuid NOT NULL REFERENCES search_runs(id) ON DELETE CASCADE,
  candidate_id uuid NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
  score numeric(5, 2) NOT NULL,
  scores jsonb NOT NULL,
  matched_skills text[] NOT NULL DEFAULT '{}',
  matched_domains text[] NOT NULL DEFAULT '{}',
  reasons text[] NOT NULL DEFAULT '{}',
  outreach_draft text NOT NULL DEFAULT '',
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (run_id, candidate_id)
);

CREATE TABLE IF NOT EXISTS outreach_events (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  candidate_id uuid NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
  run_id uuid REFERENCES search_runs(id) ON DELETE SET NULL,
  channel text NOT NULL,
  status text NOT NULL,
  message text NOT NULL,
  response text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS candidates_full_name_trgm_idx ON candidates USING gin (full_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS candidates_skills_idx ON candidates USING gin (skills);
CREATE INDEX IF NOT EXISTS candidates_domains_idx ON candidates USING gin (domains);
CREATE INDEX IF NOT EXISTS candidate_evaluations_run_score_idx ON candidate_evaluations (run_id, score DESC);

