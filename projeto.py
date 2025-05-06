from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        consentimento = True if 'consentimento' in request.form else False

        novo_usuario = Usuario(nome=nome, email=email, senha_hash=senha, consentimento=consentimento)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))
    return render_template('registro.html')
