# Import dependencies
from flask import Flask, request, jsonify
from flask_cors import CORS
import logic


# Create Flask application
app = Flask(__name__)
CORS(app)


# Endpoint to query data warehouse using NL
@app.route("/query_dwh", methods=["POST"])
def query_dwh():
    data = request.get_json()
    llm = data.get("llm")
    question = data.get("question")

    try:
        query = logic.get_query(llm, question)
        result = logic.get_query_result(query)

        response = {
            "query": query,
            "result": result
        }

        return jsonify(response), 200
    except Exception as e:
        return str(e), 500


@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    llm = data.get("llm")
    question = data.get("question")

    try:
        query = logic.get_query(llm, question)

        return query, 200
    except Exception as e:
        return str(e), 500


# Run Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)