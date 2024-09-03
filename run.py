from app import app
from config import Config


if __name__=='__main__':
    if Config.APP_ENV == 'development':
        app.run(debug=True, port=5000)
    else:
        app.run()

        