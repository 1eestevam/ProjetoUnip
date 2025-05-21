from utils import limpar_dados_entrada, normalizar_nome

def test_limpar_dados_entrada():
    assert limpar_dados_entrada('  email@exemplo.com ') == 'email@exemplo.com'
    assert limpar_dados_entrada(None) == ''

def test_normalizar_nome():
    assert normalizar_nome(' joão da Silva ') == 'João Da Silva'
    assert normalizar_nome('MARIA') == 'Maria'
