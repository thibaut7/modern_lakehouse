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
    # JDBC URL should be reachable from Spark worker
    jdbc_url = "jdbc:postgresql://postgres:5432/lakehouse"
    table_destination = "datamart.daily_trip_stats"
    properties = {
        "user": "admin",
        "password": "password",
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
