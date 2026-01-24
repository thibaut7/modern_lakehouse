FROM bitnamilegacy/spark:3.5.0

USER root

# Install curl
RUN install_packages curl

# Download dependencies
# 1. Iceberg Spark Runtime
RUN curl -sS -L -O https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.5.0/iceberg-spark-runtime-3.5_2.12-1.5.0.jar \
    && mv iceberg-spark-runtime-3.5_2.12-1.5.0.jar /opt/bitnami/spark/jars/

# 2. Hadoop AWS (Check spark jars for hadoop version first, usually 3.3.4 for Spark 3.5)
# Bitnami Spark 3.5 usually ships with Hadoop 3.3.4 libraries.
RUN curl -sS -L -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
    && mv hadoop-aws-3.3.4.jar /opt/bitnami/spark/jars/

# 3. AWS Java SDK Bundle (Compatible with Hadoop 3.3.4)
RUN curl -sS -L -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.540/aws-java-sdk-bundle-1.12.540.jar \
    && mv aws-java-sdk-bundle-1.12.540.jar /opt/bitnami/spark/jars/

# 4. Postgres JDBC
RUN curl -sS -L -O https://jdbc.postgresql.org/download/postgresql-42.7.2.jar \
    && mv postgresql-42.7.2.jar /opt/bitnami/spark/jars/

# Install Python dependencies for simulation script
RUN install_packages python3-pip
RUN pip install boto3 pandas pyarrow

USER 1001
