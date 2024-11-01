from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from mariarosa import app, db
from models import Macaquinhos
from helpers import pega_image, deleta_arquivo, FormularioProduto
import time

@app.route('/')
def index():
    lista = Macaquinhos.query.order_by(Macaquinhos.id)
    return render_template('lista.html', titulo='Maria Rosa Estoque', produtos=lista)

@app.route('/novoproduto')
def novoproduto():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novoproduto')))
    form = FormularioProduto()
    return render_template('novoproduto.html', titulo='Novo Produto', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioProduto(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novoproduto'))

    nome = form.nome.data
    cor = form.cor.data
    valor = form.valor.data

    macaquinho = Macaquinhos.query.filter_by(nome=nome).first()

    if macaquinho:
        flash('Produto já cadastrado.')
        return redirect(url_for('index'))

    novo_macaquinho = Macaquinhos(nome=nome, cor=cor, valor=valor)
    db.session.add(novo_macaquinho)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/foto{novo_macaquinho.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    macaquinho = Macaquinhos.query.filter_by(id=id).first()
    form = FormularioProduto()
    form.nome.data = macaquinho.nome
    form.cor.data = macaquinho.cor
    form.valor.data = macaquinho.valor
    foto_produto = pega_image(id)
    return render_template('editar.html', titulo='Editando Produto', id=id, foto_produto=foto_produto, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioProduto(request.form)

    if form.validate_on_submit():
        macaquinho = Macaquinhos.query.filter_by(id=request.form['id']).first()
        macaquinho.nome = form.nome.data
        macaquinho.cor = form.cor.data
        macaquinho.valor = form.valor.data

        db.session.add(macaquinho)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(macaquinho.id)
        arquivo.save(f'{upload_path}/foto{macaquinho.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Macaquinhos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Produto deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory(app.config['UPLOAD_PATH'], nome_arquivo)
