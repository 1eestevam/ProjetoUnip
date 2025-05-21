def test_registro(client):
    response = client.post('/registro', data={
        'nome': 'Novo Usuario',
        'email': 'novo@usuario.com',
        'senha': 'senha123',
        'consentimento': 'on'
    }, follow_redirects=True)
    assert 'Cadastro feito! Agora é só logar.' in response.data.decode('utf-8')
