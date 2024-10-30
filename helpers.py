import os
from mariarosa import app

def pega_image(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'foto{id}.jpg' == nome_arquivo:
            return nome_arquivo

    return 'foto_padrao.jpg'