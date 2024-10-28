from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from mariarosa import app, db
from models import Macaquinhos, Usuarios

@app.route('/')
def index():
    lista = Macaquinhos.query.order_by(Macaquinhos.id)
    return render_template('lista.html', titulo='Maria Rosa Estoque', produtos=lista)

@app.route('/novoproduto')
def novoproduto():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novoproduto')))
    return render_template('novoproduto.html', titulo='Novo Produto')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    cor = request.form['cor']
    valor = request.form['valor']

    macaquinho = Macaquinhos.query.filter_by(nome=nome).first()

    if macaquinho:
        flash('Produto já cadastrado.')
        return redirect(url_for('index'))

    novo_macaquinho = Macaquinhos(nome=nome, cor=cor, valor=valor)
    db.session.add(novo_macaquinho)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/foto{novo_macaquinho.id}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    macaquinho = Macaquinhos.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editando Produto', macaquinho=macaquinho)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    macaquinho = Macaquinhos.query.filter_by(id=request.form['id']).first()
    macaquinho.nome = request.form['nome']
    macaquinho.cor = request.form['cor']
    macaquinho.valor = request.form['valor']

    db.session.add(macaquinho)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Macaquinhos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Produto deletado com sucesso!')

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
         flash('Falha no login, por favor verifique seu login e/ou senha.')
         return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory(app.config['UPLOAD_PATH'], nome_arquivo)