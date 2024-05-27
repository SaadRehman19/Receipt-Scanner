import pandas as pd
import boto3
import os

aws_access_key_id = 'your own'
aws_secret_access_key = 'your own'
bucket_name = 'savyour-prod'
download_directory = '/home/gaditek/Receipt-Scanner/ReceiptDataset/'  
file_path='/home/gaditek/Receipt-Scanner/receiptSample.txt'

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

s3_client = session.client('s3')

df = pd.read_csv('/home/gaditek/Downloads/sample recipts.csv')


for index, row in df.iterrows():
    brand=row['title']
    outlet=row['slug']
    content=row['receipt_sample']

    file_extension = os.path.splitext(content)[1].lower()  
    if file_extension in ['.png', '.jpeg', '.jpg']:
        brand_folder = os.path.join(download_directory, brand)
        outlet_folder = os.path.join(brand_folder, outlet)

        os.makedirs(outlet_folder, exist_ok=True)
        local_file_name = os.path.join(outlet_folder, content.split('/')[-1])
        print(local_file_name)
        try:
            s3_client.download_file(bucket_name, content, local_file_name)
            print(f"Object '{content}' downloaded successfully.")
        except Exception as e:
            print(f"Error downloading '{content}': {e}")