# Full Load State Machine

- **INIT** → acquire batch metadata and validate source availability.
- **LAND_RAW** → place source file/object into landing zone with checksum.
- **INGEST_BRONZE** → load file into bronze table; capture ingest log.
- **BUILD_SILVER** → transform bronze records into conformed staging table.
- **QUALITY_CHECKS** → enforce schema contract and rowcount thresholds.
- **ATOMIC_SWAP** → replace consumer-facing table with freshly built version.
- **SUCCESS** → emit completion event; archive raw artifacts.
- **FAILURE** → stop pipeline, raise alert, preserve diagnostics for triage.
