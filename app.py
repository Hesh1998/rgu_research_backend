# Import dependencies
from flask import Flask, request
from flask_cors import CORS
import logic


# Create Flask application
app = Flask(__name__)
CORS(app)


@app.route("/query_dwh", methods=["POST"])
def query_dwh():
    data = request.get_json()
    llm = data.get("llm")
    question = data.get("question")

    try:
        query = logic.get_query(llm, question)
        response = logic.get_query_result(query)
        return response, 200
    except Exception as e:
        return str(e), 500


# Run Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)