import boto3, json
from openai import OpenAI
import gpt_prompt
from databricks import sql


client_sm = boto3.client('secretsmanager', region_name='ap-southeast-1')


def get_query(llm, question):
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
    #result_text = "\n".join([str(row) for row in rows])
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    result_json = json.dumps(results, indent=2)

    cursor.close()
    connection.close()

    return result_json