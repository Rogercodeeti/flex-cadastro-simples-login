from flask import Flask, render_template, request, redirect, url_for,session,flash
app = Flask(__name__)
app.secret_key = 'segredo_super_importante'  # necessário para usar session
USUARIO_VALIDO = {
    'usuario': 'admin',
    'senha': '1234'
}

dados_pessoais = []

@app.route('/')
def login():
    # Se já estiver logado, vai direto pra index
    if session.get('logado'):
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    if usuario == USUARIO_VALIDO['usuario'] and senha == USUARIO_VALIDO['senha']:
        session['logado'] = True
        session['usuario'] = usuario
        flash('Login realizado com sucesso!', 'sucesso')
        return redirect(url_for('index'))
    else:
        flash('Usuário ou senha incorretos.', 'erro')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if not session.get('logado'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        if nome and email and telefone:
            dados_pessoais.append({
                'nome': nome,
                'email': email,
                'telefone': telefone
            })
            return redirect(url_for('listar'))
    return render_template('cadastrar.html')


@app.route('/listar')
def listar():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('listar.html', dados=dados_pessoais)


if __name__ == '__main__':
    app.run(debug=True)
