# Importando as bibliotecas do Flask, segurança, banco de dados, validação e utilitários
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json

# Importando funções personalizadas de arquivos do projeto
from utils import (
    limpar_dados_entrada,
    normalizar_nome,
    classificar_usuarios,
    filtrar_por_consentimento,
    buscar_usuarios
)
from validators import validar_email, validar_nome

# Criando o app Flask
app = Flask(__name__)
# Carregando configurações do projeto (como chave secreta e banco)
app.config.from_object('config.Config')
# Inicializando o banco com SQLAlchemy
db = SQLAlchemy(app)

# Redireciona para HTTPS automaticamente (se não estiver em modo debug)
@app.before_request
def before_request():
    if not request.is_secure and not app.debug:
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)

# Definindo o modelo da tabela de usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    consentimento = db.Column(db.Boolean, default=False)

# Decorador pra exigir login nas rotas
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado pra acessar essa página.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Página inicial, só acessa se estiver logado
@app.route('/')
@login_requerido
def index():
    usuario = Usuario.query.get_or_404(session['usuario_id'])
    return render_template('index.html', usuario=usuario)

# Rota de cadastro de novos usuários
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Pegando os dados do formulário
        nome = normalizar_nome(request.form.get('nome'))
        email = limpar_dados_entrada(request.form.get('email'))
        senha = request.form.get('senha')
        consentimento = 'consentimento' in request.form

        # Validando os campos
        if not nome or not email or not senha:
            flash('Preencha todos os campos, por favor.')
            return redirect(url_for('registro'))

        if not validar_nome(nome):
            flash('Nome inválido.')
            return redirect(url_for('registro'))

        if not validar_email(email):
            flash('E-mail inválido.')
            return redirect(url_for('registro'))

        if Usuario.query.filter_by(email=email).first():
            flash('Esse e-mail já está sendo usado.')
            return redirect(url_for('registro'))

        # Criptografando a senha e criando o usuário
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash, consentimento=consentimento)

        # Tentando salvar no banco
        try:
            db.session.add(novo_usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Erro ao salvar no banco de dados: ' + str(e))
            return redirect(url_for('registro'))

        flash('Cadastro feito! Agora é só logar.')
        return redirect(url_for('login'))

    return render_template('registro.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = limpar_dados_entrada(request.form.get('email'))
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Tem que preencher o e-mail e a senha.')
            return redirect(url_for('login'))

        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário existe e a senha bate
        if usuario and check_password_hash(usuario.senha_hash, senha):
            session['usuario_id'] = usuario.id
            flash('Login feito com sucesso!')
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha errados.')
            return redirect(url_for('login'))

    return render_template('login.html')

# Rota de logout (encerra a sessão)
@app.route('/logout')
@login_requerido
def logout():
    session.pop('usuario_id', None)
    flash('Você saiu da conta.')
    return redirect(url_for('login'))

# Rota que gera um relatório de usuários em JSON bruto (sem download)
@app.route('/relatorio')
@login_requerido
def relatorio():
    criterio = request.args.get('ordenar_por', 'id')
    usuarios = Usuario.query.all()
    usuarios = classificar_usuarios(usuarios, criterio)
    lista_usuarios = [
        {
            'id': u.id,
            'nome': u.nome,
            'email': u.email,
            'consentimento': u.consentimento
        } for u in usuarios
    ]
    r
