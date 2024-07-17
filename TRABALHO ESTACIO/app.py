from flask import Flask, render_template, request, redirect, url_for
import re
from parse_rest.connection import register
from parse_rest.datatypes import Object

app = Flask(__name__)

# Configurar a conexão com o Parse Server no Back4app
APPLICATION_ID = "s548E2hkmEyCDaJLR4T8cvEJ6v62dYdvCHqI4QNe"
REST_API_KEY = "K6PkiM4zVEf4EDOvbnz05Ngvghc87cbGPgacBCuc"
MASTER_KEY = "DPVkfosoyh28VIvDn6VCOrsnS2tUu5WdNHDu600q"
register(APPLICATION_ID, REST_API_KEY, master_key=MASTER_KEY)

class Pessoa(Object):
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form['nome']
    idade = request.form['idade']
    endereco = request.form['endereco']
    cep = request.form['cep']
    integrantes_familia = request.form['integrantes_familia']
    escolaridade = request.form['escolaridade']
    uso_tecnologia = request.form['uso_tecnologia']
    dificuldades_tecnologia = request.form['dificuldades_tecnologia']

    # Validação de dados
    if not re.match(r'^\d{5}-\d{3}$', cep):
        return "CEP inválido. O formato deve ser 12345-678.", 400
    if not nome or not idade or not endereco or not integrantes_familia or not escolaridade or not uso_tecnologia or not dificuldades_tecnologia:
        return "Todos os campos são obrigatórios.", 400

    nova_pessoa = Pessoa(
        nome=nome, idade=idade, endereco=endereco, cep=cep,
        integrantes_familia=integrantes_familia, escolaridade=escolaridade,
        uso_tecnologia=uso_tecnologia, dificuldades_tecnologia=dificuldades_tecnologia
    )
    nova_pessoa.save()

    return redirect(url_for('index'))

@app.route('/relatorio')
def relatorio():
    pessoas = Pessoa.Query.all()
    return render_template('relatorio.html', pessoas=pessoas)

if __name__ == '__main__':
    app.run(debug=True)
