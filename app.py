from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return('Bruno Gallego')

if __name__ == '__main__':
    app.run()
