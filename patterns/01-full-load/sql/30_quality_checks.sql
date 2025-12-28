-- Basic quality gates for the batch
-- Rowcount must be non-zero
DO $$
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM silver.provider_device_catalog_staging;
    IF v_count = 0 THEN
        RAISE EXCEPTION 'Quality check failed: staging rowcount is zero';
    END IF;
END$$;

-- Schema contract example: ensure required columns are not null
DO $$
DECLARE
    v_nulls INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_nulls
    FROM silver.provider_device_catalog_staging
    WHERE provider_id IS NULL OR device_id IS NULL;
    IF v_nulls > 0 THEN
        RAISE EXCEPTION 'Quality check failed: required columns contain nulls';
    END IF;
END$$;
