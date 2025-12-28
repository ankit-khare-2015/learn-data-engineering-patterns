-- Load landed CSV file into bronze table
-- Example assumes psql \copy from mounted data file
\copy bronze.provider_device_catalog (provider_id, device_id, device_name, device_type, last_updated) \
    FROM 'data/provider_device_catalog.csv' DELIMITER ',' CSV HEADER;
