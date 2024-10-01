import boto3
import json

def lambda_handler(event, context):
    # Get the port number to close from the event
    body = json.loads(event['body'])
    port_to_close_str = body.get('port_to_close')
    port_to_close = int(port_to_close_str)
    print (port_to_close)
    

    # Initialize the EC2 client
    ec2 = boto3.client('ec2')

    # Get the instance ID from the event
    instance_id = body.get('instance_id')
    print(instance_id)
    
    # Get the security groups for the instance
    response = ec2.describe_instances(InstanceIds=[instance_id])
    security_groups = [sg['GroupId'] for reservation in response['Reservations'] for instance in reservation['Instances'] for sg in instance['SecurityGroups']]

    # Loop through the security groups and check for the specified port
    for security_group_id in security_groups:
     print("100")
     try:
        # Get the security group details
        security_group = ec2.describe_security_groups(GroupIds=[security_group_id])['SecurityGroups'][0]
        print(200)
        # Check if the security group has a rule for the specified port
        for permission in security_group['IpPermissions']:
            if permission['FromPort'] <= port_to_close <= permission['ToPort']:
                print(300)
                print(f"Found security group {security_group['GroupName']} with port {port_to_close} open.")
                
                # Remove the rule
                ec2.revoke_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[permission]
                )
                print(f"Removed rule for port {port_to_close} from security group {security_group['GroupName']}.")
                response_body = {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json' },
                    'body': json.dumps({"message": f"Removed rule for port {port_to_close} on Instance {instance_id} from security group {security_group['GroupName']}"})
                }
                return response_body
                
     except Exception as e:
        print(f"Error processing security group {security_group_id}: {e}")
        # If we reach this point, the port was not found open
        response_body = {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json' },
                    'body': json.dumps({"message": f"Port {port_to_close} is not open on instance {instance_id} or some error"})
        }
        return response_body
    
    response_body = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json' },
            'body': json.dumps({"message": f"Port {port_to_close} is not open on Instance {instance_id}"})
        }
    return response_body