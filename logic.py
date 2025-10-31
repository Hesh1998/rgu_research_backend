import boto3, json
from openai import OpenAI
import gpt_prompt
    
client_sm = boto3.client('secretsmanager', region_name='ap-southeast-1')

def get_query_gpt():
    secret = client_sm.get_secret_value(SecretId='rgu/research/openai')
    creds = json.loads(secret['SecretString'])
    
    client_gpt = OpenAI(api_key=creds['key'])

    # response = client_gpt.responses.create(
    #     model="gpt-5",
    #     input="What is the capital of France?"
    # )

    content_system = """
    You are an intelligent assistant that always returns answers in a valid JSON format.
    Each JSON must contain a single key-value pair where the key is a short identifier
    (like 'answer' or 'query') and the value is the response content.
    """

    content_user = """
    What is the capital of France?
    """

    response = client_gpt.responses.create(
        model="gpt-5",
        response_format={ "type": "json_object" },
        input=[
            {"role": "system", "content": f"{content_system}"},
            {"role": "user", "content": f"{content_user}"}
        ]
    )

    return response.output_text