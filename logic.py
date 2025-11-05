# Import dependencies
import boto3, json
from openai import OpenAI
from google import genai
import anthropic
import gpt_prompt, gemini_prompt, claude_prompt
from databricks import sql


# AWS Secrets Manager client
client_sm = boto3.client('secretsmanager', region_name='ap-southeast-1')


# Generate the SQL query using the selected LLM based on the NL question
def get_query(llm, question):
    if llm == "gpt-5":
        return get_query_gpt(question)
    elif llm == "gem-2.5-pro":
        return get_query_gemini(question)
    elif llm == "opus-4.1":
        return get_query_claude(question)
    else:
        return "Error: Unsupported LLM specified."


# SQL query generation using OpenAI GPT-5
def get_query_gpt(question):
    print("Generating query using OpenAI GPT-5")

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


# SQL query generation using Google Gemini 2.5 Pro
def get_query_gemini(question):
    print("Generating query using Google Gemini 2.5 Pro")

    secret = client_sm.get_secret_value(SecretId='rgu/research/gemini')
    creds = json.loads(secret['SecretString'])

    client_gemini = genai.Client(api_key=creds['key'])

    response = client_gemini.models.generate_content(
        model="gemini-2.5-pro",
        contents=gemini_prompt.content.strip() + " " + question.strip(),
        config={
            "response_mime_type": "application/json"
        },
    )
    
    json_object = json.loads(response.text)
    key, query = next(iter(json_object.items()))
    return query


# SQL query generation using Anthropic Claude Opus 4.1
def get_query_claude(question):
    print("Generating query using Anthropic Claude Opus 4.1")

    secret = client_sm.get_secret_value(SecretId='rgu/research/claude')
    creds = json.loads(secret['SecretString'])

    client_claude = anthropic.Anthropic(api_key=creds['key'],)

    response = client_claude.messages.create(
        model="claude-opus-4-1",
        max_tokens=2048,
        system=claude_prompt.content_system.strip(),
        messages=[
            {"role": "user", "content": claude_prompt.content_user.strip() + " " + question.strip()}
        ]
    )

    response_text = response.content[0].text
    return response_text


# Execute the SQL query on Databricks and return the result
def get_query_result(query):
    secret = client_sm.get_secret_value(SecretId='rgu/research/databricks')
    creds = json.loads(secret['SecretString'])
    token = creds['key']

    connection = sql.connect(
                            server_hostname = "dbc-c7a0eacf-9a5e.cloud.databricks.com",
                            http_path = "/sql/1.0/warehouses/bed6110085302b78",
                            access_token = token)

    cursor = connection.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    connection.close()

    return result