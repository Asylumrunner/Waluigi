import boto3

rds = boto3.client('rds-data')

response = rds.execute_statement(
    database=""
)