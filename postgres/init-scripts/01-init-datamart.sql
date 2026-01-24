-- Create Datamart schema
CREATE SCHEMA IF NOT EXISTS datamart;

-- Create Iceberg Catalog schema (if we were using a custom catalog table, but JDBC catalog handles its own tables usually in public or specified schema)
-- We will point Iceberg to use the 'public' schema or a dedicated 'iceberg' schema for its metadata tables.
CREATE SCHEMA IF NOT EXISTS iceberg_catalog;

-- Table for 'processed' data (Datamart example)
-- We'll let Spark create this or create a structure now.
-- Let's create a simple table structure for the NYC Taxi aggregation example.
CREATE TABLE IF NOT EXISTS datamart.daily_trip_stats (
    trip_date DATE PRIMARY KEY,
    total_trips INTEGER,
    avg_fare DOUBLE PRECISION,
    max_fare DOUBLE PRECISION,
    total_revenue DOUBLE PRECISION,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
