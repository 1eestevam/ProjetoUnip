# Importa as bibliotecas necessárias do Flask, SQLAlchemy e Werkzeug
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Cria a aplicação Flask
app = Flask(__name__)
# Carrega as configurações a partir do arquivo config.py (classe Config)
app.config.from_object('config.Config')

# Inicializa a conexão com o banco de dados usando SQLAlchemy
db = SQLAlchemy(app)

# Define o modelo da tabela 'Usuario' no banco de dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Campo id (chave primária)
    nome = db.Column(db.String(100), nullable=False)  # Campo nome (obrigatório)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Campo email (único e obrigatório)
    senha_hash = db.Column(db.String(200), nullable=False)  # Campo para armazenar a senha criptografada
    consentimento = db.Column(db.Boolean, default=False)  # Campo para armazenar consentimento (padrão falso)

# Rota principal da aplicação (página inicial)
@app.route('/')
def index():
    if 'usuario_id' in session:  # Verifica se o usuário está logado
        usuario = Usuario.query.get_or_404(session['usuario_id'])  # Busca o usuário pelo ID na sessão
        return render_template('index.html', usuario=usuario)  # Exibe a página inicial passando os dados do usuário
    return redirect(url_for('login'))  # Se não estiver logado, redireciona para a página de login

# Rota para registro de novos usuários
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':  # Se o formulário for enviado (método POST)
        nome = request.form.get('nome')  # Pega o valor do campo nome
        email = request.form.get('email')  # Pega o valor do campo email
        senha = request.form.get('senha')  # Pega o valor do campo senha
        consentimento = 'consentimento' in request.form  # Verifica se o checkbox de consentimento foi marcado

        # Validação: todos os campos devem ser preenchidos
        if not nome or not email or not senha:
            flash('Todos os campos são obrigatórios.')  # Exibe mensagem de erro
            return redirect(url_for('registro'))  # Redireciona de volta para o registro

        # Verifica se o email já está cadastrado no banco
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.')  # Exibe mensagem de erro
            return redirect(url_for('registro'))  # Redireciona de volta para o registro

        # Criptografa a senha digitada pelo usuário
        senha_hash = generate_password_hash(senha)
        # Cria um novo objeto Usuario com os dados informados
        novo_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash, consentimento=consentimento)

        # Adiciona o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso.')  # Exibe mensagem de sucesso
        return redirect(url_for('login'))  # Redireciona para a página de login

    return render_template('registro.html')  # Exibe a página de registro (GET)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Se o formulário for enviado (método POST)
        email = request.form.get('email')  # Pega o valor do campo email
        senha = request.form.get('senha')  # Pega o valor do campo senha

        # Validação: todos os campos devem ser preenchidos
        if not email or not senha:
            flash('Por favor, preencha todos os campos.')  # Exibe mensagem de erro
            return redirect(url_for('login'))  # Redireciona de volta para o login

        # Busca o usuário pelo email informado
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário existe e se a senha está correta
        if usuario and check_password_hash(usuario.senha_hash, senha):
            session['usuario_id'] = usuario.id  # Armazena o ID do usuário na sessão (usuário logado)
            flash('Login realizado com sucesso!')  # Exibe mensagem de sucesso
            return redirect(url_for('index'))  # Redireciona para a página inicial
        else:
            flash('E-mail ou senha incorretos.')  # Exibe mensagem de erro
            return redirect(url_for('login'))  # Redireciona de volta para o login

    return render_template('login.html')  # Exibe a página de login (GET)
