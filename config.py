import os

SECRET_KEY = 'rosemary'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin123*',
        servidor = 'localhost',
        database = 'mariarosa'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'