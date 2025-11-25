import os
from src.main.server.server import app

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


if "__main__" == __name__:

    app.run(debug=True, host=HOST, port=PORT)