import os
from mariarosa import app

def pega_image(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'foto{id}' in nome_arquivo:
            return nome_arquivo

    return 'foto_padrao.jpg'

def deleta_arquivo(id):
    arquivo = pega_image(id)
    if arquivo != 'foto_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))