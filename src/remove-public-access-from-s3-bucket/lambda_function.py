import boto3
import json

def lambda_handler(event, context):
    # Replace with the name of the S3 bucket
    body = json.loads(event['body'])
    BUCKET_NAME = body.get('bucketName')
    print (BUCKET_NAME)

    # Create an S3 client
    s3 = boto3.client('s3')
    try:
    # Set the public access block configuration
        response = s3.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        print(f"Public access to bucket '{BUCKET_NAME}' has been restricted.")
        print (1)
        response_body = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json' },
            'body': json.dumps({"message": f"Public access to S3 bucket restricted successfully"})
        } 
        return response_body
        
    except Exception as e:    
        response_body = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json' },
            'body': json.dumps({"message": f"The buket doesn't exist or has no public access"})
        } 
        return response_body