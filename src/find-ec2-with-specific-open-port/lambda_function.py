import boto3
import json

def lambda_handler(event, context):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')
    response_body={}
    # Get a list of all EC2 instances
    response = ec2.describe_instances()
    print(event)
    receivedPortNumber = event['queryStringParameters']['portNumber']
    print(receivedPortNumber)
    receivedPortNumberFormat = int(receivedPortNumber)
    print(receivedPortNumberFormat)
    # Initialize an empty list to store instances with port open
    instances_with_port_open = []

    # Loop through the instances
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(instance['InstanceId'])
            # Check if the instance has port open
            try:
                security_groups = instance['SecurityGroups']
                for security_group in security_groups:
                    security_group_id = security_group['GroupId']
                    security_group_details = ec2.describe_security_groups(GroupIds=[security_group_id])
                    for ip_permission in security_group_details['SecurityGroups'][0]['IpPermissions']:
                        print(ip_permission)
                        if ip_permission['FromPort'] <= receivedPortNumberFormat and ip_permission['ToPort'] >= receivedPortNumberFormat:
                            print("Found");
                            print(instance['InstanceId'])
                            instances_with_port_open.append(instance['InstanceId'])
                            print("FoundX");
                            print("1")
                            print(instances_with_port_open)
                            break
            except Exception as e:
                print(e)

    # Return the list of instances with port open
    print(instances_with_port_open)
    response_body = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json' },
            'body': json.dumps({"instances_with_port_open": instances_with_port_open})
            }

    return response_body