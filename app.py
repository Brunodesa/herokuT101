from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


def herokudb():
    Host = 'ec2-23-21-91-183.compute-1.amazonaws.com'
    Database = 'd8r8pp6b4u5qdk'
    User = 'plttdyqtbutaix'
    Password = '097775965643de2cc71b7e73ef7b95b75859f8868aa7bfd4cb24a53b8d4b74fb'
    return psycopg2.connect(host=Host, database=Database, user=User, password=Password, sslmode='require')


@app.route('/')
def index():
    return render_template('index.html')


def gravar(v1, v2, v3):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (nome text,email text, passe text)")
    db.execute("INSERT INTO usr VALUES (%s, %s, %s)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()


def existe(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE nome = %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor = None
    return valor


def eliminar(v1):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("DELETE FROM usr WHERE nome = %s", (v1,))
    ficheiro.commit()
    ficheiro.close()
    return


def log(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome = %s and passe = %s", (v1, v2,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


@app.route('/p1')
def p1():
    return render_template('p1.html')


@app.route('/registo', methods=['GET', 'POST'])
def registo():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if existe(v1):
            erro = 'O Utilizador já existe.'
        elif v3 != v4:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2, v3)
            erro = 'Utilizador Criado'
    return render_template('registo.html', erro=erro)


def alterar(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("UPDATE usr SET passe = %s WHERE nome = %s", (v2, v1))
    ficheiro.commit()
    ficheiro.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            erro = 'Bem-Vindo.'
    return render_template('login.html', erro=erro)


@app.route('/newpasse', methods=['GET', 'POST'])
def newpasse():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        v3 = request.form['cpasse']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
            erro = 'A palavra passe foi alterada com sucesso'
    return render_template('newpasse.html', erro=erro)


@app.route('/apagar', methods=['POST', 'GET'])
def apagar():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A senha está incorreta.'
        else:
            eliminar(v1)
            erro = 'Conta eliminada com Sucesso.'
    return render_template('apagar.html', erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
