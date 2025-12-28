# Troubleshooting

- **Service unavailable**: ensure Postgres container is healthy via `docker ps` and `docker inspect retail_warehouse`.
- **Load fails**: confirm CSV file path is reachable from container and permissions allow read.
- **Quality checks fail**: inspect `silver.provider_device_catalog_staging` for nulls or unexpected types; rerun upstream extract if needed.
- **Atomic swap issues**: verify no concurrent writers and that `publish` schema exists prior to swap.
