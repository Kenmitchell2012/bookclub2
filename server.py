from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import books


if __name__ == "__main__":
    app.run(port=6001, debug=True)