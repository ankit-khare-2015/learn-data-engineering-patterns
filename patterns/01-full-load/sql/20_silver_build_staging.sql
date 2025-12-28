TRUNCATE TABLE silver.provider_device_catalog_staging;

INSERT INTO silver.provider_device_catalog_staging (provider_id, device_id, device_name, device_type, last_updated, batch_id)
SELECT
    provider_id,
    device_id,
    INITCAP(device_name) AS device_name,
    device_type,
    last_updated,
    :batch_id AS batch_id
FROM bronze.provider_device_catalog
WHERE batch_id = :batch_id;
