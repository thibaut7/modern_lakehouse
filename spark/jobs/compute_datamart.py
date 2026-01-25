from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, max, sum as _sum

def main():
    spark = SparkSession.builder \
        .appName("ComputeDatamart") \
        .getOrCreate()

    # 1. Read from Iceberg
    table_name = "my_catalog.default.nyc_taxi_trips"
    print(f"Reading from Iceberg table {table_name}...")
    
    df = spark.table(table_name)

    # 2. Aggregate
    # Daily stats: total trips, avg fare, max fare, total revenue
    daily_stats = df.groupBy("trip_date") \
        .agg(
            count("*").alias("total_trips"),
            avg("total_amount").alias("avg_fare"),
            max("total_amount").alias("max_fare"),
            _sum("total_amount").alias("total_revenue")
        ) \
        .orderBy("trip_date")

    daily_stats.show()

    # 3. Write to Postgres Datamart
    import os
    pg_user = os.getenv("POSTGRES_USER", "admin")
    pg_pass = os.getenv("POSTGRES_PASSWORD", "password")
    pg_db = os.getenv("POSTGRES_DB", "lakehouse")

    jdbc_url = f"jdbc:postgresql://postgres:5432/{pg_db}"
    table_destination = "datamart.daily_trip_stats"
    properties = {
        "user": pg_user,
        "password": pg_pass,
        "driver": "org.postgresql.Driver"
    }

    print(f"Writing to Postgres table {table_destination}...")

    daily_stats.write \
        .mode("overwrite") \
        .jdbc(jdbc_url, table_destination, properties=properties)

    print("Datamart update complete.")
    spark.stop()

if __name__ == "__main__":
    main()
