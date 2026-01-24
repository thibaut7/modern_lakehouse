from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, month, year

def main():
    spark = SparkSession.builder \
        .appName("IngestRawToIceberg") \
        .getOrCreate()

    # Configuration is expected to be passed via spark-submit or spark-defaults.conf 
    # but we can print it to verify
    print("Spark Configured. master: ", spark.sparkContext.master)

    # 1. Read Raw Data (Parquet or CSV)
    # We assume data is in s3a://raw-data/nyc-taxi/
    raw_path = "s3a://raw-data/nyc-taxi/"
    
    print(f"Reading raw data from {raw_path}...")
    try:
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(raw_path)
    except Exception as e:
        print(f"Error reading raw data: {e}")
        # Create dummy data if no data exists for demonstration
        print("Creating dummy data for demonstration...")
        data = [
            ("2023-01-01 10:00:00", "2023-01-01 10:15:00", 1.5, 10.0),
            ("2023-01-01 10:30:00", "2023-01-01 10:45:00", 2.0, 15.0),
            ("2023-01-02 11:00:00", "2023-01-02 11:30:00", 5.0, 30.0)
        ]
        columns = ["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance", "total_amount"]
        df = spark.createDataFrame(data, columns)

    # Clean / Transform
    df_clean = df.withColumn("pickup_time", to_timestamp(col("tpep_pickup_datetime"))) \
                 .withColumn("dropoff_time", to_timestamp(col("tpep_dropoff_datetime"))) \
                 .withColumn("trip_date", to_timestamp(col("tpep_pickup_datetime")).cast("date")) \
                 .withColumn("pickup_month", month(col("tpep_pickup_datetime"))) \
                 .withColumn("pickup_year", year(col("tpep_pickup_datetime")))

    # 2. Write to Iceberg
    table_name = "my_catalog.default.nyc_taxi_trips"
    
    print(f"Writing to Iceberg table {table_name}...")
    
    # Create table if not exists (using DataFrameWriterV2 API or SQL)
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS my_catalog.default")
    
    # Append data
    df_clean.writeTo(table_name) \
        .createOrReplace() \
        # .partitionedBy("pickup_year", "pickup_month") \ # Partitioning can be complex on replace
        
    print("Write complete.")
    
    # Verify
    count = spark.table(table_name).count()
    print(f"Total rows in Iceberg table: {count}")

    spark.stop()

if __name__ == "__main__":
    main()
