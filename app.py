# Import dependencies
from flask import Flask
from flask_cors import CORS


# Create Flask application
app = Flask(__name__)
CORS(app)


@app.route("/test", methods=["GET"])
def test():
    return "Success", 200


# Run Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)