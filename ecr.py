import boto3


# Create an STS client
sts_client = boto3.client('sts')

# Specify the ARN of the IAM role to assume
role_arn = 'arn:aws:iam::xxxxxxxxxxxx:user/zero-t-hero'

# Assume the IAM role to get temporary credentials
assumed_role = sts_client.assume_role(
    RoleArn=role_arn,
    RoleSessionName='AssumeRoleSession'
)

# Extract temporary credentials from the assumed role
credentials = assumed_role['Credentials']

ecr_client = boto3.client(
    'ecr',
    region_name='us-east-1',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)

repository_name = "berlin_store_locator_api"

response = ecr_client.create_repository(repositoryName=repository_name)

repository_uri = response['repository']['repositoryUri']

print(repository_uri)
