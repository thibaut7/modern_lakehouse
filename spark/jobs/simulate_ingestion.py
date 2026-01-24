import sys
import random
import time
from datetime import datetime, timedelta

def install_dependencies():
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "boto3", "pandas"])

try:
    import boto3
    import pandas as pd
except ImportError:
    print("Installing dependencies...")
    install_dependencies()
    import boto3
    import pandas as pd

def generate_trip_data(num_rows=1000):
    data = []
    base_time = datetime(2024, 1, 1)
    
    for _ in range(num_rows):
        pickup_time = base_time + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        dropoff_time = pickup_time + timedelta(minutes=random.randint(5, 60))
        
        trip = {
            'tpep_pickup_datetime': pickup_time.strftime('%Y-%m-%d %H:%M:%S'),
            'tpep_dropoff_datetime': dropoff_time.strftime('%Y-%m-%d %H:%M:%S'),
            'passenger_count': random.randint(1, 4),
            'trip_distance': round(random.uniform(1.0, 20.0), 2),
            'PULocationID': random.randint(1, 263),
            'DOLocationID': random.randint(1, 263),
            'payment_type': random.randint(1, 2),
            'fare_amount': round(random.uniform(5.0, 50.0), 2),
            'tip_amount': round(random.uniform(0.0, 10.0), 2),
            'tolls_amount': 0.0,
            'total_amount': 0.0  # calculated below
        }
        trip['total_amount'] = trip['fare_amount'] + trip['tip_amount'] + trip['tolls_amount']
        data.append(trip)
        
    return pd.DataFrame(data)

def upload_to_minio(df, bucket='raw-data', object_name=None):
    if object_name is None:
        object_name = f"nyc-taxi/trips_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    s3 = boto3.client('s3',
                      endpoint_url='http://minio:9000',
                      aws_access_key_id='admin',
                      aws_secret_access_key='password')
    
    csv_buffer = df.to_csv(index=False)
    
    print(f"Uploading to s3://{bucket}/{object_name}")
    s3.put_object(Bucket=bucket, Key=object_name, Body=csv_buffer)
    print("Upload successful.")

if __name__ == "__main__":
    print("Generating synthetic data...")
    df = generate_trip_data(10000)
    upload_to_minio(df)
