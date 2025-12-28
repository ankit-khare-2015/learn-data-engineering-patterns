# Operations Guide

- Start services: `docker compose -f docker/docker-compose.yml up -d`.
- Run pipeline: `python src/full_load_job.py --batch-id $(date +%s)`.
- Validate: connect to Postgres and review `publish.provider_device_catalog` rowcount.
- Archive: retain landed files with batch metadata for audit purposes.
