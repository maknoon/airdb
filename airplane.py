#!~/usr/bin/python
from flask import Flask

app = Flask(__name__)

# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route('/')
def index():
    return 'airdb'

@app.route('/test/<name>')
def test_name(name):
    return 'Welcome, {}!'.format(name)


if __name__ == '__main__':
    app.run()
