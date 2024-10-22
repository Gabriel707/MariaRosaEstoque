from flask import Flask, render_template, request, redirect, session, flash

class Macaquinho:
    def __init__(self, nome, cor, valor):
        self.nome = nome
        self.cor = cor
        self.preco = valor

macaquinho1 = Macaquinho('Macaquinho Raposa', 'Amarelo', 44.99)
macaquinho2 = Macaquinho('Macaquinho Bambi', "Cinza estampado", 44.99)
macaquinho3 = Macaquinho('Macaquinho Ursinho Polar', 'Azul Estampado', 44.99)
lista = [macaquinho1, macaquinho2, macaquinho3]

app= Flask(__name__)
app.secret_key = 'rosemary'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Maria Rosa Estoque', produtos=lista)

@app.route('/novoproduto')
def novoproduto():
    return render_template('novoproduto.html', titulo='Novo Produto')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    cor = request.form['cor']
    valor = request.form['valor']
    macaquinho4 = Macaquinho(nome, cor, valor)
    lista.append(macaquinho4)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
     if 'Maria@lafayette33*' == request.form['senha']:
         session['usuario_logado'] = request.form['usuario']
         flash(session['usuario_logado'] + ' logado com sucesso!')
         return redirect('/')
     else:
         flash('Falha no login, por favor verifique seu login e/ou senha.')
         return redirect('/login')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/')

app.run(debug=True)