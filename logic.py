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
                    You are an expert SQL generator.
                    Given a database schema and a natural language question,
                    you must produce a valid SQL query that can be executed on that schema.

                    Output must be a valid JSON object in this exact format:
                    {
                    "query": "SELECT ..."
                    }

                    Do not include explanations, comments, or any other text.
                    """

    content_user = """
    What is the product with most sales?
    """

    response = client_gpt.chat.completions.create(
        model="gpt-5",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": content_system.strip()},
            {"role": "user", "content": content_user.strip()}
        ]
    )

    response_text = response.choices[0].message.content
    json_object = json.loads(response_text)
    key, query = next(iter(json_object.items()))
    return query