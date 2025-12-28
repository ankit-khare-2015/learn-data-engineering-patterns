# Full Load with Atomic Swap

This pattern loads the device catalog with a full refresh while keeping consumers stable through an atomic swap of the publish table. 
## What the layers hold
- Bronze (append-only): every batch ever loaded, stamped with `batch_id` and `_ingested_at`.
- Silver (current batch): only rows for the latest batch id.
- Publish (current batch): same rows as silver, swapped in one transaction.
- Batch state: `metadata.batch_state` stores the last batch id used.

## Example query results
- Bronze keeps history (all batches):
  - `SELECT * FROM bronze.provider_device_catalog;`
  - Example rows include multiple `batch_id` values:
    - `... | 401 | D-401 | Beacon X | Sensor | ... | 1766922992`
    - `... | 101 | D-001 | Beacon X | Sensor | ... | 1766923034`
    - `... | 206 | D-010 | Handheld Alpha | Handheld | ... | 1766923034`
- Silver shows only the latest batch:
  - `SELECT * FROM silver.provider_device_catalog_staging;` → batch `1766923034` only.
- Publish shows only the latest batch (after swap):
  - `SELECT * FROM publish.provider_device_catalog;` → batch `1766923034` only.

## How to run
1) Start Postgres: `docker compose -f docker/docker-compose.yml up -d`
2) Create venv and install deps: `bash setup_env.sh && source .venv/bin/activate`
3) Run pipeline: `python src/full_load_job.py --batch-id $(date +%s)` (or omit `--batch-id` to reuse the last saved one)
4) Check data:
   - Bronze history: `SELECT COUNT(*) FROM bronze.provider_device_catalog;`
   - Current batch: `SELECT batch_id, COUNT(*) FROM silver.provider_device_catalog_staging GROUP BY batch_id;`
   - Published view: `SELECT * FROM publish.provider_device_catalog;`

## Files to know
- Architecture: `architecture/full-load-sequence.md`, `architecture/full-load-state-machine.md`
- ADR: `adr/ADR-001-atomic-swap-strategy.md`
- Runbook: `runbook/operations.md`, `runbook/troubleshooting.md`
- Code/SQL: `src/full_load_job.py`, `src/config.yaml`, `sql/00_init.sql` → `sql/40_atomic_swap.sql`
- Data: `data/provider_device_catalog.csv`
