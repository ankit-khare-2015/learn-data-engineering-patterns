-- Atomically swap refreshed staging table into publish schema
BEGIN;
    CREATE TABLE IF NOT EXISTS publish.provider_device_catalog AS
    TABLE silver.provider_device_catalog_staging WITH NO DATA;

    CREATE TABLE publish.provider_device_catalog_new AS
    SELECT * FROM silver.provider_device_catalog_staging;

    ALTER TABLE publish.provider_device_catalog RENAME TO provider_device_catalog_old;
    ALTER TABLE publish.provider_device_catalog_new RENAME TO provider_device_catalog;
    DROP TABLE publish.provider_device_catalog_old;
COMMIT;
