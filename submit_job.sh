#!/bin/bash
# Usage: ./submit_job.sh /path/to/job.py (path inside container or relative to volume mount)

JOB_PATH=$1

if [ -z "$JOB_PATH" ]; then
  echo "Usage: ./submit_job.sh <path_to_job.py>"
  exit 1
fi

docker exec lakehouse-spark-master spark-submit \
    --master spark://spark-master:7077 \
    --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
    --conf spark.sql.catalog.my_catalog=org.apache.iceberg.spark.SparkCatalog \
    --conf spark.sql.catalog.my_catalog.type=jdbc \
    --conf spark.sql.catalog.my_catalog.uri=jdbc:postgresql://postgres:5432/lakehouse \
    --conf spark.sql.catalog.my_catalog.jdbc.user=admin \
    --conf spark.sql.catalog.my_catalog.jdbc.password=password \
    --conf spark.sql.catalog.my_catalog.warehouse=s3a://warehouse/ \
    --conf spark.sql.catalog.my_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO \
    --conf spark.sql.catalog.my_catalog.s3.endpoint=http://minio:9000 \
    --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
    --conf spark.hadoop.fs.s3a.access.key=admin \
    --conf spark.hadoop.fs.s3a.secret.key=password \
    --conf spark.hadoop.fs.s3a.path.style.access=true \
    --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
    --conf spark.hadoop.fs.s3a.connection.ssl.enabled=false \
    --verbose \
    $JOB_PATH
