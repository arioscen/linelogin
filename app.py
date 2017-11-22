from flask import Flask, render_template, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/Index.html')
def index():
    return render_template('Index.html')


@app.route('/')
def main():
    return redirect(url_for('index'))


@app.route('/profile/')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
