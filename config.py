class Config:
    SECRET_KEY = 'sua_chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///usuarios.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # banco em memória
    WTF_CSRF_ENABLED = False

SECRET_KEY = 'uma_chave_muito_secreta_aleatoria'  # Troque para algo secreto e complexo
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # Envia cookie apenas por HTTPS
PERMANENT_SESSION_LIFETIME = 3600  # Duração da sessão em segundos (ex: 1 hora)
