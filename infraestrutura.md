# Infraestrutura da Aplicação Web Flask

## 1. Visão Geral

Este documento descreve a arquitetura de infraestrutura para uma aplicação web em Flask que realiza autenticação de usuários, geração de relatórios, e manipulação segura de dados.

---

## 2. Componentes

### Servidor de Aplicação

- **Flask + Gunicorn** (produção)
- **Servidor reverso:** Nginx
- **Gerenciador de pacotes:** pip + requirements.txt

### Banco de Dados

- **PostgreSQL** em ambiente gerenciado (Render, Railway, ou AWS RDS)

### Armazenamento

- Dados armazenados no banco
- Backups automáticos semanais
- Logs mantidos via sistema de monitoramento da plataforma (ex: Render ou AWS CloudWatch)

---

## 3. Justificativas Tecnológicas

| Tecnologia  | Justificativa |
|-------------|---------------|
| Flask       | Framework minimalista, ideal para APIs |
| PostgreSQL  | Banco relacional seguro e robusto |
| Docker      | Permite deploy padronizado |
| Nginx       | Servidor reverso confiável para produção |
| Gunicorn    | Servidor WSGI compatível com Flask |

---

## 4. Escalabilidade e Redundância

- **Escalabilidade horizontal:** múltiplas instâncias da aplicação via contêineres (Docker)
- **Balanceamento de carga:** Nginx ou serviço da plataforma (ex: AWS ALB)
- **Backup:** agendado e automático, exportado em formato SQL ou JSON

---

## 5. Segurança

- **HTTPS obrigatório**
- **Criptografia de senhas:** bcrypt via `werkzeug.security`
- **Autenticação por sessão segura**
- **Controle de acesso via decorators**
- **Firewall de aplicação** (ex: Cloudflare)
- **Validação e limpeza de entradas**
- **Testes de penetração sugeridos via ferramentas como OWASP ZAP**

---

## 6. DevSecOps desde o início

- Validação de inputs e sanitização
- Tratamento de exceções com logs e mensagens amigáveis
- Separação entre camadas de aplicação
- Código versionado com Git

