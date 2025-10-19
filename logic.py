import boto3, json
from openai import OpenAI

client = boto3.client('secretsmanager', region_name='ap-southeast-1')

def get_query_gpt():
    secret = client.get_secret_value(SecretId='rgu/research/openai')
    creds = json.loads(secret['SecretString'])
    
    client = OpenAI(api_key=creds['key'])

    response = client.responses.create(
        model="gpt-5",
        input="What is the capital of France?"
    )

    return response.output_text