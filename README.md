# Data Engineering Patterns

This repo collects simple, repeatable patterns for data engineering. Each pattern has its own folder with architecture notes, runnable assets, SQL, and code.

## Patterns
- Data ingestion: full load with atomic swap (`patterns/01-full-load/`)
  - Bronze keeps every batch (append-only history)
  - Silver and publish hold only the latest batch for stable consumer reads
  - Includes Docker setup, SQL steps, Python runner, and runbook

More patterns will be added under `patterns/` following the same structure.
