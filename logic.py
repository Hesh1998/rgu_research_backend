import boto3, json
from openai import OpenAI
import gpt_prompt
    
client_sm = boto3.client('secretsmanager', region_name='ap-southeast-1')

def get_response(llm, question):
    if llm == "gpt-5":
        return get_query_gpt(question)
    else:
        return "Error: Unsupported LLM specified."

def get_query_gpt(question):
    secret = client_sm.get_secret_value(SecretId='rgu/research/openai')
    creds = json.loads(secret['SecretString'])
    
    client_gpt = OpenAI(api_key=creds['key'])

    response = client_gpt.chat.completions.create(
        model="gpt-5",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": gpt_prompt.content_system.strip()},
            {"role": "user", "content": gpt_prompt.content_user.strip() + " " + question.strip()}
        ]
    )

    response_text = response.choices[0].message.content
    json_object = json.loads(response_text)
    key, query = next(iter(json_object.items()))
    return query