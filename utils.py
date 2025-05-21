import re

def limpar_dados_entrada(texto):
    """Remove espaços extras e caracteres potencialmente perigosos."""
    if not texto:
        return ''
    return texto.strip()

def normalizar_nome(nome):
    """Coloca o nome no formato capitalizado (Ex: joão da silva -> João Da Silva)."""
    if not nome:
        return ''
    return ' '.join(p.capitalize() for p in nome.strip().split())

def classificar_usuarios(lista_usuarios, campo='id'):
    """Classifica os usuários com base em um campo: id, nome ou email."""
    if campo not in ['id', 'nome', 'email']:
        campo = 'id'
    return sorted(lista_usuarios, key=lambda x: getattr(x, campo))

def filtrar_por_consentimento(lista_usuarios, consentiu=True):
    """Filtra usuários que aceitaram (ou não) o consentimento."""
    return [u for u in lista_usuarios if u.consentimento == consentiu]

def buscar_usuarios(lista_usuarios, termo):
    """Busca usuários por nome ou e-mail contendo o termo (case insensitive)."""
    termo = termo.lower()
    return [
        u for u in lista_usuarios
        if termo in u.nome.lower() or termo in u.email.lower()
    ]
