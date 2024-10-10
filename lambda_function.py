import boto3
          import json
          
          # Function to assume a role in the Management Account and return temporary credentials
          def assume_role(account_id, role_name):
          """Assumes a role in the Management Account and returns temporary credentials."""
          sts_client = boto3.client('sts')
          role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

          response = sts_client.assume_role(
          RoleArn=role_arn,
           RoleSessionName='CrossAccountSession'
          )

          return response['Credentials']

          def lambda_handler(event, context):
          # Specify your Management Account ID and IAM Role Name
          management_account_id = '593793039129'
          role_name = 'CostExplorerAccessRole'  # Replace with the role name created in Management Account

          # Assume the role in the Management Account to get temporary credentials
          credentials = assume_role(management_account_id, role_name)

          # Create Cost Explorer client using the assumed role credentials
          ce = boto3.client(
              'ce',
              aws_access_key_id=credentials['AccessKeyId'],
              aws_secret_access_key=credentials['SecretAccessKey'],
              aws_session_token=credentials['SessionToken'],
              region_name='us-east-1'  # Specify the region where Cost Explorer is supported
          )

          # Create EC2 client using the Lambda function's execution role credentials
          ec2 = boto3.client('ec2')

          # Query Cost Explorer for total cost using the assumed role
          print("Querying Cost Explorer for total cost...")
          response = ce.get_cost_and_usage(
              TimePeriod={
                  'Start': '2024-10-01',
                  'End': '2024-10-10'  # Replace with the date range of interest
              },
              Granularity='MONTHLY',  # Change this to 'DAILY' if you want daily cost details
              Metrics=['BlendedCost']
          )
          print("2")

          # Parse the total cost
          total_cost = float(response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
          print(f"Total cost from Management Account: ${total_cost}")

          # If total cost exceeds the threshold, stop EC2 instances in the Workload Account
          if total_cost > float(event['ALLOCATION_THRESHOLD']):
              print(f"Total cost exceeds threshold. Stopping EC2 instances in Workload Account.")
              
              # Describe EC2 instances in the Workload Account
              ec2_instances = ec2.describe_instances(
                  Filters=[{'Name': 'tag:Name', 'Values': ['CostMonitoredEC2Instance']}]
              )

              # Stop the instances
              for reservation in ec2_instances['Reservations']:
                  for instance in reservation['Instances']:
                      print(f"Stopping EC2 instance: {instance['InstanceId']}")
                      ec2.stop_instances(InstanceIds=[instance['InstanceId']])
          else:
              print(f"Total cost is below the threshold. No action required.")

          return {
              'statusCode': 200,
              'body': json.dumps(f'Total cost: ${total_cost}')
          }