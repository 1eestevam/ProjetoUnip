# tests/test_validators.py
from validators import validar_email

def test_email_valido():
    assert validar_email('teste@exemplo.com')

def test_email_invalido():
    assert not validar_email('email_invalido')
