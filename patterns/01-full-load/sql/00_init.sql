-- Initialize schemas and base tables for the full-load pattern
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS publish;
CREATE SCHEMA IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS bronze.provider_device_catalog (
    provider_id   INTEGER,
    device_id     TEXT,
    device_name   TEXT,
    device_type   TEXT,
    last_updated  TIMESTAMPTZ,
    batch_id      TEXT,
    _ingested_at  TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE bronze.provider_device_catalog ADD COLUMN IF NOT EXISTS batch_id TEXT;

CREATE TABLE IF NOT EXISTS silver.provider_device_catalog_staging (
    provider_id   INTEGER,
    device_id     TEXT,
    device_name   TEXT,
    device_type   TEXT,
    last_updated  TIMESTAMPTZ,
    batch_id      TEXT,
    loaded_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS metadata.batch_state (
    state_key     TEXT PRIMARY KEY,
    last_batch_id TEXT,
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);
