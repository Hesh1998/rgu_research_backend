# Import dependencies
from flask import Flask
from flask_cors import CORS
import boto3, json, base64, botocore


# Create Flask application
app = Flask(__name__)
CORS(app)


@app.route("/test", methods=["GET"])
def test():
    session = boto3.Session(profile_name='aws-cli-user', region_name='ap-southeast-1')
    client = session.client("secretsmanager")

    try:
        secret = client.get_secret_value(SecretId='rgu/research/openai')
        return secret, 200
    except botocore.exceptions.ClientError as e:
        return str(e), 500

# Run Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)