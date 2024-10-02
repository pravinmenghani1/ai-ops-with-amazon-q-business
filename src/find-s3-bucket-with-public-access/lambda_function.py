import boto3
import json

# Create an S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):

    body = json.loads(event['body'])
    bucketPrefix = body.get('bucketPrefix')
    print (bucketPrefix)

    
    # Get a list of all S3 buckets
    response = s3.list_buckets()
    buckets = response['Buckets']

    # Loop through the buckets and check for public access
    bucketPrefix_buckets = []
    for bucket in buckets:
        bucket_name = bucket['Name']
        
        if bucket_name.startswith(bucketPrefix):
            try:
                # Check the bucket's public access block settings
                public_access_block = s3.get_public_access_block(Bucket=bucket_name)
                if (
                    public_access_block['PublicAccessBlockConfiguration']['BlockPublicAcls'] is False or
                    public_access_block['PublicAccessBlockConfiguration']['IgnorePublicAcls'] is False or
                    public_access_block['PublicAccessBlockConfiguration']['BlockPublicPolicy'] is False or
                    public_access_block['PublicAccessBlockConfiguration']['RestrictPublicBuckets'] is False
                ):
                   print("Public:"+bucket_name)
                   bucketPrefix_buckets.append(bucket_name)
            except s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                    print(e)

    # Return the list of buckets with public access
    print("Final")
    print(bucketPrefix_buckets)
    response_body = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json' },
            'body': json.dumps({"bucketPrefix_buckets": bucketPrefix_buckets})
            }        
        
    return response_body
