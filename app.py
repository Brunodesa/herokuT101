from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registo')
def registo():
    return render_template('registo.html')


@app.route('/jogos')
def jogos():
    return render_template('jogos.html')


@app.route('/carrinho')
def carrinho():
    return render_template('/carrinho.html')

if __name__ == '__main__':
    app.run(debug=True)
