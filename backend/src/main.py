from flask import Flask

from backend.src.resource.ScoringResource import ScoringResource


def main():
    # Create the Flask app

    app = Flask(__name__)

    # Create the API
    api = ScoringResource(app)

    app.run(debug=True)


if __name__ == '__main__':
    main()
