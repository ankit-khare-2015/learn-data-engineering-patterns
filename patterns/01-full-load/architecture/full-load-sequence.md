# Full Load Sequence

1. Extract provider device catalog from the source system.
2. Land raw file to object storage with metadata (batch id, received at).
3. Ingest raw file into bronze table with minimal transformation.
4. Build silver staging table applying schema alignment and type casting.
5. Run quality checks (rowcount, schema contract, freshness).
6. Publish refreshed table via atomic swap to keep consumers isolated from load churn.
