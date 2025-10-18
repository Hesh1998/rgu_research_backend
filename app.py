# Import dependencies
from flask import Flask
from flask_cors import CORS


# Create Flask application
app = Flask(__name__)
CORS(app)


@app.route("/test", methods=["GET"])
def test():
    query = "select * from dwh.gold.sales_fact left outer join dwh.gold.currency_dim ON dwh.gold.sales_fact.currency_sk = dwh.gold.currency_dim.currency_sk limit 100;"
    return query, 200


# Run Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)