# Import dependencies
from flask import Flask
from flask_cors import CORS
import boto3, json, base64
from openai import OpenAI


# Create Flask application
app = Flask(__name__)
CORS(app)


@app.route("/test", methods=["GET"])
def test():
    try:
        client = boto3.client('secretsmanager', region_name='ap-southeast-1')
        secret = client.get_secret_value(SecretId='rgu/research/openai')
        creds = json.loads(secret['SecretString'])

        client = OpenAI(api_key=creds['key'])
        response = client.responses.create(
            model="gpt-5",
            input="Write a short bedtime story about a unicorn."
        )

        return response, 200
    except Exception as e:
        return str(e), 500

# Run Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)