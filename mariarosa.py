from flask import Flask, render_template, request, redirect, session, flash, url_for

class Macaquinho:
    def __init__(self, nome, cor, valor):
        self.nome = nome
        self.cor = cor
        self.valor = valor

macaquinho1 = Macaquinho('Macaquinho Raposa', 'Amarelo', 44.99)
macaquinho2 = Macaquinho('Macaquinho Bambi', "Cinza estampado", 44.99)
macaquinho3 = Macaquinho('Macaquinho Ursinho Polar', 'Azul Estampado', 44.99)
lista = [macaquinho1, macaquinho2, macaquinho3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Gabriel Santana", "gsaraujo", "admin123*")
usuario2 = Usuario("Andre Santana", "andaraujo", "lafayette33#")
usuario3 = Usuario("Natalie Araujo", "nsaraujo", "jadeGOD7@")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 }

app= Flask(__name__)
app.secret_key = 'rosemary'

@app.route('/')
def index():
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
    macaquinho4 = Macaquinho(nome, cor, valor)
    lista.append(macaquinho4)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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

app.run(debug=True)