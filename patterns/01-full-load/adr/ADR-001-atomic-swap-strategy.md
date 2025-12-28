# ADR-001: Atomic Swap Strategy

## Context
Full refresh loads can produce transient states where consumer tables are partially updated. We need a predictable way to publish refreshed data without exposing half-finished batches.

## Decision
Stage the refreshed dataset in `silver.provider_device_catalog_staging`, then atomically swap it into the `publish` schema using table renames inside a single transaction. Consumers always read from `publish.provider_device_catalog` and never see intermediate states.

## Consequences
- Positive: removes need for consumer coordination; minimizes downtime.
- Positive: enables quick rollback by keeping prior table available before drop.
- Negative: requires duplicate storage for the staging copy during swap.
- Negative: swap is limited to systems that support transactional DDL.
