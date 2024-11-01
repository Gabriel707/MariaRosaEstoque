import os
from mariarosa import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, DecimalField

class FormularioProduto(FlaskForm):
    nome = StringField('Produto', [validators.data_required(), validators.Length(min=1, max=50)])
    cor = StringField('Cor', [validators.data_required(), validators.Length(min=1, max=40)])
    valor = DecimalField('Valor',[validators.input_required(),
                                  validators.NumberRange(min=1, max=1000, message="O valor deve estar entre 0 e 1000")
                                  ])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Usuário', [validators.data_required(), validators.Length(min=1, max=15)])
    senha = PasswordField('Senha', [validators.data_required(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def pega_image(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'foto{id}' in nome_arquivo:
            return nome_arquivo

    return 'foto_padrao.jpg'

def deleta_arquivo(id):
    arquivo = pega_image(id)
    if arquivo != 'foto_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))