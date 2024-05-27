import boto3
import os
import logging

aws_access_key_id = 'your own'
aws_secret_access_key = 'your own'
bucket_name = 'savyour-receipt'
download_directory = '/home/gaditek/Receipt-Scanner/CustomerDataset/'  
# file_path='/home/gaditek/Receipt-Scanner/sampleData.txt'
file_path='/home/gaditek/Receipt-Scanner/sampleData_v2.txt'

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

s3_client = session.client('s3')

with open(file_path, 'r') as file:
    lines = file.readlines()

count = 0
for line in lines:
    content=line.strip()
    file_extension = os.path.splitext(content)[1].lower()  
    if file_extension in ['.png', '.jpeg', '.jpg']:
        key_segments = content.split('/')
        print(key_segments)
        brand = key_segments[4] 
        outlet = key_segments[5] 

        print("brand",brand)
        print("outlet",outlet)
        
        brand_folder = os.path.join(download_directory, brand)
        outlet_folder = os.path.join(brand_folder, outlet)
        os.makedirs(outlet_folder, exist_ok=True)

        
        local_file_name = os.path.join(outlet_folder, content.split('/')[-1])
        print(local_file_name)
        try:
            s3_client.download_file(bucket_name, content, local_file_name)
            count += 1
            print(f"Object '{content}' downloaded successfully.")
        except Exception as e:
            print(f"Error downloading '{content}': {e}")

        if count==4000:
            break    


print(count)